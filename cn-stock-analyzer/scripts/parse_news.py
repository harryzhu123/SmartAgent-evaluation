"""
新闻文件解析器 - 支持 txt 和 csv 格式

用法：
    python parse_news.py --input news.txt --output parsed_news.json
    python parse_news.py --input news.csv --output parsed_news.json

支持的格式：
1. txt 文件：每条新闻用空行分隔，或每行一条新闻
2. csv 文件：包含 title/标题 列，可选 source/来源、time/时间 列

输出统一的 JSON 格式供后续分析使用。
"""

import json
import csv
import sys
import argparse
import re
from pathlib import Path


def parse_txt(filepath):
    """Parse a txt file containing news items."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Try splitting by double newline first (paragraph-separated)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]

    if len(paragraphs) >= 2:
        news_items = paragraphs
    else:
        # Fall back to line-by-line
        news_items = [line.strip() for line in content.splitlines() if line.strip()]

    results = []
    for item in news_items:
        parsed = extract_metadata(item)
        results.append(parsed)

    return results


def parse_csv(filepath):
    """Parse a csv file containing news items."""
    results = []

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # Normalize column names
        for row in reader:
            normalized = {k.strip().lower(): v.strip() for k, v in row.items() if v}

            title = (
                normalized.get("title")
                or normalized.get("标题")
                or normalized.get("新闻标题")
                or normalized.get("headline")
                or ""
            )
            source = (
                normalized.get("source")
                or normalized.get("来源")
                or normalized.get("新闻来源")
                or ""
            )
            time = (
                normalized.get("time")
                or normalized.get("时间")
                or normalized.get("date")
                or normalized.get("日期")
                or normalized.get("发布时间")
                or ""
            )
            content = (
                normalized.get("content")
                or normalized.get("内容")
                or normalized.get("正文")
                or normalized.get("摘要")
                or ""
            )

            if title or content:
                results.append({
                    "title": title or content[:50] + "..." if content else "",
                    "source": source,
                    "time": time,
                    "content": content or title,
                    "raw": title + (" " + content if content else ""),
                })

    return results


def extract_metadata(text):
    """Extract source and time from a raw news text string."""
    source = ""
    time = ""

    # Common source patterns
    source_patterns = [
        r"(?:来源[:：]\s*)([^\s,，]+)",
        r"(?:据|——)\s*(新华社|央视|人民日报|经济日报|中国证券报|证券时报|财联社|21世纪经济报道|第一财经|每日经济新闻)",
        r"^【([^】]+)】",
        r"\[([^\]]+)\]",
    ]
    for pattern in source_patterns:
        match = re.search(pattern, text)
        if match:
            source = match.group(1).strip()
            break

    # Date patterns
    date_patterns = [
        r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)",
        r"(\d{1,2}月\d{1,2}日)",
        r"(今[日天]|昨[日天]|前[日天])",
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            time = match.group(1).strip()
            break

    # Extract a clean title (first sentence or first 50 chars)
    title = text.split("。")[0].split("\n")[0][:80]
    # Remove source prefix if present
    title = re.sub(r"^【[^】]+】\s*", "", title)
    title = re.sub(r"^\[[^\]]+\]\s*", "", title)

    return {
        "title": title,
        "source": source,
        "time": time,
        "content": text,
        "raw": text,
    }


def main():
    parser = argparse.ArgumentParser(description="解析新闻文件")
    parser.add_argument("--input", required=True, help="输入文件路径 (txt/csv)")
    parser.add_argument("--output", default="parsed_news.json", help="输出 JSON 路径")
    args = parser.parse_args()

    filepath = Path(args.input)
    ext = filepath.suffix.lower()

    if ext == ".csv":
        results = parse_csv(filepath)
    elif ext in (".txt", ".text"):
        results = parse_txt(filepath)
    else:
        print(f"不支持的文件格式: {ext}，支持 .txt 和 .csv")
        sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"解析完成：共 {len(results)} 条新闻 → {args.output}")


if __name__ == "__main__":
    main()
