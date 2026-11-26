#!/usr/bin/env python3
"""Build the news portal site: generate data.json from the content in this repo.

Usage: python build.py <repo-root> <out-dir>
"""
import json
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None

CATEGORIES = [
    ("news", "每日新闻"),
    ("macos", "macOS 周报"),
    ("ai", "AI 热门项目"),
]

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]


def extract_title(text):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return "未命名"


def render_body(text):
    body = []
    dropped = False
    for line in text.splitlines():
        if not dropped and line.strip().startswith("# "):
            dropped = True
            continue
        body.append(line)
    md = "\n".join(body).strip()
    if markdown is None:
        return md
    return markdown.markdown(md, extensions=MD_EXTENSIONS)


def main():
    if len(sys.argv) != 3:
        print("usage: build.py <daily-news-repo-dir> <out-dir>", file=sys.stderr)
        sys.exit(2)

    repo = Path(sys.argv[1])
    out = Path(sys.argv[2])

    articles = []
    for slug, label in CATEGORIES:
        cat_dir = repo / slug
        if not cat_dir.is_dir():
            print(f"warn: category dir missing: {cat_dir}", file=sys.stderr)
            continue
        for md_path in sorted(cat_dir.rglob("*.md")):
            text = md_path.read_text(encoding="utf-8")
            articles.append({
                "slug": slug,
                "category": label,
                "title": extract_title(text),
                "date": md_path.stem,
                "html": render_body(text),
                "path": str(md_path.relative_to(repo)),
            })

    articles.sort(key=lambda a: a["date"], reverse=True)

    data = {
        "categories": [{"slug": s, "label": l} for s, l in CATEGORIES],
        "articles": articles,
    }

    out.mkdir(parents=True, exist_ok=True)
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"built data.json: {len(articles)} articles across {len(CATEGORIES)} categories")


if __name__ == "__main__":
    main()
