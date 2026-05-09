#!/usr/bin/env python3
"""
Vygeneruje Twitter posty / thready pro témata v `twitter/*.md`.

Použití:
  source .env
  /opt/homebrew/bin/python3 scripts/generate_twitter_threads.py --file twitter/10_trendy_budoucnost.md --start 91 --limit 1

Výstup:
  twitter/generated/<slug>/<NN>_<slug-topic>.md
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
TWITTER_DIR = BASE_DIR / "twitter"
OUT_DIR = TWITTER_DIR / "generated"


def _slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_-]+", "_", s, flags=re.UNICODE).strip("_")
    return s[:80] or "tema"


def _parse_topics(md_path: Path) -> list[tuple[int, str]]:
    topics: list[tuple[int, str]] = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.*\S)\s*$", line)
        if not m:
            continue
        topics.append((int(m.group(1)), m.group(2)))
    return topics


def _render_thread_from_rag(topic_title: str) -> str:
    # Import až tady, aby šel skript aspoň načíst bez heavy deps.
    # `src/` není Python package, takže načteme přímo soubor `src/mcp_server.py`.
    import importlib.util

    mcp_path = BASE_DIR / "src" / "mcp_server.py"
    spec = importlib.util.spec_from_file_location("mcp_server", mcp_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Nelze načíst modul: {mcp_path}")
    mcp_server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mcp_server)  # type: ignore[attr-defined]

    question = topic_title

    hits = mcp_server._search(question, k=8)  # type: ignore[attr-defined]
    context_parts = []
    for h in hits:
        context_parts.append(
            "[{title}]\n{text}\nZdroj: {url}".format(
                title=h["title"], text=h["text"], url=h["url"]
            )
        )
    context = "\n\n---\n\n".join(context_parts)

    prompt = (
        "Na základě těchto úryvků z AI YouTube videí napiš Twitter výstup v češtině.\n\n"
        "Cíl: praktický, konkrétní, bez hype.\n"
        "Forma: thread 5–7 tweetů.\n\n"
        "Tvrdá pravidla:\n"
        "- každý tweet max 260 znaků\n"
        "- piš opatrně: žádné extrémní tvrzení, žádné absolutní predikce, žádné \"exploduje\"\n"
        "- nepoužívej žádná čísla ani procenta (kromě číslování tweetů typu 1/6)\n"
        "- nepoužívej ceny, velikosti trhu ani časové predikce, pokud nejsou EXPLICITNĚ v úryvcích\n"
        "- žádné značky/produkty, pokud nejsou v úryvcích\n"
        "- když něco v úryvcích není, vynech to nebo formuluj jako nejistou hypotézu\n"
        "- nepoužívej anglická slova ani jiné abecedy; jen čeština\n\n"
        "Formát výstupu:\n"
        "- pouze čistý text, žádný Markdown\n"
        "- každý tweet na samostatném řádku\n"
        "- číslování přesně ve tvaru \"1/6 \", \"2/6 \" ... (počet si sám zvol a dodrž)\n\n"
        "Struktura:\n"
        "- 1. tweet: hook + teze\n"
        "- 2.–(n-1). tweet: 1 pointa + 1 praktická implikace\n"
        "- poslední tweet: checklist \"Co dělat teď\" (3–5 krátkých bodů) + 1 otázka\n\n"
        "Úryvky:\n"
        "{context}\n\n"
        "Téma: {question}\n"
    ).format(context=context, question=question)

    resp = mcp_server.client_claude.messages.create(  # type: ignore[attr-defined]
        model="claude-haiku-4-5",
        max_tokens=1200,
        system=(
            "Jsi seniorní copywriter pro Twitter/X zaměřený na AI a praktické workflow. "
            "Píšeš česky, stručně, konkrétně. "
            "Držíš se poskytnutých úryvků a nepřidáváš nepodložená tvrzení."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()

    # Sanitizace: občas proklouzne jiná abeceda (cyrilice apod.). Bezpečně vyhoď.
    cleaned_chars: list[str] = []
    for ch in raw:
        if ch == "\n":
            cleaned_chars.append(ch)
            continue
        cat = unicodedata.category(ch)
        if cat.startswith("C"):  # control/surrogates
            continue
        name = unicodedata.name(ch, "")
        if "CYRILLIC" in name or "ARABIC" in name or "HEBREW" in name or "GREEK" in name:
            continue
        cleaned_chars.append(ch)
    return "".join(cleaned_chars).strip()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Např. twitter/10_trendy_budoucnost.md")
    parser.add_argument("--start", type=int, default=1, help="Od jakého čísla tématu začít (včetně)")
    parser.add_argument("--limit", type=int, default=0, help="Kolik témat vygenerovat (0 = všechna)")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Pokud výstupní soubor existuje, přeskoč (nepřepisuj).",
    )
    args = parser.parse_args(argv)

    md_path = (BASE_DIR / args.file).resolve()
    if not md_path.exists():
        print(f"Soubor neexistuje: {md_path}", file=sys.stderr)
        return 2
    if not str(md_path).startswith(str(TWITTER_DIR) + "/"):
        print("Bezpečnost: --file musí být v adresáři twitter/", file=sys.stderr)
        return 2

    topics = [(n, t) for (n, t) in _parse_topics(md_path) if n >= args.start]
    if args.limit and args.limit > 0:
        topics = topics[: args.limit]

    if not topics:
        print("Žádná témata k vygenerování.", file=sys.stderr)
        return 1

    theme_slug = _slugify(md_path.stem)
    theme_out_dir = OUT_DIR / theme_slug
    theme_out_dir.mkdir(parents=True, exist_ok=True)

    for n, title in topics:
        out_path = theme_out_dir / f"{n:03d}_{_slugify(title)}.md"
        if args.skip_existing and out_path.exists():
            print(f"SKIP: {out_path}")
            continue
        thread = _render_thread_from_rag(title)
        content = (
            f"# {n}. {title}\n\n"
            f"Zdroj tématu: {md_path.name}\n\n"
            f"---\n\n"
            f"{thread}\n"
        )
        out_path.write_text(content, encoding="utf-8")
        print(f"OK: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
