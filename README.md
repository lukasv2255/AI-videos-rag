# AI Videos RAG

RAG knowledge base z AI YouTube kanálů + kurátorované články. Dotazování přes MCP přímo v Claude Code.

**Kanály:** Nick Saraev (283 videí), Cole Medin (181), Greg Isenberg (408) — celkem 866 videí, 15 801 chunků

---

## Použití

### Přidání článků z X.com

Vlož odkaz (nebo více najednou) do chatu — Claude automaticky přečte, extrahuje a appenduje do `articles.md`, pak pushne na GitHub.

```
https://x.com/foo/status/123
https://x.com/bar/status/456
```

### Dotazování

Zpráva začínající `ask` → Claude zavolá MCP nástroje:

```
ask co jsou Claude Code Routines
ask perspektivní AI byznysy
ask co říkají o cold emailech
```

Bez `ask` → Claude čte `articles.md` přímo (rychlejší, bez API volání).

---

## Struktura

```
AI-videos-rag/
├── src/
│   ├── mcp_server.py        # MCP server — 5 nástrojů (ask_ai_videos, search_articles, ...)
│   ├── ingest.py            # embedování docs/*.md → vectors.npy + metadata.json
│   ├── build_rag_docs.py    # transcripts/*.txt → docs/*.md
│   └── query.py             # CLI dotazování bez MCP
├── scripts/
│   ├── download_transcripts.py  # stahování transkriptů z YouTube (yt-dlp)
│   ├── run_mcp.sh           # spouštěcí wrapper pro MCP server
│   └── watchdog.sh          # hlídá download_transcripts.py, restartuje při pádu
├── tasks/
│   ├── lessons.md           # poučení z předchozích session
│   └── roadmap.md           # co je hotovo, co chybí
├── articles.md              # kurátorované články (keyword search)
├── metadata.json            # texty a metadata chunků (je v gitu)
├── vectors.npy              # embeddingy (není v gitu, generuje ingest.py)
├── .env                     # API klíče (není v gitu)
├── .env.example             # šablona
└── .mcp.json                # konfigurace MCP serveru (není v gitu)
```

---

## Pipeline pro nový kanál

```bash
# 1. Přidej kanál do CHANNELS v scripts/download_transcripts.py a src/build_rag_docs.py
# 2. Stáhni transkripty
python3 scripts/download_transcripts.py >> download.log 2>&1 &

# 3. Převeď na .md
python3 src/build_rag_docs.py <slug>

# 4. Embed
source .env && python3 src/ingest.py

# 5. Restart Claude Code (MCP načte nové vektory)
```

---

## Setup na novém počítači

```bash
git clone https://github.com/lukasv2255/AI-videos-rag.git
cd AI-videos-rag
pip3 install openai anthropic tiktoken python-frontmatter numpy yt-dlp youtube-transcript-api "mcp[cli]"
cp .env.example .env   # doplň API klíče
source .env && python3 src/ingest.py   # vygeneruje vectors.npy (~$0.01)
```

`.mcp.json` — nastav absolutní cestu k `scripts/run_mcp.sh`, pak otevři projekt v Claude Code.
