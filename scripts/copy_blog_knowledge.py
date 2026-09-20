#!/usr/bin/env python3
"""将博客精选文档型页面（survey/工程解读）从 HTML 转为 Markdown 复制到知识库。

用法：python3 scripts/copy_blog_knowledge.py [--blog ~/gongshangzheng.github.io]

精选清单（BLOG_SELECTION）：设计/综述/工程类，论文单篇精读不入知识库
（已在 papers 库中索引，带 blog_url）。
"""
import argparse
import re
from datetime import date
from pathlib import Path

import html2text

BLOG_DEFAULT = Path.home() / "gongshangzheng.github.io"
OUT_DIR = Path(__file__).parent.parent / "management" / "docs" / "knowledge" / "blog"

# slug → (目标文件名, 说明)
BLOG_SELECTION = {
    "digital-human-survey-map": "数字人 survey 全景图",
    "digital-human-avatar-survey": "数字人 Avatar 综述",
    "realtime-digital-human-survey": "实时数字人综述",
    "gfvc-survey-2023": "GFVC 人脸视频编码综述",
    "digital-human-engineering-benchmark": "数字人工程基准",
    "digital-human-training-inference-benchmark": "训练推理基准",
    "digital-human-realtime-gpu-comparison": "实时方案 GPU 对比",
    "digital-human-streaming-distillation": "流式蒸馏",
    "digital-human-identity-consistency": "身份一致性",
    "cyberverse-realtime-digital-human-agent": "CyberVerse 实时数字人 Agent",
    "cyberverse-flashhead-lite-experiment": "FlashHead Lite 实验",
    "realtime-communication-hub": "实时通信系列（Hub）",
    "realtime-communication-media-pipeline": "实时通信媒体管线",
    "realtime-communication-server-architecture": "实时通信服务端架构",
    "realtime-communication-webrtc-core": "WebRTC 核心",
    "realtime-communication-network-basics": "实时网络基础",
    "tool-augmented-digital-human": "工具增强数字人",
    "voice-ai-digital-human-landscape": "语音 AI 数字人全景",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def convert(page: Path) -> tuple[str, str]:
    """返回 (frontmatter, markdown 正文)。"""
    text = page.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    fm = m.group(1) if m else ""
    body = text[m.end():] if m else text

    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_images = False
    h.ignore_links = False
    md = h.handle(body)
    # 压缩连续空行
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return fm, md


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", type=Path, default=BLOG_DEFAULT)
    args = ap.parse_args()

    pages = args.blog / "src" / "pages"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    copied = []
    for slug, desc in BLOG_SELECTION.items():
        src = pages / f"{slug}.html"
        if not src.exists():
            print(f"WARN 缺失: {src}")
            continue
        fm, md = convert(src)
        header = (
            f"> 来源：博客 gongshangzheng.github.io `src/pages/{slug}.html`，"
            f"html2text 转换复制于 {today}。原文：https://gongshangzheng.github.io/{slug}.html\n\n"
        )
        out = OUT_DIR / f"{slug}.md"
        out.write_text(f"---\n{fm}\n---\n\n{header}{md}\n", encoding="utf-8")
        copied.append(slug)

    print(f"复制 {len(copied)}/{len(BLOG_SELECTION)} 篇 → {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
