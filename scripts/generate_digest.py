"""Generate a sourced Chinese Markdown digest using OpenAI."""
import datetime as dt
import json
import os
import pathlib
import re
from openai import OpenAI
from fetch_news import fetch

def main():
    articles = fetch()
    tech = [x for x in articles if x["category"] == "tech"]
    world = [x for x in articles if x["category"] == "world"]
    if len(tech) < 3 or len(world) < 2:
        raise RuntimeError("Not enough recent articles; refusing to fabricate a digest")
    candidates = tech[:25] + world[:25]
    date = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date().isoformat()
    prompt = (
        "从提供的候选文章中选出恰好5条不同事件的重要新闻：科技与互联网3条、国际新闻2条。"
        "只依据候选标题、摘要和来源，不添加未经证实的事实。"
        "避免重复话题，每条用中文写标题、2至3句简述、1至2句价值分析。"
        "每条必须附上候选文章中完全一致的原始URL。"
        "不要生成或猜测图片URL；RSS缺少可靠图片时直接省略配图。"
        "按以下Markdown结构输出：二级标题、新闻摘要、价值分析、原文链接。"
        "不要添加候选列表以外的报道或虚构引述。\n"
        + json.dumps(candidates, ensure_ascii=False)
    )
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions="你是严谨的中文国际新闻编辑，不能编造事实、图片或来源。",
        input=prompt,
    )
    body = response.output_text.strip()
    links = re.findall(r"https://[^\s)>]+", body)
    allowed = {x["url"] for x in candidates}
    if len(links) != 5 or any(link not in allowed for link in links):
        raise RuntimeError("Digest source validation failed; not publishing")
    if len(set(links)) != 5:
        raise RuntimeError("Duplicate article URLs; not publishing")
    path = pathlib.Path("news") / date[:4] / date[5:7] / f"{date}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# 每日科技与国际新闻简报 · {date}\n\n" + body + "\n", encoding="utf-8")
    print(path)

if __name__ == "__main__":
    main()
