#!/usr/bin/env python3
"""采集数字人语料，生成「论文信息对」骨架并增量合并到文档 sidecar。

来源（去重合并）：
  A. 博客数字人页面：~/gongshangzheng.github.io/src/pages/*.html
     判据：frontmatter aliases 含 `categories/AI/数字人`
  B. 库内单篇论文笔记：management/docs/论文笔记/*.md

字段口径见 openspec/changes/docs-dh-key-technology-map/design.md。
骨架字段（blog_url / blog_date / tags / venue / institution / year / title /
title_zh / arxiv_id）每次刷新；内容字段（qa / derives_from / derived_by /
method_family / note / note_type）若已非空则保留，不被覆盖——便于人工/Agent
逐篇补全后再次重跑。

默认 dry-run：只打印统计与样例，不写盘。
    python3 scripts/collect_dh_paper_units.py
写入（先 --out 到缓存复核，或直接 --apply 到 sidecar）：
    python3 scripts/collect_dh_paper_units.py --out .cache/.../skeleton.json
    python3 scripts/collect_dh_paper_units.py --apply \
        --target "management/docs/数字人概述/数字人关键技术地图.json"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BLOG_DEFAULT = Path.home() / "gongshangzheng.github.io"
DOCS_DIR = REPO_ROOT / "management" / "docs"
NOTES_DIR = DOCS_DIR / "论文笔记"
DEFAULT_TARGET = DOCS_DIR / "数字人概述" / "数字人关键技术地图.json"
DH_CATEGORY = "categories/AI/数字人"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
YEAR_RE = re.compile(r"(19|20)\d{2}")
ARXIV_RE = re.compile(r"arXiv[:：]\s*(\d{4}\.\d{4,5})")

VENUE_HINTS = [
    "cvpr", "iccv", "eccv", "neurips", "nips", "siggraph", "iclr", "icml",
    "acm", "ieee", "aaai", "tpami", "ijcv", "tog", "tvcg", "bmvc", "wacv",
    "interspeech", "icassp", "pp-rai", "arxiv", "fg", "mm",
]
INSTITUTION_HINTS = [
    "university", "universit", "institute", "academy", "college", "school",
    "laboratory", " lab", "lab/", " labs", "research", "group", "team",
    "corporation", "corp.", "inc.", "google", "meta", "adobe", "nvidia",
    "microsoft", "bytedance", "alibaba", "tencent", "kuaishou", "baidu",
    "ant group", "deepmind", "openai", "apple", "samsung", "huawei",
    "eth ", "ethz", "mit", "cuhk", "hkust", "kaist", "nus", "ntu",
    "monash", "inria", "damo", "zip lab", "soul", "shengshu",
    "大学", "学院", "研究院", "实验室", "研究团队", "研究所", "科技", "集团",
    "团队", "公司", "清华", "北大", "复旦", "浙大", "交大", "中山大学",
    "南京大学", "北交", "北邮", "中国电信", "京东", "快手", "腾讯", "阿里",
    "百度", "字节", "蚂蚁", "优图", "混元", "通义", "生数",
]


def is_venue(text: str) -> bool:
    low = text.lower()
    return bool(YEAR_RE.fullmatch(text.strip())) or any(h in low for h in VENUE_HINTS)


def is_institution(text: str) -> bool:
    low = text.lower()
    return any(h in low for h in INSTITUTION_HINTS)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t", "-", "#")):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def parse_list(raw: str) -> list[str]:
    raw = (raw or "").strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [x.strip().strip('"').strip("'") for x in raw.split(",") if x.strip()]


def normalize_key(name: str) -> str:
    """把博客 slug / 笔记 slug / 简称归一，用于跨来源去重。"""
    s = name.lower().strip()
    s = re.sub(r"^paper-", "", s)
    s = re.sub(r"-\d{4}$", "", s)
    s = s.replace("_", "-").replace(" ", "-")
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff-]", "", s)
    return s


def parse_venue_institution(text: str) -> tuple[str | None, str | None, int | None]:
    """从 `hero_sub`（venue · 机构）或笔记 summary 括号（机构，venue year）解析。

    只把确为 venue / 机构的片段录入，子标题与宣传语一律丢弃。
    """
    if not text:
        return None, None, None
    raw = text.strip()
    ym = YEAR_RE.search(raw)
    year = int(ym.group(0)) if ym else None
    # 笔记 summary 形态：名字（机构，venue year）…
    m = re.match(r"^[^（(]*[（(]\s*([^，,）)]+?)\s*[，,]\s*([^）)]+?)\s*[）)]", raw)
    if m:
        institution = m.group(1).strip() or None
        venue_text = m.group(2).strip()
        return (venue_text if is_venue(venue_text) else None), institution, year

    venue_parts: list[str] = []
    inst_parts: list[str] = []
    for part in (p.strip() for p in raw.split("·")):
        if not part:
            continue
        if is_venue(part):
            venue_parts.append(part)
        elif is_institution(part):
            inst_parts.append(part)
    venue = " / ".join(venue_parts) or None
    institution = " + ".join(inst_parts) or None
    return venue, institution, year


def note_slug_to_doc(note_file: Path) -> str:
    rel = note_file.relative_to(DOCS_DIR).with_suffix("")
    return rel.as_posix()


def scan_blog(blog: Path) -> list[dict]:
    pages = blog / "src" / "pages"
    if not pages.is_dir():
        return []
    entries = []
    for f in sorted(pages.glob("*.html")):
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        aliases = fm.get("aliases", "")
        if DH_CATEGORY not in aliases:
            continue
        venue, institution, year = parse_venue_institution(fm.get("hero_sub", ""))
        entries.append({
            "id": f.stem,
            "source": ["blog"],
            "title_zh": fm.get("title", f.stem),
            "title": "",
            "blog_url": f"https://gongshangzheng.github.io/{f.name}",
            "blog_date": fm.get("date", "")[:10],
            "venue": venue,
            "institution": institution,
            "year": year,
            "arxiv_id": None,
            "tags": parse_list(fm.get("tags", "")),
            "method_family": "",
            "qa": [],
            "derives_from": [],
            "derived_by": [],
            "note": None,
            "note_type": None,
        })
    return entries


def scan_notes() -> list[dict]:
    if not NOTES_DIR.is_dir():
        return []
    entries = []
    for f in sorted(NOTES_DIR.glob("*.md")):
        if f.stem == "README":
            continue
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        venue, institution, year = parse_venue_institution(fm.get("summary", ""))
        entries.append({
            "id": f.stem,
            "source": ["note"],
            "title_zh": fm.get("title", f.stem),
            "title": "",
            "blog_url": None,
            "blog_date": fm.get("date", "")[:10],
            "venue": venue,
            "institution": institution,
            "year": year,
            "arxiv_id": fm.get("arxiv_id") or None,
            "tags": parse_list(fm.get("tags", "")),
            "method_family": "",
            "qa": [],
            "derives_from": [],
            "derived_by": [],
            "note": note_slug_to_doc(f),
            "note_type": "doc",
        })
    return entries


def merge(blog_entries: list[dict], note_entries: list[dict]) -> list[dict]:
    """按 normalize_key 合并；博客条目为主，笔记信息补全并去重。"""
    by_key: dict[str, dict] = {}
    for e in blog_entries:
        by_key.setdefault(normalize_key(e["id"]), e)

    for n in note_entries:
        key = normalize_key(n["id"])
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = n
            continue
        # 合并：保留博客骨架，补入笔记的 note/arxiv，合并 source
        existing["note"] = n["note"]
        existing["note_type"] = "doc"
        if n.get("arxiv_id") and not existing.get("arxiv_id"):
            existing["arxiv_id"] = n["arxiv_id"]
        if "note" not in existing["source"]:
            existing["source"].append("note")
        for field in ("venue", "institution", "year"):
            if not existing.get(field) and n.get(field):
                existing[field] = n[field]
    return list(by_key.values())


def assign_seq(entries: list[dict]) -> list[dict]:
    def sort_key(e: dict):
        return (e.get("year") or 9999, e.get("blog_date") or "")
    for i, e in enumerate(sorted(entries, key=sort_key), start=1):
        e["seq"] = i
    return sorted(entries, key=lambda e: e["seq"])


def merge_with_existing(new_entries: list[dict], existing: list[dict]) -> list[dict]:
    """保留已在 sidecar 中补全的内容字段。"""
    keep = {"qa", "derives_from", "derived_by", "method_family", "note", "note_type", "title"}
    old = {e.get("id"): e for e in existing}
    for e in new_entries:
        prev = old.get(e["id"])
        if not prev:
            continue
        for field in keep:
            if prev.get(field):
                e[field] = prev[field]
    return new_entries


def load_existing(target: Path) -> list[dict]:
    if not target.is_file():
        return []
    try:
        data = json.loads(target.read_text(encoding="utf-8") or "{}")
    except (json.JSONDecodeError, ValueError):
        return []
    return data.get("papers", []) if isinstance(data, dict) else []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", type=Path, default=BLOG_DEFAULT)
    ap.add_argument("--out", type=Path, default=None, help="骨架输出文件（不含 sidecar 其它键）")
    ap.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="sidecar 路径")
    ap.add_argument("--apply", action="store_true", help="写入 --target（否则只读）")
    args = ap.parse_args()

    blog_entries = scan_blog(args.blog)
    note_entries = scan_notes()
    merged = merge(blog_entries, note_entries)
    merged = merge_with_existing(merged, load_existing(args.target))
    merged = assign_seq(merged)

    n_blog = sum(1 for e in merged if "blog" in e["source"])
    n_note_only = sum(1 for e in merged if e["source"] == ["note"])
    n_note = sum(1 for e in merged if e.get("note"))
    n_inst = sum(1 for e in merged if e.get("institution"))
    n_venue = sum(1 for e in merged if e.get("venue"))
    n_year = sum(1 for e in merged if e.get("year"))

    print(f"条目总数: {len(merged)}（含博客 {n_blog}，库内独有 {n_note_only}）")
    print(f"有机构: {n_inst}  有 venue: {n_venue}  有年份: {n_year}  有笔记: {n_note}")
    print(f"博客命中: {len(blog_entries)}  笔记命中: {len(note_entries)}")
    print("\n样例（前 8 条）:")
    for e in merged[:8]:
        print(f"  #{e['seq']:>3} {e['id']:<32} {e.get('year')} {e.get('venue') or '-':<22} {e.get('institution') or '-'}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"papers": merged}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        try:
            shown = args.out.resolve().relative_to(REPO_ROOT)
        except ValueError:
            shown = args.out
        print(f"\n骨架已写入: {shown}")
    if args.apply:
        data = {}
        if args.target.is_file():
            try:
                data = json.loads(args.target.read_text(encoding="utf-8") or "{}")
            except (json.JSONDecodeError, ValueError):
                data = {}
        data["papers"] = merged
        args.target.parent.mkdir(parents=True, exist_ok=True)
        args.target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        try:
            shown_target = args.target.resolve().relative_to(REPO_ROOT)
        except ValueError:
            shown_target = args.target
        print(f"sidecar 已写入: {shown_target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
