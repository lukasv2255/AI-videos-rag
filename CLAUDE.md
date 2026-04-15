# AI Videos RAG — projektové instrukce

## Účel projektu
RAG knowledge base z YouTube kanálu Nick Saraev + curated articles.
Dotazování přes MCP server přímo v Claude Code chatu.

## articles.md — klíčové pravidlo

**Trigger:** Kdykoliv pošleš odkaz z `x.com` — automaticky bez ptaní proveď celé workflow níže.

Když mi pošleš odkaz na článek, tweet nebo jakýkoliv obsah:
1. **Přečti obsah** (přes Chrome MCP nebo WebFetch)
2. **Extrahuj klíčové informace** — konkrétní fakta, ceny, use-casy, insights
3. **Zkontroluj jestli téma už v articles.md existuje:**
   - Pokud ano → **rozšiř existující sekci** o nové informace
   - Pokud ne → **appenduj novou sekci** s nadpisem `## Název tématu`
4. **Pošli podrobné shrnutí do chatu** — co bylo přidáno/rozšířeno v articles.md.
   Formát shrnutí v chatu:
   - Název sekce a zda jde o novou sekci nebo rozšíření existující
   - Všechny klíčové body které byly přidány (kompletní, ne zkrácené)
   - Co z obsahu bylo vynecháno a proč (reklamy, opakování, irelevantní části)
5. **Ulož a pushni** na GitHub

### Formát nové sekce
```markdown
## Název tématu

*Zdroj: autor/název, datum — https://x.com/...*

Stručný úvod co téma řeší.

**Klíčový bod 1**
Detail...

**Klíčový bod 2**
Detail...
```

**Pravidlo:** Řádek `*Zdroj:*` musí vždy obsahovat plný URL odkaz na originální článek/tweet.

### Proč strukturovaně
Nad articles.md se dotazuji přes MCP (`ask_nick_saraev` + articles citace).
Dotazy mohou být konkrétní ("co je competitor intelligence") nebo obecné
("ukaž perspektivní AI byznys modely") — sekce musí být dohledatelné podle tématu.

## Dotazování — kdy použít co

- **Defaultně:** čti přímo `articles.md` — rychlejší, žádné API volání
- **`ask_nick_saraev`:** pouze když uživatel explicitně zmíní Nicka ("co říká Nick", "podle Nicka", "z videí" apod.)

## MCP server
- Soubory: `mcp_server.py`, `run_mcp.sh`, `.mcp.json`
- Vektory: `vectors.npy` (není v gitu), `metadata.json` (je v gitu)
- Restart po změně `mcp_server.py`: zavři a otevři Claude Code

## Důležité
- `.env` nikdy do gitu
- `vectors.npy` nikdy do gitu (40 MB, generuje se z `metadata.json`)
