"""
Převede stažené transktipty na .md soubory vhodné pro RAG.

Výstup: docs/<slug>/<video_id>.md

Spuštění:
    python3 build_rag_docs.py              # všechny kanály
    python3 build_rag_docs.py colemedin    # jen jeden kanál
"""

import re
import sys
from pathlib import Path

CHANNELS = [
    {"name": "Nick Saraev",   "slug": "nicksaraev",  "url": "https://www.youtube.com/@nicksaraev"},
    {"name": "Cole Medin",    "slug": "colemedin",    "url": "https://www.youtube.com/@ColeMedin"},
    {"name": "Greg Isenberg", "slug": "gregisenberg", "url": "https://www.youtube.com/@GregIsenberg"},
]


def parse_transcript(txt_path: Path):
    text = txt_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = video_id = None
    content_start = 0

    for i, line in enumerate(lines):
        if line.startswith("Title: "):
            title = line[len("Title: "):].strip()
        elif line.startswith("Video ID: "):
            video_id = line[len("Video ID: "):].strip()
        elif title and video_id and line.strip() == "":
            content_start = i + 1
            break

    if not title or not video_id:
        return None

    content = " ".join(lines[content_start:]).strip()
    content = re.sub(r" +", " ", content)

    return {"title": title, "video_id": video_id, "content": content}


def to_markdown(doc: dict, channel_name: str, channel_url: str) -> str:
    safe_title = doc["title"].replace('"', '\\"')
    url = f"https://www.youtube.com/watch?v={doc['video_id']}"

    return f"""---
title: "{safe_title}"
video_id: "{doc['video_id']}"
channel: "{channel_name}"
channel_url: "{channel_url}"
url: "{url}"
---

# {doc['title']}

{doc['content']}
"""


def process_channel(channel: dict):
    slug = channel["slug"]
    input_dir  = Path("transcripts") / slug
    output_dir = Path("docs") / slug

    if not input_dir.exists():
        print(f"  ✗ transcripts/{slug}/ neexistuje, přeskakuji")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    txt_files = sorted(input_dir.glob("*.txt"))
    ok = skipped = 0

    for txt_path in txt_files:
        doc = parse_transcript(txt_path)
        if not doc:
            skipped += 1
            continue

        out_path = output_dir / f"{doc['video_id']}.md"
        out_path.write_text(to_markdown(doc, channel["name"], channel["url"]), encoding="utf-8")
        ok += 1

    print(f"  {channel['name']}: {ok} .md souborů → docs/{slug}/  (přeskočeno: {skipped})")


def main():
    filter_slug = sys.argv[1] if len(sys.argv) > 1 else None
    channels = [c for c in CHANNELS if not filter_slug or c["slug"] == filter_slug]

    if not channels:
        print(f"Neznámý kanál: {filter_slug}")
        return

    for channel in channels:
        process_channel(channel)


if __name__ == "__main__":
    main()
