#!/usr/bin/env python3
"""从复核后的博客论文清单（papers/data/blog_papers.json）导入 SQLite 论文库。

流程：
1. 读取 extract_blog_papers.py 产出并经人工复核的 JSON（deny=true 跳过）
2. 对含 arXiv id 的条目分批调用 arXiv API 补全元数据（失败标记，可重试）
3. upsert 到 data/papers.db（papers + paper_categories），幂等可重跑

用法：
    python3 scripts/import_papers.py               # 全量导入
    python3 scripts/import_papers.py --refresh     # 重新补全此前 arXiv 缺失的条目
"""
import argparse
import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from server.db import init_db, upsert_paper  # noqa: E402

DB_PATH = Path(__file__).parent.parent / "data" / "papers.db"
PAPERS_JSON = Path(__file__).parent.parent / "papers" / "data" / "blog_papers.json"
ARXIV_API = "http://export.arxiv.org/api/query"
BLOG_BASE = "https://gongshangzheng.github.io"
NS = {"atom": "http://www.w3.org/2005/Atom"}

# 人工核验过的 id（slug token 无法自动匹配但确认正确）
ARXIV_ALLOWLIST = {
    "match-2026": "2603.15811",
    "gfvc-survey-2023": "2403.11641",
}

# 太泛的 token，不作为单独匹配依据
GENERIC_TOKENS = {
    "digital", "human", "paper", "survey", "hub", "talk", "talking", "avatar",
    "face", "video", "live", "real", "time", "realtime", "source", "code",
    "analysis", "read", "about", "tool", "augmented", "engineering", "benchmark",
    "comparison", "landscape", "design", "gallery", "brainstorm", "evaluation",
    "training", "loss", "system", "communication", "media", "pipeline", "server",
    "network", "basics", "core", "arxiv", "digest", "blog", "notes",
}

SUFFIX_STRIP = [
    "-source-code-analysis", "-source-read", "-source", "-read", "-paper", "-review",
]


def _norm(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalnum())


def verify_arxiv_match(slug: str, arxiv_title: str) -> bool:
    """slug 与 arXiv 标题 token 匹配：digest/hub/概述页首链接不可靠，不匹配则降级为纯博客条目。"""
    if slug in ARXIV_ALLOWLIST:
        return True
    base = slug
    for suf in SUFFIX_STRIP:
        if base.endswith(suf):
            base = base[: -len(suf)]
    tokens = [t for t in base.split("-") if t and not t.isdigit() and t != "paper"]
    title = _norm(arxiv_title)
    joined = _norm("-".join(tokens))
    if joined and joined in title:
        return True
    return any(len(t) >= 3 and t not in GENERIC_TOKENS and _norm(t) in title for t in tokens)


def fetch_arxiv_batch(arxiv_ids: list[str]) -> tuple[dict, list[str]]:
    """批量获取论文元数据。返回 (结果表, 失败 id 列表)。"""
    results: dict[str, dict] = {}
    failed: list[str] = []
    batch_size = 50
    for i in range(0, len(arxiv_ids), batch_size):
        batch = arxiv_ids[i:i + batch_size]
        params = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": len(batch)})
        url = f"{ARXIV_API}?{params}"
        print(f"  Fetching arXiv batch {i // batch_size + 1}: {len(batch)} papers...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                root = ET.fromstring(resp.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  WARN batch failed: {e}")
            failed.extend(batch)
            continue

        for entry in root.findall("atom:entry", NS):
            entry_id = entry.find("atom:id", NS).text or ""
            arxiv_id = entry_id.split("/abs/")[-1]
            base, _, ver = arxiv_id.rpartition("v")
            if ver.isdigit():
                arxiv_id = base

            title = " ".join((entry.find("atom:title", NS).text or "").split())
            summary = " ".join((entry.find("atom:summary", NS).text or "").split())
            published = (entry.find("atom:published", NS).text or "").strip()

            authors = [a.find("atom:name", NS).text for a in entry.findall("atom:author", NS)
                       if a.find("atom:name", NS) is not None]
            pdf_url = ""
            for link in entry.findall("atom:link", NS):
                if link.get("title") == "pdf":
                    pdf_url = link.get("href", "")
                    break
            results[arxiv_id] = {
                "title": title,
                "abstract": summary,
                "authors": json.dumps(authors, ensure_ascii=False),
                "published_at": published or None,
                "pdf_url": pdf_url,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "arxiv_categories": [c.get("term", "") for c in entry.findall("atom:category", NS)],
            }
        if i + batch_size < len(arxiv_ids):
            time.sleep(3)  # arXiv API 礼貌限速
    return results, failed


def to_iso_date(date_str: str) -> str | None:
    """博客 frontmatter 日期（2026-06-05T17:55:22 或 2026-06-05）→ ISO 日期。"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="重试此前 arXiv 补全失败的条目")
    args = ap.parse_args()

    if not PAPERS_JSON.exists():
        print(f"ERROR: {PAPERS_JSON} 不存在，先运行 extract_blog_papers.py 并完成人工复核", file=sys.stderr)
        return 1

    records = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    kept = [r for r in records if not r.get("deny")]
    denied = len(records) - len(kept)
    print(f"清单：{len(records)} 条（deny {denied}），导入 {len(kept)} 条")

    # 分组：有/无 arxiv id
    with_arxiv = [r for r in kept if r.get("arxiv_id")]
    without = [r for r in kept if not r.get("arxiv_id")]
    ids = list({r["arxiv_id"] for r in with_arxiv})
    print(f"arXiv 补全：{len(ids)} 个 id（无 id 博客条目 {len(without)} 篇直接落库）")

    arxiv_meta: dict[str, dict] = {}
    arxiv_failed: set[str] = set()
    if ids:
        arxiv_meta, failed = fetch_arxiv_batch(ids)
        arxiv_failed = set(failed)
        print(f"  arXiv 成功 {len(arxiv_meta)} / 失败 {len(arxiv_failed)}")

    init_db()
    now = datetime.now().isoformat()
    imported = arxiv_ok = arxiv_miss = 0
    upserted: list[dict] = []

    for r in kept:
        slug = r["slug"]
        blog_url = f"{BLOG_BASE}/{slug}.html"
        meta = arxiv_meta.get(r.get("arxiv_id") or "")
        if meta and not verify_arxiv_match(slug, meta.get("title", "")):
            # 概述/digest 页首链接不可靠：降级为纯博客条目
            meta = None
            r = {**r, "arxiv_id": None}
        arxiv_status = (
            "ok" if meta else
            ("failed" if r.get("arxiv_id") in arxiv_failed else "no_id")
        )

        paper_id = f"arxiv-{r['arxiv_id']}" if r.get("arxiv_id") else f"blog-{slug}"
        paper = {
            "id": paper_id,
            "title": (meta or {}).get("title") or r.get("title") or slug,
            "abstract": (meta or {}).get("abstract") or r.get("description") or "",
            "authors": (meta or {}).get("authors") or json.dumps(["Unknown"]),
            "published_at": (meta or {}).get("published_at") or to_iso_date(r.get("date", "")),
            "url": (meta or {}).get("url") or blog_url,
            "pdf_url": (meta or {}).get("pdf_url", ""),
            "source": "blog",
            "categories": [r["category"]] if r.get("category") else [],
            "arxiv_categories": (meta or {}).get("arxiv_categories", []),
            "blog_url": blog_url,
            "metadata": json.dumps({
                "slug": slug,
                "rel_path": r.get("rel_path", ""),
                "hit_reasons": r.get("hit_reasons", []),
                "arxiv_status": arxiv_status,
            }, ensure_ascii=False),
            "crawled_at": now,
        }
        upsert_paper(paper)
        upserted.append(paper)
        imported += 1
        if arxiv_status == "ok":
            arxiv_ok += 1
        elif arxiv_status == "failed":
            arxiv_miss += 1

    # 清理本批次之外的旧 blog 条目（重跑后降级/合并产生的脏行）
    conn = sqlite3.connect(DB_PATH)
    ids = tuple(p["id"] for p in upserted)
    stale = conn.execute(
        "SELECT id FROM papers WHERE source='blog' AND id NOT IN (%s)" % ",".join("?" * len(ids)),
        ids,
    ).fetchall()
    for (pid,) in stale:
        conn.execute("DELETE FROM paper_categories WHERE paper_id = ?", (pid,))
        conn.execute("DELETE FROM papers WHERE id = ?", (pid,))
        print(f"  清理旧行: {pid}")
    conn.commit()
    conn.close()
    print(f"导入完成：{imported} 条（arXiv ok={arxiv_ok} failed={arxiv_miss} no_id={imported - arxiv_ok - arxiv_miss}；清理旧行 {len(stale)}）")
    if arxiv_miss:
        print(f"提示：{arxiv_miss} 条 arXiv 补全失败已标记，稍后运行 --refresh 重试")
    return 0


if __name__ == "__main__":
    sys.exit(main())
