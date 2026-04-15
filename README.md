# AI Videos RAG

Dvě knowledge bases dotazovatelné přímo v Claude Code chatu přes MCP server:

- **YouTube transkripty** (RAG) — sémantické vyhledávání přes embeddingy (aktuálně Nick Saraev, 282 videí)
- **articles.md** — kurátorované články z X.com, keyword search podle sekcí

---

## Setup na novém počítači

### 1. Klonuj repo

```bash
git clone https://github.com/lukasv2255/AI-videos-rag.git
cd AI-videos-rag
```

### 2. Nainstaluj závislosti

```bash
pip3 install openai anthropic tiktoken python-frontmatter numpy yt-dlp youtube-transcript-api
pip3 install "mcp[cli]"   # vyžaduje Python 3.11+, jinak: /opt/homebrew/bin/pip3 install "mcp[cli]" --break-system-packages
```

### 3. Vytvoř .env

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Vygeneruj vectors.npy

`metadata.json` je součástí repo (6813 chunků, 282 videí).
Stačí spustit ingest — vygeneruje `vectors.npy` z metadat (~$0.002):

```bash
source .env && python3 ingest.py
```

### 5. Nastav MCP server

Uprav `.mcp.json` — změň cestu na absolutní cestu na tvém počítači:

```json
{
  "mcpServers": {
    "yt-rag": {
      "command": "/bin/bash",
      "args": ["/ABSOLUTNI/CESTA/AI-videos-rag/run_mcp.sh"]
    }
  }
}
```

### 6. Otevři projekt v Claude Code

Otevři složku `AI-videos-rag` v Claude Code desktop.
Potvrď načtení MCP serveru `yt-rag` — server se spustí automaticky.

---

## Jak se ptát

**articles.md** (default — rychlé, žádné API volání):
| Co chceš | Jak se zeptat |
|---|---|
| Téma z článků | *"Co jsou Claude Code Routines?"* |
| Byznys příležitosti | *"Ukaž perspektivní AI byznysy"* |
| Konkrétní info | *"Co je competitor intelligence?"* |

**YouTube transkripty** (pouze když explicitně zmíníš Nicka):
| Co chceš | Jak se zeptat |
|---|---|
| Otázka z videí | *"Co říká Nick o cold emailech?"* |
| Shrnutí videa | *"Shrň video CLAUDE SKILLS FULL COURSE"* |
| Výpis videí | *"Vypiš videa o n8n"* |

**Poznámka:** Pokud MCP říká "video chybí" — nevěřit. Použij `list_videos` nebo `summarize_video` s částí názvu.

---

## Dostupné MCP nástroje

- `search_nick_saraev` — nejrelevantnější úryvky k dotazu
- `ask_nick_saraev` — strukturovaná odpověď z více videí
- `summarize_video` — shrnutí celého konkrétního videa
- `list_videos` — výpis všech videí v databázi

---

## Struktura projektu

```
AI-videos-rag/
├── .env                  # API klíče (není v gitu)
├── .mcp.json             # konfigurace MCP serveru
├── articles.md           # kurátorované články (keyword search)
├── metadata.json         # texty a metadata chunků z transkriptů
├── vectors.npy           # embeddingy (není v gitu, generuje ingest.py)
├── build_rag_docs.py     # převod transkriptů → .md soubory
├── ingest.py             # embedování a ukládání vektorů
├── mcp_server.py         # MCP server se 4 nástroji
├── run_mcp.sh            # wrapper pro spuštění MCP serveru
├── download_transcripts.py  # stahování transkriptů z YouTube
└── query.py              # CLI dotazování (bez MCP)
```
