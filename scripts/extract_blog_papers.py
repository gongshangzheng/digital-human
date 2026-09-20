#!/usr/bin/env python3
"""扫描博客 src/pages/*.html，识别数字人相关页面，输出结构化清单供人工复核。

用法：
    python3 scripts/extract_blog_papers.py [--blog ~/gongshangzheng.github.io]

输出：papers/data/blog_papers.json
    每条记录：slug / title / description / tags / date / rel_path /
              arxiv_id(可选) / hit_reasons / category(待人工填写) / deny(默认 false)

复核方式：
    1. 将误命中条目的 "deny" 改为 true（并可在 hit_reasons 备注）
    2. 为每条填写 category（六类之一，见 CATEGORY_SET）
    3. 运行 scripts/import_papers.py 导入 SQLite
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ---------------- 配置 ----------------

BLOG_DEFAULT = Path.home() / "gongshangzheng.github.io"
PAGES_DIR = "src/pages"
OUTPUT_REL = Path("papers/data/blog_papers.json")

# 正文/标题/tags 关键词（不区分大小写）
KEYWORDS = [
    "talking head", "talking face", "talking portrait", "talkinghead",
    "digital human", "数字人", "虚拟人",
    "avatar", "digital avatar",
    "audio-driven", "audio driven", "语音驱动", "音频驱动",
    "lip sync", "lip-sync", "lipsync", "口型", "唇形",
    "面部动画", "人脸动画", "portrait animation",
    "talking portrait generation", "语音肖像",
]

# 文件名（slug）强模式：命中即视为数字人相关
SLUG_STRONG = [
    r"^paper-", r"^digital-human", r"^cyberverse", r"ditto", r"avatar",
    r"^gfvc", r"^ex-omni", r"^wan-streamer", r"^opens2v", r"^infinitetalk",
    r"^lam-", r"^lhm-", r"^mead-", r"^hdtf", r"^vfhq-", r"^unils-",
    r"^consisid-", r"^arc2face-", r"^anigs-", r"^emo-", r"^geneava-",
    r"^hypergaussians", r"^motionshop", r"^semhitok-", r"^styledit-",
    r"^styleid-", r"^theval-", r"^vbench", r"^id-sim", r"^captalk",
    r"^flexavatar", r"^smartavatar", r"^liveavatar", r"^realtime-",
    r"^voice-ai", r"^tool-augmented",
]

# 文件名（slug）弱模式：需叠加至少一个关键词命中才计入
SLUG_WEAK = [r"survey", r"arxiv-digest", r"talk"]

# 明确排除（弱关键词误命中 / 与数字人无关）
DENYLIST_DEFAULT = [
    "php-security", "dive-into-llms-ch08-mllm",
]

CATEGORY_SET = [
    "2d-talking-head", "3d-avatar", "audio-driven-animation",
    "realtime-system", "evaluation-dataset", "survey",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-", "\t")):
            k, _, v = line.partition(":")
            v = v.strip().strip('"').strip("'")
            if v:
                fm[k.strip()] = v
    return fm


def extract_arxiv_id(text: str) -> str | None:
    # 链接形式或正文提及（如 arxiv.org/abs/2506.12345、arXiv:2506.12345）
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", text)
    if m:
        return m.group(1)
    m = re.search(r"arXiv[:：]\s*(\d{4}\.\d{4,5})", text)
    if m:
        return m.group(1)
    return None


def slug_matches(slug: str) -> tuple[list[str], list[str]]:
    strong, weak = [], []
    for pat in SLUG_STRONG:
        if re.search(pat, slug, re.IGNORECASE):
            strong.append(f"slug~{pat}")
    for pat in SLUG_WEAK:
        if re.search(pat, slug, re.IGNORECASE):
            weak.append(f"slugweak~{pat}")
    return strong, weak


def keyword_hits(haystack: str) -> list[str]:
    hits = []
    low = haystack.lower()
    for kw in KEYWORDS:
        if kw.lower() in low:
            hits.append(f"kw~{kw}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", type=Path, default=BLOG_DEFAULT, help="博客仓库路径")
    args = ap.parse_args()

    pages = args.blog / PAGES_DIR
    if not pages.is_dir():
        print(f"ERROR: {pages} 不存在", file=sys.stderr)
        return 1

    records = []
    for f in sorted(pages.glob("*.html")):
        slug = f.stem
        if slug in DENYLIST_DEFAULT:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        # 正文取 frontmatter 之后部分（控制扫描量）
        body = text[6000:60000] if FRONTMATTER_RE.match(text) else text[:40000]
        title = fm.get("title", slug)
        tags = fm.get("tags", "")

        reasons = keyword_hits(f"{title}\n{tags}")
        strong, weak = slug_matches(slug)
        reasons += strong
        # 弱 slug 需叠加关键词；标题/tags 未命中时再看正文前 20k（要求 ≥2 个不同关键词）
        if not reasons:
            body_hits = keyword_hits(body[:20000])
            if len(set(body_hits)) >= 2:
                reasons += body_hits[:5]
        if weak and reasons:
            reasons += weak
        if not reasons:
            continue

        records.append({
            "slug": slug,
            "title": title,
            "description": fm.get("description", ""),
            "tags": tags,
            "date": fm.get("date", ""),
            "rel_path": f"{PAGES_DIR}/{f.name}",
            "arxiv_id": extract_arxiv_id(body),
            "hit_reasons": sorted(set(reasons)),
            "category": "",  # 待人工复核填写（六类之一）
            "deny": False,   # 人工置 true 排除
        })

    out = Path(__file__).parent.parent / OUTPUT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"共命中 {len(records)} 篇 → {out}")
    print(f"下一步：人工复核（deny 误命中 / 填 category ∈ {CATEGORY_SET}），然后运行 import_papers.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
