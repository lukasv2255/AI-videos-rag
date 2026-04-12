"""
CLI pro dotazování RAG knowledge base z YouTube transkriptů.

Použití:
    python3 query.py                  # interaktivní režim
    python3 query.py "tvá otázka"     # jednorázový dotaz

Dva režimy:
    /search <dotaz>   → vrátí nejrelevantnější úryvky bez LLM (rychlé, levné)
    /ask <dotaz>      → Claude syntetizuje odpověď z nalezených chunků
    nebo jen napiš otázku → automaticky /ask
"""

import os
import sys
import textwrap

import chromadb
from openai import OpenAI
import anthropic

# ── Konfigurace ────────────────────────────────────────────────────────────
CHROMA_DIR   = "chroma_db"
COLLECTION   = "nicksaraev"
EMBED_MODEL  = "text-embedding-3-small"
TOP_K        = 6      # kolik chunků vytáhnout
MAX_CONTEXT  = 4000   # max tokenů kontextu pro LLM

client_oai     = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
client_claude  = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
client_chroma  = chromadb.PersistentClient(path=CHROMA_DIR)
collection     = client_chroma.get_or_create_collection(COLLECTION)

SYSTEM_PROMPT = """Jsi asistent pro odpovídání na otázky o obsahu YouTube kanálu Nick Saraev.
Odpovídej výhradně na základě poskytnutých úryvků z transkriptů.
Pokud odpověď v úryvcích není, řekni to přímo.
Cituj konkrétní videa když je to relevantní (uveď název videa).
Odpovídej v jazyce, ve kterém je položena otázka."""


# ── Vyhledávání ────────────────────────────────────────────────────────────

def search(query: str, k: int = TOP_K) -> list[dict]:
    """
    Převede otázku na embedding a najde nejpodobnější chunky v ChromaDB.

    Proč embedding dotazu? Sémantické hledání funguje tak, že věty
    s podobným významem mají podobné vektory — i když nesdílí stejná slova.
    """
    vector = client_oai.embeddings.create(
        model=EMBED_MODEL,
        input=[query]
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text":     doc,
            "title":    meta["title"],
            "url":      meta["url"],
            "score":    round(1 - dist, 3),   # cosine similarity (1 = identické)
        })
    return hits


# ── Výpis výsledků ─────────────────────────────────────────────────────────

def print_hits(hits: list[dict]):
    for i, h in enumerate(hits, 1):
        score_bar = "█" * int(h["score"] * 20)
        print(f"\n[{i}] {h['title']}")
        print(f"    Relevance: {score_bar} {h['score']}")
        print(f"    URL: {h['url']}")
        print(f"    {textwrap.fill(h['text'][:300] + '...', width=80, subsequent_indent='    ')}")


# ── Generování odpovědi ────────────────────────────────────────────────────

def ask(query: str, hits: list[dict]) -> str:
    """
    Pošle otázku + nalezené chunky do Clauda.

    RAG princip: místo aby LLM odpovídal z paměti (může halucinovat),
    dostane konkrétní úryvky jako kontext a odpovídá jen z nich.
    """
    context_parts = []
    char_budget = MAX_CONTEXT * 4  # přibližně 4 znaky na token

    for h in hits:
        chunk_text = f"[{h['title']}]\n{h['text']}\nZdroj: {h['url']}"
        if len("\n\n".join(context_parts)) + len(chunk_text) > char_budget:
            break
        context_parts.append(chunk_text)

    context = "\n\n---\n\n".join(context_parts)

    message = client_claude.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Kontext z transkriptů:\n\n{context}\n\n---\n\nOtázka: {query}"
        }]
    )
    return message.content[0].text


# ── CLI ────────────────────────────────────────────────────────────────────

def run(query: str, mode: str = "ask"):
    print(f"\n🔍 Hledám: {query}\n")
    hits = search(query)

    if mode == "search" or not hits:
        print_hits(hits)
        return

    # Vždy ukaž zdroje
    print("Zdroje:")
    for i, h in enumerate(hits, 1):
        print(f"  [{i}] {h['title']} (score: {h['score']}) — {h['url']}")

    print("\n💬 Odpověď:\n")
    answer = ask(query, hits)
    print(textwrap.fill(answer, width=80))


def main():
    # Jednorázový dotaz přes argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        run(query)
        return

    # Interaktivní režim
    print("RAG Knowledge Base — Nick Saraev")
    print("Příkazy: /search <dotaz>  |  /ask <dotaz>  |  /quit")
    print("Nebo jen napiš otázku (= /ask)\n")

    while True:
        try:
            raw = input("▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNahledanou.")
            break

        if not raw:
            continue
        if raw in ("/quit", "/exit", "quit", "exit"):
            break
        elif raw.startswith("/search "):
            run(raw[8:].strip(), mode="search")
        elif raw.startswith("/ask "):
            run(raw[5:].strip(), mode="ask")
        else:
            run(raw, mode="ask")


if __name__ == "__main__":
    main()
