# Kompletní průvodce Claude ekosystémem — skills, agenti, MCP, workflow, byznys

---

## 1. Claude Skills — co to jsou a jak fungují

**Co je skill:**
Skill je složka obsahující `SKILL.md` (povinný) — instrukce v Markdown s YAML frontmatter — a volitelně `scripts/`, `references/`, `assets/`. Je to sada instrukcí, která učí Clauda jak zacházet se specifickými úkoly nebo workflow. Místo opakovaného vysvětlování preferencí v každém chatu naučíš Clauda jednou a těžíš pokaždé.

**Tři úrovně progressive disclosure:**
- **1. úroveň (YAML frontmatter):** Vždy načtena v system promptu. Dává Claudovi jen tolik informací, aby věděl kdy skill použít.
- **2. úroveň (tělo SKILL.md):** Načtena když Claude uzná skill za relevantní. Obsahuje kompletní instrukce.
- **3. úroveň (linkované soubory):** Další soubory ve složce skillu, které Claude prozkoumá jen podle potřeby.

Toto minimalizuje spotřebu tokenů při zachování specializované expertízy.

**Technické požadavky (kritická pravidla):**
- Soubor musí být pojmenován přesně `SKILL.md` (case-sensitive)
- Složka skillu musí být v kebab-case: `notion-project-setup` ✅, `Notion Project Setup` ❌
- Žádný `README.md` uvnitř složky skillu
- YAML frontmatter musí obsahovat povinná pole `name` a `description`
- `description` musí obsahovat OBOJÍ: co skill dělá + kdy ho použít (trigger podmínky), max 1024 znaků, bez XML tagů
- Zakázáno: XML závorky `< >`, názvy obsahující "claude" nebo "anthropic"

**Příklad dobré vs. špatné description:**
```yaml
# Dobré
description: Analyzes Figma design files and generates developer handoff 
documentation. Use when user uploads .fig files, asks for "design specs", 
"component documentation", or "design-to-code handoff".

# Špatné
description: Helps with projects.
```

**Tři kategorie skillů (dle Anthropic):**
1. **Document & Asset Creation** — tvorba dokumentů, prezentací, designů, kódu. Využívá vestavěné schopnosti Clauda, žádné externí nástroje nepotřebuje.
2. **Workflow Automation** — vícekrokové procesy s konzistentní metodologií, koordinace přes více MCP serverů.
3. **MCP Enhancement** — workflow guidance jako nadstavba nad přístupem k nástrojům. Příklad: Sentry skill, který automaticky analyzuje a opravuje bugy v GitHub PR pomocí Sentry MCP serveru.

**MCP vs. Skills — kuchyňská analogie:**
- MCP poskytuje profesionální kuchyni: přístup k nástrojům, ingrediencím, vybavení.
- Skills poskytují recepty: krok za krokem jak vytvořit něco hodnotného.

**Distribuce skillů:**
- Upload přes Settings > Capabilities > Skills v Claude.ai, nebo do složky skills v Claude Code
- Skills jsou otevřený standard — fungují identicky přes Claude.ai, Claude Code i API
- Via API: endpoint `/v1/skills`, parametr `container.skills` v Messages API
- Admins mohou nasadit skills workspace-wide (od 18. 12. 2025)

**5 vzorů pro instrukce skillů:**
1. **Sequential workflow orchestration** — explicitní pořadí kroků, závislosti, validace v každé fázi
2. **Multi-MCP coordination** — workflow přes více služeb (Figma → Drive → Linear → Slack)
3. **Iterative refinement** — opakované zlepšování výstupu s validačními skripty
4. **Context-aware tool selection** — stejný výsledek, různé nástroje podle kontextu
5. **Domain-specific intelligence** — specializovaná znalost zabudovaná do logiky (např. finanční compliance)

**9 typů skillů podle Anthropic (Thariq, Anthropic, 17. 3. 2026 — https://x.com/trq212/status/2033949937936085378):**

| Typ | Co řeší | Příklady |
|---|---|---|
| **Library & API Reference** | Správné použití interních nebo problematických knihoven, edge cases, gotchas | `billing-lib`, `internal-platform-cli`, `frontend-design` |
| **Product Verification** | Testování a ověřování kódu, ideálně s Playwright/tmux | `signup-flow-driver`, `checkout-verifier`, `tmux-cli-driver` |
| **Data Fetching & Analysis** | Napojení na datové a monitoring stacky, credentials, dashboard IDs | `funnel-query`, `cohort-compare`, `grafana` |
| **Business Process & Team Automation** | Opakující se workflow jako jeden příkaz, ukládání výsledků do logů | `standup-post`, `create-ticket`, `weekly-recap` |
| **Code Scaffolding & Templates** | Generování boilerplate s natural language požadavky | `new-workflow`, `new-migration`, `create-app` |
| **Code Quality & Review** | Vynucování code style, adversarial review, testing practices | `adversarial-review`, `code-style`, `testing-practices` |
| **CI/CD & Deployment** | Fetch, push, deploy s daty z jiných skillů | `babysit-pr`, `deploy-service`, `cherry-pick-prod` |
| **Runbooks** | Symptom → multi-tool investigation → structured report | `service-debugging`, `oncall-runner`, `log-correlator` |
| **Infrastructure Operations** | Routine maintenance s guardrails pro destruktivní akce | `resource-orphans`, `dependency-management`, `cost-investigation` |

**Nejdůležitější tipy pro psaní skillů (od Anthropic):**
- **Gotchas sekce** — nejvyšší-signal obsah v jakémkoliv skillu. Buduj ji průběžně z reálných failure points.
- **Skill je složka, ne soubor** — využij filesystem jako progressive disclosure: `references/api.md`, `assets/template.md`, `scripts/helper.py`
- **Description je pro model** — Claude scanuje descriptions aby rozhodl "je tu skill pro tento request?". Piš trigger podmínky, ne shrnutí.
- **Nerailroad Clauda** — dej mu info, ale flexibilitu adaptovat se. Příliš specifické instrukce v reusable skillu = problém.
- **Setup config** — pro skilly vyžadující konfiguraci (Slack kanál, složka...) ukládej do `config.json` ve složce skillu. Pokud chybí, Claude se zeptá.
- **Paměť** — skilly mohou ukládat data do `${CLAUDE_PLUGIN_DATA}` (stabilní složka přes upgrady). Např. `standups.log` pro kontext minulých standupů.
- **On-demand hooks** — skilly mohou registrovat hooks platné jen pro danou session. Příklady: `/careful` (blokuje rm -rf, DROP TABLE, force-push), `/freeze` (blokuje edity mimo konkrétní složku).
- **Měření** — PreToolUse hook pro logování skill usage = víš které skilly jsou populární nebo undertriggerují.

**Distribuce v týmu:**
- Malý tým: `./.claude/skills/` v repozitáři
- Velký tým: interní plugin marketplace (GitHub sandbox → PR do marketplace po získání trakce)
- Skilly mohou záviset na jiných skilly — odkazuj je jménem, model je zavolá pokud jsou nainstalované

**Skill Graphs — sítě propojených skillů** (@arscontexta, 18. 2. 2026 — https://x.com/arscontexta/status/2023957499183829467):

Jeden SKILL.md nestačí pro komplexní domény. Skill graph = síť skill souborů propojených wikilinky. Každý soubor je jedna kompletní myšlenka, technika nebo skill.

Jak funguje:
- Každý node má YAML description → agent skenuje bez čtení celého souboru
- Wikilinky jsou vetkaná do prózy (nesou kontext, ne jen referenci)
- MOCs (Maps of Content) organizují sub-témata pro navigaci
- Progressive disclosure: index → descriptions → links → sekce → plný obsah

Příklady skill grafů: trading (risk management, market psychology, position sizing...), legal (contract patterns, compliance, jurisdiction...), company onboarding (org struktura, procesy, kultura, competitive landscape).

Plugin `arscontexta` (249 souborů) je skill graph pro budování knowledge bases — nainstaluj, spusť `/learn` a `/reduce`.

**Skills — failure modes a testování** (@hooeem, 11. 3. 2026 — https://x.com/hooeem/status/2031755971265974632):

5 failure modes:
1. **Silent Skill** (nikdy se nespustí) — YAML description příliš slabá. Fix: přidej trigger phrases, buď explicitní.
2. **Hijacker** (spustí se na špatné requesty) — description příliš broad nebo chybí negative boundaries. Fix: přidej "Do NOT use for [jiné tasky]".
3. **Drifter** (spustí se správně, špatný output) — ambiguózní instrukce. Fix: nahraď vágní jazyk konkrétním ("Format nicely" → "Use H2 headings, bold first sentence, max 3 lines/paragraph").
4. **Fragile Skill** (funguje na clean input, padá na edge cases) — chybí edge case instrukce. Fix: "If [condition], then [specific action]."
5. **Overachiever** (přidává co nikdo nechce) — chybí scope constraints. Fix: "Output ONLY [specified format] and nothing else."

State management přes session:
Přidej do SKILL.md: *"At the start of every session, read context-log.md. At the end, write summary of what finished and what's pending."* → Claude čte vlastní poznámky z předchozí session.

Skills 2.0 testování: Evals (Pass/Fail pro konkrétní test prompts), Benchmarks (pass rate, token cost, speed), A/B Comparator (slepý test dvou verzí instrukcí), Description Optimiser.

---

## 2. LLM Knowledge Base — Karpathyho metoda

*Zdroj rozšíření: @polydao na X, 9. 4. 2026 — https://x.com/polydao/status/2042203352054771748*

**Základní myšlenka (Andrej Karpathy, ex-OpenAI/Tesla):**
Většina AI nástrojů funguje jako RAG: nahraješ soubory, LLM při každém dotazu od nuly hledá relevantní části. Karpathyho přístup je jiný — LLM postupně buduje a udržuje persistentní wiki z markdown souborů, která sedí mezi tebou a surovými zdroji. Znalost se kompiluje jednou a průběžně aktualizuje, ne znovu odvozuje při každém dotazu.

Mentální posun: **LLM jako kompilátor a knihovník — ne chatbot.**

**Tři vrstvy systému:**
- **Raw sources** (`raw/`) — tvoje kurátorované zdrojové dokumenty. Neměnné, LLM z nich pouze čte.
- **Wiki** (`wiki/`) — LLM-generované markdown soubory. Souhrny, entity stránky, koncepty, porovnání. LLM tuto vrstvu vlastní celou.
- **Reports** (`reports/`) — výstupy: odpovědi na dotazy, eseje, slide decky. Každý dotaz se ukládá jako permanentní asset.

**6-krokový workflow**

1. **Capture** — Obsidian Web Clipper ukládá libovolnou webovou stránku do `raw/` jako .md s URL, titulkem a datem. Neorganizuj, jen ukládej.
2. **Compile** — LLM skenuje `raw/` a vytváří/aktualizuje stránky v `wiki/`. Každý koncept = vlastní .md soubor s definicí, zdroji a backlinky.
3. **Navigate** — Obsidian graph view ukazuje clustery znalostí a izolované uzly (= mezery které ještě nemáš).
4. **Query** — místo "Explain X" v stateless chatu: *"Using only my wiki, explain X based on everything I've researched."* LLM čte wiki a zapíše odpověď do `reports/`.
5. **Answer in files, not chat** — klíčový návyk: každá odpověď jde do souboru, ne do chatu. Výstupy: Markdown report, Marp slide deck (.md → prezentace), PNG diagramy.
6. **Health check** — LLM periodicky skenuje wiki na: kontradikce, entities bez vlastní stránky, duplikáty, nesourcované claims, nové kandidáty na články.

**Tři operace (zkráceno):**
- **Ingest** → jeden zdroj může ovlivnit 10–15 wiki stránek
- **Query** → odpovědi se ukládají zpět jako nové wiki stránky
- **Lint** → weekly health check příkazem

**Obsidian — proč právě on:**
- Backlinks — všude kde je koncept zmíněn
- Graph view — vizuální mapa znalostí, vidíš mezery
- Dataview plugin — dotazování poznámek jako databáze
- Marp plugin — .md soubor přímo jako prezentace

**Praktické nastavení (víkendový MVP):**
- **Den 1:** Obsidian + vault (`raw/`, `wiki/`, `reports/`) + Web Clipper + 20–30 naklipen článků na jedno téma
- **Den 2:** Skill `/kb-compile` → wiki stránky → graph view → Skill `/kb-report` → první dotaz

**Proč lepší než stateless "New Chat":**
- Dnešní odpověď se stává zítřejším kontextem
- Tvá terminologie a frameworky se stávají kanonickými wiki stránkami
- 6 měsíců práce = privátní korpus, který model dokáže číst v jednom context window

**Privátní/offline varianta:** Obsidian + Ollama (lokální LLM) — nic neopouští tvůj počítač. Claude Code se přidá jen pro konkrétní tasky kde cloud model dává smysl.

**Advanced — finetuning z wiki:**
Až wiki dosáhne dostatečné velikosti, lze ji použít jako finetuning korpus — znalost se "zapeče" přímo do vah modelu. Pro tým: interní docs, API historie, design decisions → finetuned org assistant.

**Obsidian MCP integrace:**
MCP server pro Obsidian (3 300+ hvězd na GitHubu) — Claude čte a zapisuje přímo do vaultu v reálném čase.

Dostupné nástroje: `list_files_in_vault`, `get_file_contents`, `search`, `patch_content` (vloží pod konkrétní heading), `append_content`, `delete_file`.

Setup (3 kroky):
1. Obsidian → Community Plugins → "Local REST API" → install → zkopíruj API key
2. Otevři `~/Library/Application Support/Claude/claude_desktop_config.json`
3. Přidej MCP blok s hostem `127.0.0.1:27124` a API key → restart Claude

Příklady promptů:
- *"Find all notes mentioning Polymarket and give me a short summary of each"*
- *"Take my last meeting note and create summary.md I can send by email"*
- *"Add this idea to my research note under the #Ideas heading"*

**Nepotřebuješ Obsidian** (@coreyganim, 6. 4. 2026 — https://x.com/coreyganim/status/2041144598446092411):
Složka .md souborů + dobrý schema soubor překoná fancy tool stack v 90 % případů. Základní setup:
- `raw/` — sem padá vše, neorganizuj
- `wiki/` — LLM to vlastní celé
- `outputs/` — odpovědi a reporty

CLAUDE.md template (schema soubor):
```markdown
# Knowledge Base Schema
## What This Is
A personal knowledge base about [YOUR TOPIC].
## How It's Organized
- raw/ contains unprocessed source material. Never modify these files.
- wiki/ contains the organized wiki. AI maintains this entirely.
- outputs/ contains generated reports and answers.
## Wiki Rules
- Every topic gets its own .md file in wiki/
- Every wiki file starts with a one-paragraph summary
- Link related topics using [[topic-name]] format
- Maintain an INDEX.md that lists every topic
## My Interests
[List 3-5 things you want this KB to focus on]
```

Compounding loop: jednou za měsíc řekni: *"Review the entire wiki/. Flag contradictions, find topics mentioned but never explained, suggest 3 new articles."*

---

## 3. MCP (Model Context Protocol) — co to je a jak funguje

**Problém který MCP řeší:**
AI asistent může psát, vysvětlovat a plánovat — ale nemá přístup k tvým systémům. MCP standardizuje toto propojení. Je to pro AI nástroje to, co HTTP je pro web.

**Tři aktéři:**
- **Host** — aplikace (Claude Desktop, IDE). Obsahuje AI model i MCP klienta.
- **MCP Client** — spravuje spojení s MCP servery.
- **MCP Server** — lightweight proces který ty napíšeš, vystavuje capabilities přes JSON-RPC.

Klíčový mentální model: AI model → MCP klient → server → databáze. Nikdy přímý přístup.

**Tři primitiva MCP:**
- **Tools** — akce s vedlejšími efekty (odeslat email, spustit query)
- **Resources** — read-only data identifikovaná URI
- **Prompts** — znovupoužitelné prompt šablony s dynamickými argumenty

**Dvě transportní vrstvy:**
- **stdio** — lokální vývoj, child process
- **HTTP + SSE** — remote servery, web deployments

**35 MCP serverů které stojí za instalaci:**

| Kategorie | Server | Co dělá | Cena |
|---|---|---|---|
| Search | Tavily | AI-optimized web search | Free 1000/měs |
| Search | Exa | Sémantické vyhledávání | Free 1000/měs |
| Search | Context7 | Live dokumentace frameworků | Zdarma |
| Scraping | Firecrawl | URL → čistý markdown | Free 500 kreditů |
| Scraping | Apify | 3000+ hotových scraperů | Free $5 kredity |
| Scraping | Crawl4AI | 61k GitHub stars | Zdarma |
| Browser | Playwright | Claude ovládá Chrome | Zdarma |
| Dev | GitHub | PR, issues, code search | S GitHub účtem |
| Dev | Linear | Issue tracking | Free tier |
| Dev | Sentry | Produkční chyby v kontextu | Free 5K chyb/měs |
| Dev | Vercel | Deploy, build logy | Free tier |
| Dev | Jira | JQL search, sprint mgmt | Free 10 users |
| DB | Supabase | Postgres + auth + storage | Free tier |
| DB | PostgreSQL | Natural language queries | Zdarma |
| DB | MongoDB | 40+ nástrojů | Free 512MB |
| DB | Neo4j | Graph database | Community free |
| Vector | Pinecone | Cloud vector search | Free 2GB |
| Vector | Qdrant | Sémantická paměť | Zdarma |
| Vector | Chroma | Lokální prototyping | Zdarma |
| Vector | Memory MCP | Knowledge graph paměť | Zdarma |
| Produktivita | Notion | Dokumenty a wikis | Free tier |
| Produktivita | Slack | Čtení a posílání zpráv | S workspace |
| Produktivita | Todoist | Task management | Free tier |
| Produktivita | Zapier | Automatizace 6000+ appů | Free 100 tasks/měs |
| Byznys | Stripe | Platby a předplatné | Test mode zdarma |
| Byznys | HubSpot | CRM | Free CRM |
| Design | Figma | Design soubory → kód | S Figma účtem |
| Design | Bannerbear | Automatická tvorba bannerů | Free 30 imgs/měs |
| Infra | Cloudflare | Workers, KV, D1, DNS | Free tier |
| Infra | Docker | Container management | Zdarma |
| Infra | Grafana | Dashboard metriky a alerty | Grafana Cloud |
| Monitoring | Sentry | Produkční chyby | Free tier |

**Doporučené startovní kombinace:**
- Vývojář: GitHub + Sentry + Context7 + Playwright
- Výzkum: Tavily + Firecrawl + Exa
- Řízení projektů: Linear + Slack + Notion
- Byznys: Stripe + HubSpot + Zapier
- Data: Supabase + Firecrawl + Apify

**Praktické pravidlo:** 3–5 serverů je sweet spot — každý přidaný server spotřebovává tokeny na popis nástrojů.

**Jak nainstalovat libovolný MCP server (Claude Code):**
```bash
# Základní instalace
claude mcp add server-name -- npx -y @package/server

# S API klíčem
claude mcp add server-name -e API_KEY=your-key -- npx -y @package/server

# Globálně (všechny projekty)
claude mcp add --scope user server-name -- npx -y @package/server

# Přehled nainstalovaných
claude mcp list
```

*Zdroj: @zodchiii na X, 8. 4. 2026 — https://x.com/zodchiii/status/2041804097628582294*

**Jak postavit vlastní MCP server (TypeScript):**

*Zdroj: @techwith_ram na X, 24. 3. 2026 — https://x.com/techwith_ram/status/2036401174715207817*

Tři primitiva:
- **Tools** — akce s vedlejšími efekty (send email, run query). Mají `name`, `description` (AI čte), JSON schema vstupů.
- **Resources** — read-only data identifikovaná URI (`file:///path`, `db://customers/42`). Statické nebo live.
- **Prompts** — znovupoužitelné prompt šablony s dynamickými argumenty.

Dvě transportní vrstvy:
- **stdio** — lokální vývoj, child process (nejjednodušší, bez portů/auth)
- **HTTP + SSE** — remote servery, multi-user, cloud deployment

Napojení na Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["/absolute/path/to/build/index.js"]
    }
  }
}
```

**Časté chyby při vývoji MCP serveru:**
- `"Server not found"` — cesta v configu musí být absolutní
- `"Tool returned an error"` — přidej try/catch a vrať chybu jako text, ne throw
- stdout pollution — při stdio transportu **nikdy** nepoužívej `console.log` (corrupts stream), používej `console.error`
- Schema mismatch — buď konkrétní v popisu vstupů, AI jinak hádá typy

Debug nástroj: `npx @modelcontextprotocol/inspector` — testuj tool calls bez Claude.

---

## 4. Claude Managed Agents — infrastruktura v cloudu

*Zdroj rozšíření: @NickSpisak_ na X, 8. 4. 2026 — https://x.com/NickSpisak_/status/2041949191887262164*

**Co to je:**
Dosud: stavíš celou infrastrukturu sám (sandboxing, state management, error recovery, credential handling) — měsíce engineeringu. Managed Agents = Anthropic říká: *"My to zvládneme. Ty jen řekni co má agent dělat."*

**4 stavební bloky:**
1. **Agent** — konfigurace: model, system prompt, nástroje + MCP servery. Vytvoříš jednou, znovu použiješ.
2. **Environment** — izolovaný kontejner. Předinstaluj Python, Node.js, Go, libovolné balíčky přes `"packages": {"pip": ["pandas", "numpy"]}`.
3. **Session** — běžící instance agenta, pamatuje si stav, soubory přetrvávají, může běžet hodiny.
4. **Events** — server-sent events: zprávy tam a zpět, agent streamuje responses, tool calls, status updates.

**Deployment za 10 minut (3 API volání):**

```bash
# 1. Instalace CLI
brew install anthropic-cli

# 2. Vytvoř agenta
curl https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -d '{"name": "My Agent", "model": "claude-sonnet-4-6",
       "tools": [{"type": "agent_toolset_20260401"}]}'

# 3. Vytvoř environment
curl https://api.anthropic.com/v1/environments \
  -d '{"name": "dev-env", "config": {"type": "cloud", "networking": {"type": "unrestricted"}}}'
```
`agent_toolset_20260401` aktivuje vše: bash, file read/write, web search, web fetch, grep, glob.

**Systém oprávnění:**
- `always_allow` — automatické spouštění (interní agenti)
- `always_ask` — čeká na schválení každého tool callu (zákaznicky orientované)
- Lze kombinovat: agent automaticky čte soubory, ale čeká na souhlas před bash příkazy
- MCP nástroje defaultně `always_ask` — nový third-party nástroj se nespustí automaticky
- **Výhoda oproti LangGraph/CrewAI/AutoGen:** ty nemají per-tool permission scoping out of the box, zde je to config flag

**Cena:**
- Standardní Claude API token sazby + $0.08/session-hour
- Typická 10minutová session = pár centů

**Příklady co se buduje:**
- Sentry/Seer: klonuje repo → čte kód → píše opravu → otevírá PR
- Rakuten: specialistické agenty pro každé oddělení, nasazení za méně než týden
- Asana AI Teammates: agent pracuje v Asaně vedle lidí
- Data analysis: agent dostane CSV → napíše Python skript → spustí → vrátí insights

**Rychlý start (bez API):**
```
start onboarding for managed agents in Claude API
```
Nebo: `platform.claude.com` → vizuální agent builder → testuj inline → zkopíruj agent ID do kódu.

---

## 5. Advisor Strategy — Opus + Sonnet/Haiku

**Princip:**
Menší model řídí celý úkol (executor) a pouze v momentě kdy narazí na problém volá větší model jako poradce (advisor). Advisor nikdy nevolá nástroje, nikdy neprodukuje user-facing výstup.

**Výsledky benchmarků:**
- Sonnet + Opus advisor: +2.7 p.b. na SWE-bench, náklady nižší o 11.9%
- Haiku + Opus advisor na BrowseComp: 41.2% vs. 19.7% solo (více než dvojnásobek)
- Haiku + Opus advisor vs. Sonnet solo: o 29% nižší skóre, ale o 85% nižší náklady

**Implementace:**
```python
response = client.messages.create(
    model="claude-sonnet-4-6",  # executor
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-6",
            "max_uses": 3,
        },
    ],
    messages=[...]
)
```
Advisor typicky generuje jen 400–700 tokenů (krátký plán). Celkové náklady výrazně pod spuštěním Opusu end-to-end.

---

## 6. Claude Code — klávesové zkratky a workflow

*Zdroj rozšíření: @hanakoxbt na X, 9. 4. 2026 — https://x.com/hanakoxbt/status/2042242394557464896*

**V prohlížeči (claude.ai):**

| Zkratka | Funkce | Proč to záleží |
|---|---|---|
| `Cmd/Ctrl+K` | Nový chat okamžitě | 4s → 0.3s, 15-20× denně |
| `↑` (šipka nahoru) | Upravit poslední zprávu místo follow-up | **21× méně tokenů** — follow-up: ~10 500 tokenů, edit: ~500 tokenů |
| `Cmd/Ctrl+.` | Zastavit generování okamžitě | Ušetří 500–1 000 tokenů za špatnou odpověď |
| `Cmd/Ctrl+/` | Přepnout/skrýt sidebar | +24% pracovního prostoru (280px zpět) |
| `Cmd/Ctrl+Shift+L` | Přepnout dark/light mode | 6s → 0.2s |
| `Shift+Enter` | Nový řádek bez odeslání | Zabrání náhodným odesláním (4–5× denně) |

**V Claude Code (terminál):**

| Zkratka | Funkce | Proč to záleží |
|---|---|---|
| `Esc Esc` (dvojité) | Rewind na libovolný checkpoint | 4 možnosti: kód+konverzace, jen konverzace, jen kód, shrnutí od checkpointu. Zero-risk experimenty. |
| `Ctrl+R` | Fuzzy search přes celou historii promptů | Hledáš prompt z minulého týdne? 2 klíčová slova → hned |
| `Alt/Option+T` | Přepnout extended thinking per zpráva | Jednoduché dotazy: off. Komplexní architektura: on. Ušetří 3 000+ tokenů na triviálních dotazech. |
| `Ctrl+G` | Otevřít prompt v externím editoru (VS Code, vim…) | Psaní víceřádkového promptu v terminálu: 2 min boje s kurzorem → 30s v editoru |
| `Shift+Tab` | Cyklovat: normal → auto-accept → plan | normal = ptá se na vše, auto-accept = rovnou dělá, plan = ukáže plán bez spuštění |
| `/btw` | Boční otázka bez přerušení úkolu | Ptáš se bez zrušení kontextu — vytvořil Erik Schluntz z Claude Code týmu |

**Celkové čísla (naměřeno týden před/po):**
- Před: 51 min/den na klikání, navigaci, čekání, přeposílání
- Po: 22 min/den
- Úspora: **29 minut denně = ~120 hodin ročně** (3 celé pracovní týdny)
- Token úspora z editace, stopování a thinking toggle: ~35%

Všechny zkratky ověříš sám přes `Cmd+?` (Mac) nebo `Ctrl+?` (Windows) v libovolném chatu.

---

## 7. Claude Code Hooks — automatické akce

**Proč lepší než CLAUDE.md:** CLAUDE.md je suggestion (~80% úspěšnost). Hooks jsou automatické akce pokaždé, bez výjimky.

**Dva hlavní typy:**
- `PreToolUse` — před akcí. Exit code 2 = blokovat + poslat chybovou zprávu Claudovi.
- `PostToolUse` — po akci. Pro cleanup, formátování, testy, logování.

**8 praktických hooků:**

1. **Auto-formátování** — Prettier po každém Write/Edit
2. **Blokování nebezpečných příkazů** — `rm -rf`, `git reset --hard`, `DROP TABLE`, `curl | sh`
3. **Ochrana citlivých souborů** — `.env*`, `*.pem`, `*.key`, `secrets/*`
4. **Testy po každé editaci** — Claude vidí výsledky a opravuje hned (2–3× lepší kvalita dle Borise Chernyho)
5. **Blokování PR bez passing testů** — hard gate
6. **Auto-lint** — ESLint s `--fix` po každé editaci
7. **Logování příkazů** — timestampovaný audit trail v `.claude/command-log.txt`
8. **Auto-commit po úkolu** — `Stop` hook → čistá git historie

**Kompletní settings.json:**
```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash", "hooks": [
        {"type": "command", "command": ".claude/hooks/block-dangerous.sh"},
        {"type": "command", "command": ".claude/hooks/log-commands.sh"}
      ]},
      {"matcher": "Edit|Write", "hooks": [
        {"type": "command", "command": ".claude/hooks/protect-files.sh"}
      ]},
      {"matcher": "mcp__github__create_pull_request", "hooks": [
        {"type": "command", "command": ".claude/hooks/require-tests-for-pr.sh"}
      ]}
    ],
    "PostToolUse": [
      {"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write 2>/dev/null; exit 0"},
        {"type": "command", "command": "npx eslint --fix $(jq -r '.tool_input.file_path') 2>&1 | tail -10; exit 0"}
      ]}
    ],
    "Stop": [
      {"matcher": "", "hooks": [
        {"type": "command", "command": ".claude/hooks/auto-commit.sh"}
      ]}
    ]
  }
}
```

---

## 8. Claude Code — Boris Cherny stack (5 vrstev)

**Vrstva 1 — Základ:**
- 5–10 paralelních Claude sessions
- Začínat v plan mode (`Shift+Tab`)
- Auto-accept jakmile je plán solídní
- Aktualizovat `CLAUDE.md` po každé korekci

**Vrstva 2 — Týmová paměť:**
- Sdílené `CLAUDE.md`, týmové hooks, commitovaná oprávnění
- Claude přestane být osobní a stane se týmovou kognitivní vrstvou

**Vrstva 3 — Výstupní styly = kognitivní módy:**
- `Explanatory` → Claude vysvětluje reasoning
- `Learning` → Claude učí při kódování
- `Minimal` → Claude tiše vykonává
- Vlastní agenti: `backend-reviewer`, `migration-guard`, `code-simplifier`

**Vrstva 4 — Native Worktree Parallelism:**
Každý Claude agent: vlastní git worktree + vlastní úkol + vlastní testy + vlastní PR.

**Vrstva 5 — Compound operace:**
- `/simplify` — paralelní code reviewery (duplicitní logika, nested conditionals, špatné queries)
- `/batch` — interaktivní plánování → desítky agentů → paralelní PRs

**Installable skill (všech 42 tipů):**
```bash
mkdir -p ~/.claude/skills/boris
curl -L -o ~/.claude/skills/boris/SKILL.md https://howborisusesclaudecode.com/api/install
```
Pak `/skills boris` — Claude načte celý workflow.

*Zdroj rozšíření: @NainsiDwiv50980 na X, 27. 3. 2026 — https://x.com/NainsiDwiv50980/status/2037558089386430578*

---

## 9. Project Memory System pro Claude Code

**Problém (AI amnézie):**
Claude každou session začíná od nuly. Nepamatuje si proč jsi zvolil framework, jaké bugy jsi opravil, jaká architekturní rozhodnutí padla.

**Řešení:**
```
docs/project_notes/
├── bugs.md       # opravené bugy s root cause a řešením
├── decisions.md  # architekturní rozhodnutí (ADR formát)
├── key_facts.md  # konfigurace, porty, endpointy, tech stack
└── issues.md     # history dokončených úkolů
```

**Jak Claude s pamětí pracuje:**
- Před debuggingem → `bugs.md`
- Před přidáním knihovny → `decisions.md`
- Před odhadnutím konfigurace → `key_facts.md`
- Po dokončení práce → zapíše do `issues.md`

**Compound effect:**
- 1. bug: 1 hodina → 2. výskyt: 10 minut → 3. výskyt: 2 minuty → 4. výskyt: Claude mu předejde

**Konkrétní příklady co memory řeší** (@Suryanshti777, 28. 3. 2026 — https://x.com/Suryanshti777/status/2037921273062506764):

- **Bez decisions.md:** tým používá Tailwind, CSS modules i Chakra UI najednou → chaos. S decisions.md: `ADR-006: Use Tailwind, avoid Chakra/CSS modules` → Claude vynucuje konzistenci automaticky.
- **Bez key_facts.md:** Claude hádá porty, endpointy, env setup → špatné konfigurace. S key_facts.md: `Staging API: api.staging.app.com:8443, DB: PostgreSQL, Auth: Clerk` → Claude přestane hádat.
- **Bez bugs.md:** stejný bug `Connection refused on DB` (root cause: staging port 5433) se řeší znovu. S bugs.md: 45 minut → 2 minuty.

Klíčový princip: bez paměti Claude navrhuje nové knihovny, conflicting patterns, duplicitní závislosti — ne proto že je špatný, ale proto že nemá kontext. Memory mění Claude z chatbota na *learning AI engineer*.

Implementace: čisté markdown soubory, žádný RAG, žádný vector DB, žádné embeddingy. Pod 300 řádků. Obrovský dopad.

---

## 10. Byznys příležitosti — Prediction Markets a AI freelancing

### Prediction Markets infrastruktura

**Klíčová teze:**
Lidé co vydělávají skutečné peníze na Polymarketu nejsou ti s nejlepšími predikcemi. Jsou to ti, kdo prodávají nástroje prediktorům.

**Proč teď:** API otevřené, volume roste ($500M+ na velkých eventech), infrastruktura téměř neexistuje. Crypto-native audience zvyklá platit za SaaS.

**Produktové portfolio:**
- Bot subscriptions: $200–500/měs
- Private tools: $1 000–5 000/měs
- Automation dashboards: $5 000–10 000 setup + monthly
- Institutional solutions: $10 000+/měs

**Matematika:**
- 150 traderů × $300/měs = $540 000/rok
- 5 private clients × $2 000/měs = +$120 000/rok
- 1 institutional client × $10 000/měs = +$120 000/rok
- **Celkem: $780 000/rok** (konzervativní, nulový růst)

### AI Freelancing za $200/hod

**Aktuální tržní sazby:**
- AI agent development: $175–300/hod
- RAG implementace: $150–250/hod
- Obecná LLM integrace: $125–200/hod

**Postup:**

*Fáze 1 — Výběr niche:* Jeden jasně definovaný niche vždy porazí "jsem celkem dobrý v AI obecně". Vysokopoptávkové niche: AI agenti pro SaaS, workflow automation pro professional services, content systems pro marketing, data analysis pro e-commerce, Custom Claude Skills.

*Fáze 2 — Proof (týdny 1–3):* 3 portfolio projekty + pravidelný obsah + min. 1 testimonial.

*Fáze 3 — Cenotvorba:* Start na $150/hod minimum. Pokud AI systém ušetří klientovi 20 hod/měs při $50/hod = $1000 úspora. 20 hodin práce za $150/hod = $3000. Break-even za 3 měsíce.

*Timeline:*
- Měsíc 1: Portfolio + první klient + $3–5K revenue
- Měsíc 3: $175/hod + referraly + $5–8K/měs
- Měsíce 4–6: $200/hod + 3–5 klientů + $8–15K/měs
- Měsíce 6–12: $200+ + inbound leads + $15–25K/měs

---

*Historická analogie:*
Zlatokopecká horečka: prodavači lopat zbohatli, ne horníci. Internetový boom: platební systémy a CDN překonaly většinu webů. Crypto: burzy a infrastrukturní protokoly vydělaly více než většina traderů. Prediction markets jsou další vlna.

**7 AI dovedností co vydělávají peníze v 2026** (@aiedge_, 11. 3. 2026 — https://x.com/aiedge_/status/2031735799994265818):

1. **Tool Stacking & Selection** — znát které AI nástroje použít na jaký task a jak je řetězit (output jednoho → input druhého). Příklad: YouTube transcript → NotebookLM → Claude Skill → Canva. Firmy platí za systémový design, ne za znalost jednoho nástroje.
2. **AI-Powered Research Systems** — autonomní scraping, syntéza a surfování insights. Cíl: raw data → actionable recommendation. X scraper na outlier viral topics → pitch pro content firmy.
3. **AI Media Generation** — faceless content, AI voiceover/avatar/reklamy. Productized workflow: niche + monthly retainer pro content agentury, personal brands, e-commerce.
4. **Coding (vibe coding pro SMB)** — small/medium firmy potřebují custom interní nástroje (dashboardy, client portály, workflow automations). Nemohou si dovolit vývojáře za $10K+, ale zaplatí $1 500–3 000 za funkční nástroj za týden.
5. **Agentic Workflow Design** — multi-step AI agenti (Zapier/MCP/n8n, lead gen agenti, customer service). OpenClaw expert: $2 000–6 000 za setup pro lokální firmy.
6. **Prompt Engineering** — balíček: audit jak tým promptuje + půldenní workshop = okamžitě lepší výstupy. Scalable: kurz, coaching, corporate training.
7. **AI Consulting (meta-skill)** — diagnóza kde AI vytvoří leverage + implementace. $5 000 audit → $10 000–20 000 implementace → $2 000–5 000/měs retainer. Jeden klient = šestimístný byznys.

---

## 6 AI Business Opportunities Nobody Is Building Yet (2027)

*Zdroj: @zephyr_hg na X, 13. 4. 2026 — https://x.com/zephyr_hg/status/2043735668396872188*

Trh je zahlcený AI chatboty a content nástroji. Šest příležitostí, které jsou stále volné — každou lze validovat za víkend.

**1. AI Compliance Monitoring pro malé firmy**
Monitoring regulatorních změn (GDPR, HIPAA, SOC 2, daňové kódy) a automatické upozornění co firma musí udělat. Cena: $300–500/měsíc. Jedno zmeškané deadline = $10 000+ pokuta — ROI se prodá samo.

**2. AI Proposal Writing pro service businesses**
Freelanceři a agentury tráví 3–5 hodin na každém návrhu. Systém vezme brief z konverzace a vygeneruje branded proposal za minuty. Cena: $150–300/měsíc nebo $50 za proposal.

**3. AI Quality Control pro e-commerce produktové listingy**
Miliony e-shopů mají špatné popisy produktů — chybné specs, chybějící atributy, zastaralé SEO. Audit celého katalogu, přepsání a standardizace. Cena: $500–2000 za audit + monthly retainer.

**4. Industry-Specific AI Training Packages**
Generické AI nechápe obor. Právní firma potřebuje AI co mluví case law, nemovitosti zónové předpisy, medicína klinická terminologie. One-time setup $2 000–5 000 + monthly support $200–500. Specialista vydělá 3–5× víc než generalista.

**5. AI Competitor Intelligence pro lokální firmy**
Automatický monitoring konkurence — cenové změny, nové služby, review sentiment, nové kampagne. Weekly intelligence brief. Cena: $200–400/měsíc. Data jsou veřejná (weby, review sites, sociální sítě).

**6. AI Workflow Auditing as a Service**
Firmy začínají používat AI, ale dělají to špatně — různé týmy, různé nástroje, žádná konzistence. Audit všech AI workflow, zpráva co funguje/co je rozbité/co chybí. Cena: $1 500–3 000 za audit. Před 12 měsíci tato služba neexistovala.

**Proč tyto příležitosti existují**
AI jako infrastruktura uvnitř service businessu — nižší startup cost, rychlejší validace, vyšší marže, téměř nulová konkurence. Většina lidí staví produkt/app. Chytřejší je stavět service business poháněný AI.

---

## Claude Code Automatizace — 3-krokový systém

*Zdroj: @noisyb0y1 na X, 13. 4. 2026 — https://x.com/noisyb0y1/status/2043609541477044439*

Google engineer s 11 lety zkušeností automatizoval 80% své práce pomocí Claude Code. Pracuje 2–3 hodiny denně místo 8. Tři kroky, 15–20 minut setup.

**1. Karpathy CLAUDE.md (5 minut)**
Andrej Karpathy zdokumentoval nejčastější chyby LLM při psaní kódu: over-engineering, ignorování existujících patterns, přidávání závislostí které nikdo nežádal. Jeden CLAUDE.md soubor s těmito 4 principy to řeší:

- **Think Before Coding** — zastaví špatné předpoklady a přehlédnuté tradeoffs
- **Simplicity First** — zastaví over-engineering a nafouklé abstrakce
- **Surgical Changes** — zastaví úpravu kódu který nikdo nežádal
- **Goal-Driven Execution** — nejdřív testy, ověřená kritéria úspěchu

Výsledek: porušení konvencí klesá z ~40% na ~3%.

Auto-generování pro jakýkoliv projekt:
```
claude -p "Read the entire project and create a CLAUDE.md based on: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution. Adapt to the real architecture you see." --allowedTools Bash,Write,Read
```

**2. Everything Claude Code (10 minut)**
`github.com/affaan-m/everything-claude-code` — 153 000+ hvězd

Kompletní AI operating system pro vývoj produktů:
- 30+ specializovaných agentů: `planner.md`, `architect.md`, `tdd-guide.md`, `code-reviewer.md`, `security-reviewer.md`, `loop-operator.md`
- 180+ skills: TDD, security, research, content
- AgentShield: 1 282 security testů přímo v konfiguraci
- Funguje na Claude, Codex, Cursor, OpenCode, Gemini

Instalace: `/plugin marketplace add affaan-m/everything-claude-code`

⚠️ Nenačítej vše najednou — 27 agentů + 64 skills současně spálí token limity. Vezmi jen co potřebuješ.

**3. Token fix — downgrade na v2.1.98 (30 sekund)**
Claude Code v2.1.100 tichě krade tokeny:
- v2.1.98: 169 514 bytes → 49 726 tokenů
- v2.1.100: 168 536 bytes → 69 922 tokenů (méně bytes, ale +20 196 tokenů navíc)

Inflace je server-side — nevidíš ji, nemůžeš ji ověřit přes `/context`. Důsledky: CLAUDE.md instrukce se ředí 20K tokeny skrytého obsahu, Claude Max limity hoří 40% rychleji.

Fix: `npx claude-code@2.1.98`

**Case study: jak vypadá plná automatizace**
.NET app + GitLab API + Claude Code, cyklus každých 15 minut:
1. Čte GitLab issues → Claude rozhodne jestli je issue ready pro vývoj
2. Pokud ready → subagent začne pracovat → pushne branch → vytvoří PR
3. PR workflow → kontroluje nové komentáře → implementuje je

Výsledek: z 8h/den kódování na 2–3h review a testování. Kód stejné kvality — vše prochází review.

**Checklist (15–20 minut celkem)**
1. Karpathy CLAUDE.md: `claude -p "Create a CLAUDE.md based on Karpathy's principles for this project" --allowedTools Bash,Write,Read`
2. Everything Claude Code: `/plugin marketplace add affaan-m/everything-claude-code`
3. Token fix: `npx claude-code@2.1.98`

---

## Claude Code Routines — proč poráží n8n a Zapier

*Zdroj: @coreyganim na X, 14. 4. 2026 — https://x.com/coreyganim/status/2044137332920492467*

Claude Code Routines nejsou další automation tool. Je to jiná kategorie: Claude běží na Anthropic cloud infrastruktuře s přístupem k repozitářům, GitHub events a externím nástrojům. Místo předem definované sekvence — přemýšlí a adaptuje se.

**5 věcí co Routines umí a n8n neumí**

- **Reasoning o problému** — PR review routine nečte jen jestli prošly testy. Čte codebase, chápe architekturní patterns, aplikuje reálné review standardy týmu. Drag-and-drop to neumí.
- **Generování a opravy kódu** — když app spadne, routine nealertuje. Klonuje repo, čte error logy, diagnostikuje root cause, napíše fix, otestuje, otevře PR. Ty jen schválíš.
- **Context awareness přes systémy** — Slack zpráva + Linear issue + GitHub changes = Claude čte vše jako kontext, ne jako oddělené kroky.
- **Konfigurace přirozeným jazykem** — neprogramuješ klikáním. Popíšeš úkol v angličtině. "Review every PR for security issues, leave comments, post summary to Slack." Hotovo.
- **Continuous improvement** — když routine nefunguje dobře, řekneš Claudovi co zlepšit. Prompt se adaptuje na dalším runu.

**Kde n8n ještě vyhrává:** jednoduché integrace, 300+ hotových konektorů, vizuální učení.
**Kde Routines vyhrává:** komplexní automatizace, reasoning, edge case handling, generování kódu, vlastní integrace.

**Jak postavit první routine (10–15 minut)**

1. Jdi na `claude.ai/code/routines` → New routine
2. Napiš prompt v angličtině — co má routine dělat (ne kroky, ale výsledek)
3. Přidej GitHub repo a konektory (Slack, atd.)
4. Zvol trigger: schedule / GitHub event / API webhook
5. Klikni Create — sleduj logy, uprav prompt podle výsledku

**Příklad — PR review routine:**
```
You are a code reviewer. When a PR is submitted:
- Read the code changes
- Check for security vulnerabilities and performance issues
- Check alignment with coding standards
- Leave inline comments on specific lines
- Post a summary to Slack
Be thorough but constructive. Focus on issues, not style preferences.
```

**Předpoklady:** Claude Pro nebo vyšší (Routines vyžadují Claude Code on the web).

---

## Claude Power User za 30 dní — framework a byznys

*Zdroj: @cyrilXBT na X, 15. 4. 2026 — https://x.com/cyrilxbt/status/2044240739635179615*

Autor šel za 30 dní od průměrného uživatele Claude k trénování firemních týmů za $1 500–$2 000 za workshop. 14 firem na waitlistu. Žádný technický background.

**Klíčový insight:** Claude je reasoning engine, ne vyhledávač. Výkon je přímo úměrný kvalitě briefu. Naučit se dávat dobrý brief = naučit se nástroj.

**10 dovedností co oddělují power usery**

1. **Role Assignment** — před každým taskem dej Claudovi roli. Samo o sobě zlepší výstup o ~40%.
2. **Constraint Setting** — řekni co nemá dělat stejně jasně jako co má dělat.
3. **Iteration Loops** — nikdy nepřijímej první draft. Jedno konkrétní připomínkové kolo = dramatická změna. Tři kola = výstup co bys sám nenapsal.
4. **Context Preservation** — jeden dlouhý conversation per projekt, ne nový chat pokaždé. Kontext se kumuluje.
5. **Persona Training** — vlož své nejlepší texty, řekni "piš v tomto stylu". Claude zpětně inženýruje tvůj hlas lépe než jakýkoliv brief.
6. **Output Formatting** — vždy specifikuj formát (tabulka, odrážky, odstavce, čísla). Bez toho = nekonzistentní výsledky.
7. **Chain of Thought** — u komplexních tasků řekni "think step by step before answering". Dramaticky snižuje chyby.
8. **Projects and Memory** — Claude Projects = persistentní paměť přes všechny konverzace. Přidej brand voice, audience, klíčové info.
9. **Skill Files** — `skill.md` soubory pro opakující se workflow. Načítají se jen když jsou potřeba → lean context window.
10. **Failure Analysis** — když výstup selže, zeptej se Clauda proč. Řekne ti přesně co šlo špatně. Oprav → updatuj prompt.

**30denní cesta (začínáš od nuly)**

- Dny 1–3: pouze Role Assignment — každý prompt začíná rolí, nic jiného
- Dny 4–7: naučit se iterovat — jeden output, tři kola zpětné vazby
- Dny 8–14: první systém — jeden opakující se task → prompt template
- Dny 15–21: Claude Projects — brand voice, audience, klíčová data
- Dny 22–30: druhý a třetí systém → power user threshold

**Byznys model:** firmy platí za konzistenci, ne za znalost Clauda. Casual uzeři mají náhodné výsledky protože nemají systém. Workshop za půl dne = $1 500, celý den = $2 000.

---

## Secure Agent Sandbox Infrastructure — Browser Use architektura

*Zdroj: @larsencc (Larsen Cundric, Browser Use) na X, 27. 2. 2026 — https://x.com/larsencc/status/2027225210412470668*

Browser Use provozuje miliony web agentů. Článek popisuje jak vyřešili bezpečnostní izolaci agentů co mohou spouštět libovolný kód.

**Problém:** agent co může spouštět kód má přístup ke všemu na stroji — env vars, API klíče, DB credentials, interní služby.

**Dva přístupy k izolaci**

| Pattern | Co se izoluje | Jak funguje |
|---|---|---|
| **Pattern 1 — Isolate the tool** | Nebezpečné operace (code execution) v sandboxu | Agent běží na tvé infrastruktuře, sandbox volá přes HTTP |
| **Pattern 2 — Isolate the agent** | Celý agent v sandboxu | Agent nemá žádná credentials, komunikuje přes control plane |

Browser Use začal s Pattern 1, přešel na Pattern 2.

**Pattern 2 — Implementace**

Sandbox (Unikraft micro-VM v produkci, Docker lokálně) dostane pouze 3 env proměnné:
- `SESSION_TOKEN`
- `CONTROL_PLANE_URL`
- `SESSION_ID`

Žádné AWS klíče, žádné DB credentials, žádné API tokeny.

**Control Plane** je proxy pro vše:
- LLM volání: sandbox pošle nové zprávy → control plane přidá celou historii → pošle do providera
- Soubory: sandbox požádá o presigned S3 URL → nahraje přímo na S3 bez AWS credentials
- Billing a cost caps: control plane vynucuje, sandbox neví

**Bezpečnostní hardening sandboxu:**
1. **Bytecode-only** — Python .py soubory smazány při build, jen .pyc bytecode
2. **Privilege drop** — start jako root (čtení bytecode) → okamžitý drop na `sandbox` user
3. **Env stripping** — SESSION_TOKEN přečten do Python proměnné → smazán z `os.environ`

**Unikraft micro-VM:**
- Boot pod 1 sekundu
- Scale-to-zero: idle VM se suspend, při requestu resume
- Distribuováno přes více metros (AWS)
- Lokálně/evaly: stejný Docker image, stejný entrypoint → "same image everywhere"

**Klíčový závěr:** *"Your agent should have nothing worth stealing and nothing worth preserving."*

Kompromisy: extra network hop na každé operaci, 3 services místo 1. V praxi latence je zanedbatelná vedle LLM response times.

---

## AI Design — proč AI generuje stále stejný design a jak to změnit

*Zdroj: vibecoding.cz, 30. 3. 2026 — https://www.vibecoding.cz/articles/ostatni/proc-ai-generuje-stale-stejny-design-a-jak-to-ve-vasem-projektu-zmenit/*

AI modely konvergují k průměru trénovacích dat — Inter font, modrofialový gradient, card grid, abstraktní hero sekce. Termín pro to: **"AI slop design"**.

**Proč se to děje:**
Komponentové knihovny (Tailwind UI, shadcn/ui, Material Design) dominují trénovacím datům. Model reprodukuje průměr milionu webů = SaaS landing page šablona.

**Nejrychlejší opravy v promptech:**

- **Negativní instrukce fungují lépe než pozitivní** — "žádný card grid", "nepoužívej Inter ani Roboto", "žádný fialovo-modrý gradient" → model respektuje konkrétní zákazy, ignoruje vágní "udělej to originální"
- **Typografie je nejrychlejší páka** — jedna řádka CSS změní charakter celé stránky. Příklady: `Space Grotesk` + `Source Serif Pro`, nebo `DM Serif Display` + `Outfit`
- **Barvy s kontextem** — "tmavě zelená a krémová, skandinávský minimalismus" generuje něco rozpoznatelného; "moderní SaaS paleta" generuje modrofialovou
- **Reálný obsah místo lorem ipsum** — model přizpůsobí layout délce textu
- **Referenční screenshoty jako vstup** — přiložit 2–3 screenshoty webů které se ti líbí + "inspiruj se vizuálním stylem, ale nepoužívej stejné barvy ani layout"
- **Animace s účelem** — max. 3 typy: jedna vstupní sekvence, jeden scroll efekt, jeden hover přechod. Doporučení: Framer Motion

**Design tokeny v CLAUDE.md (trvalé řešení):**
Místo opakování v každém promptu — ulož vizuální identitu do CLAUDE.md jednou:
```markdown
## Design systém
Fonty: DM Serif Display (nadpisy), Outfit (tělo textu)
Barvy: primární #1a4d2e, sekundární #f5f0e8, akcent #d4a574
Border-radius: 0px karty, 4px tlačítka, 8px inputy
Spacing základ: 8px grid
Stín: nepoužívat box-shadow, místo toho border 1px solid #e5e0d8
```

**Nástroje:**

- **Google Stitch** — AI-nativní plátno pro prototypování. "Vibe Design" mód: popíšeš záměr a pocit, ne komponenty. Exportuje `design.md` (design systém jako markdown) + export do Figmy. MCP server pro napojení na Claude Code. Free: 350 generací/měsíc.
- **Pencil.dev** — vizuální plátno přímo v IDE (Cursor, VS Code). Soubory `.pen` = JSON v repozitáři vedle kódu. Agent má plný vizuální kontext přes MCP. Vytvořil Tomáš Krcha (spoluautor Adobe XD). Free.
- **Paper.design** — HTML/CSS canvas (design je rovnou kód). GPU shadery (halftone, liquid metal). MCP server s 24 nástroji. Seed investice $4.2M od Accel.
- **Impeccable** (`npx skills add pbakaus/impeccable`) — skill od autora jQuery UI a Chrome DevTools. Příkazy: `/audit`, `/critique`, `/polish`, `/bolder`, `/quieter`, `/teach-impeccable` (onboarding projektu).

**Co AI design stále neumí:**
AI zvládne ~70 % designové práce za zlomek času. Zbylých 30 % — brand identita, emoční rezonance, kontextové UX rozhodování — vyžaduje lidský úsudek. Víc paralelních agentů nenahrazuje kvalitu vizuálního rozhodování.

---

## Claude Cowork — nastavení pro maximální produktivitu

*Zdroj: @NickSpisak_ na X, 27. 3. 2026 — https://x.com/NickSpisak_/status/2037535318614610191*
*Zdroj: @coreyganim na X, 27. 3. 2026 — https://x.com/coreyganim/status/2037549431151526241*

Claude Cowork = funkce v Claude Desktop app která dělá skutečnou práci: čte email, kontroluje kalendář, píše dokumenty, napojuje se na Slack, Gmail, Google Calendar, Notion, 30+ dalších nástrojů.

**Proč většina lidí Cowork nepoužívá správně:** přeskočí prvních 30 minut konfigurace. Claude bez nastavení nezná tvé jméno, byznys, styl komunikace ani workflow.

**5-krokový setup (30 minut, nebo 10 minut s pluginem):**

**Krok 1 — Napoj nástroje PRVNÍ (5 minut)**
Před psaním instrukcí připoj nástroje — Claude pak může tahat kontext z existujících dokumentů při setupu.
Priorita: Google Workspace (Drive, Gmail, Calendar) → Slack → Notion → project management (Asana, Linear)

**Krok 2 — Vytvoř context soubory (10 minut)**
Tři soubory v dedikované složce (např. `ClaudeContext/`):
- `about-me.md` — co děláš, jaké projekty, background, koho sloužíš, jaké nástroje používáš
- `brand-voice.md` — jak komunikuješ (přímý/vřelý/akademický?), co nesnášíš (buzzwords, pasivní hlas), příklady tvých nejlepších textů
- `working-style.md` — má se nejdřív ptát nebo rovnou pracovat? Formát výstupů? Hard rules ("nikdy em dashes")?

Trick: nepiš to sám — řekni Claudovi "Create these three files. Interview me so you can fill them out."

**Krok 3 — Global Instructions (5 minut)**
Claude Desktop → Settings → Cowork → Edit Global Instructions. Zkondenzuj context soubory do ~800 slov:
```
Who I am (2-3 věty)
How I work (přístup, komunikace)  
Output defaults (formát podle typu tasku)
Voice/tone
Key business context
Rules (always do / never do)
```
Přidej vždy: **"Always show a plan. Wait for my approval. Then execute."** — tohle zabrání Claude přepisovat soubory které neměl.

**Krok 4 — Nainstaluj skills (5 minut)**
Customize → Browse Plugins. Začni s 3-5:
- Productivity plugin (od Anthropic) — task management, plánování dne
- Jeden specifický pro tvůj workflow (newsletter, projekty, výzkum...)
- Vlastní skill: "I want to create a plugin for [recurring task]. Interview me about the workflow, then turn it into a plugin."

**Krok 5 — Scheduled tasks (5 minut)**
Automatické tasky bez promptování. Příklad daily briefing (každý den 8:00):
*"Check Slack for high-priority messages. Check email for anything needing response. Check calendar and prep for today's meetings. Give me a prioritized briefing."*
→ Otevřeš laptop, briefing už čeká.

**Další tips:**
- **Transfer z ChatGPT** — Settings → Capabilities → "Start import from other AI providers". Vygeneruje prompt, vlož do ChatGPT, dostaneš export všech memories → vlož do Claude.
- **successful-examples/** složka — dej tam své nejlepší emaily, posty, návrhy. Claude reverse-engineeruje tvůj styl z reálných výsledků, ne z popisu.
- **Plan mode je safety net** — bez něj Claude může přepsat soubory které neměl. S ním: uvidíš plán → schválíš → teprve pak spustí.

---

## Claude Managed Agents — hluboký dív: bezpečnost, architektura, enterprise

*Zdroj rozšíření: @hooeem na X, 14. 4. 2026 — https://x.com/hooeem/status/2044068404659646923*

### Stale Harness Trap — proč workaroundy zabíjejí výkon

Typická past: postavíš harness kolem dnešního modelu, hardcoduješ workaroundy pro jeho quirky, odešleš do produkce. Funguje. Pak vyjde nový model a tvoje workaroundy se stávají dead code.

Příklad z Anthropic: Claude 3.5 Sonnet měl "context anxiety" — model předčasně ukončoval tasky jak se plnil kontext window. Engineeři zabudovali automatické context resety do harnessu. Po vydání Claude 4.5 Opus toto omezení zmizelo. Hardcoded resety se staly pasivní zátěží snižující výkon.

**Řešení Managed Agents:** odtrhne reasoning engine od execution layer. Logika agenta zůstává čistá, Anthropic řeší model-specific problémy.

### Brain vs. Hands architektura

Meta-harness princip transformuje infrastrukturu agentů z "pets" (jeden monolitický kontejner co opatrujete) na "cattle" (každá komponenta je resilient a nahraditelná):

- Sandbox crashne z faulty bash příkazu? Harness ho zachytí jako standardní tool-call error, vyzve model k retry s novým kontejnerem. Žádný ztracený kontext.
- Harness selže? Restartuje okamžitě, stáhne celý event stream z nezávislého session logu, pokračuje z přesného místa selhání.
- Kontejnery jsou provisioned lazily — reasoning engine začne streamovat okamžitě, sandbox se spustí jen při prvním tool callu vyžadujícím code execution. Výsledek: median time-to-first-token latency klesla o 60%, na 95. percentilu o 90%+.

### Security — Zero-Trust a Credentials Vault

**Reálný attack vector:** malicious prompt skrytý v codebase může instruovat agenta aby četl environment variables a exfiltroval API klíče na externí server.

**Řešení — MCP Proxy architektura:**
1. Agent vydá strukturovaný tool call proxy, předá jen funkční payload + session-scoped identifikátor. Žádné credentials.
2. Proxy zkřížuje session identifikátor s Anthropic credentials vault (analogie k HashiCorp Vault).
3. Proxy stáhne OAuth/bearer tokeny přímo z vault.
4. Proxy provede API call jménem agenta, vrátí jen operační výstup.

Harness a sandbox zůstávají trvale slepé k podkladovým credentials. Kompromitovaný sandbox nemůže ukrást credentials — jednoduše neexistují v paměti ani filesystému kontejneru.

**Git authentication:** token se použije výhradně při provisioning kontejneru, zapojí se do git remote konfigurace. Agent spouští `git push/pull` nativně bez přístupu k raw tokenu.

### Context Compaction

Long-running agenti čelí degradaci kvality jak se plní context window surovými logy. Managed Agents odděluje kontinuální session od aktivního context window:

- Session = immutable, append-only databáze každého eventu (mimo LLM)
- Při naplnění kontextu: harness pozastaví execution, injektuje summarizační prompt, model vygeneruje hustý souhrn v XML tagách, surová konverzační historie se smaže, injektuje se jen souhrn
- Raw eventy přetrvávají v externím session logu — agent může kdykoliv dotazovat historické slices

Ekvivalent v Claude Code: `/compact` (manuální kompakce), `/clear` (reset session).

### Event Stream — real-time telemetrie

Agenti operují asynchronně. Aplikace se připojuje k SSE (Server-Sent Events) streamu. Klíčové typy eventů: zprávy, tool cally, status updates, span termination (z nich lze extrahovat token consumption a počítat náklady v reálném čase).

Session state je persistentní — můžeš přidávat zprávy do stejného session ID hodiny nebo dny po sobě. Agent provisionuje nový kontejner a pokračuje v přesném předchozím kontextu.

### Multi-Agent Swarm (Research Preview)

Pro komplexní workloady: orchestrátorský agent s týmem specialistů (database specialist, frontend reviewer, security auditor). Decompose task → orchestrátor spustí independent concurrent sessions pro každého sub-agenta → každý sub-agent má čistý, focused context window → komunikace přes internal message queue a shared workspace log.

Use case: audit celého repozitáře na authentication vulnerabilities a přepsání postižených endpointů. Paralelizovaný swarm za minuty místo dní.

### Outcomes — Deterministic Self-Evaluation (Research Preview)

Definuješ explicitní, ověřitelná kritéria úspěchu přes JSON schemas a binární assertions:
- Vygenerovaná funkce musí mít pod 50 řádků
- Musí být přítomny a projít 3 distinct edge-case testy
- Output musí striktně odpovídat OpenAPI specifikaci

Pokud assertion selže, agent vstoupí do autoresearch refinement loop. Interní benchmarking: zvýšení success rate o 10 p.b. na komplexních structural generation workflows.

### Enterprise Case Studies

- **Asana AI Teammates**: agenti s deep awareness of Asana work graph. Autonomně přijímají tasky, dekomponují cíle, používají Google Drive/SharePoint via MCP, postují checkpoint komentáře.
- **Rakuten**: 5 divisí (product, sales, marketing, finance, HR), každý domain-specific agent shipping za méně než týden. 79% redukce time-to-market pro nové AI features.
- **Sentry**: detection → autonomous remediation → PR. Zero human intervention until code merge.

### Deployment Checklist

1. Account na `platform.claude.com` s kredity
2. Agent vytvořen (system prompt, model, tools)
3. Environment nakonfigurován (network rules, dependencies)
4. Credentials vault setup (OAuth connections)
5. Test session v konzoli
6. Agent ID, Environment ID, Vault ID extrahovány
7. Session management logika v application backendu
8. SSE event stream handler implementován
9. Database persistence pro session IDs
10. Cost monitoring dashboard

### Open-Source alternativy k Managed Agents

- **Eigent + CAMEL-AI** — local-first, privacy-centric, Docker/self-hosted, model-agnostic (Claude + OpenAI + Ollama)
- **MultiCA** — AI agenti jako členové týmu na vizuálních kanban boardech, real-time WebSocket streaming
- **Cabinet** — AI-first knowledge base na file-based markdown s git-backed historií, persistent memory, scheduled cron jobs
- **n8n** — visual node automation s encrypted credential vaults (ne striktně agent harness, ale robustní pro enterprise orchestraci)

---

## Claude Skills — Praktický průvodce (Modul 1: Základy)

*Zdroj rozšíření: @Ai_here202 na X, 15. 4. 2026 — https://x.com/Ai_here202/status/2044357700012883980*

### Skills vs Projects vs MCP — kde co patří

| | Co dělá | Klíčové vlastnosti |
|---|---|---|
| **Projects** | Knowledge base | Statické, informační, reference-only |
| **Skills** | Execution engine | Procedurální, opakovatelné, automatizované |
| **MCP** | Connection layer | Napojení na databáze, kalendáře, emaily |

**Kdy vytvořit skill:** pokud jsi napsal stejné instrukce více než 3×, nebo chceš konzistentní, opakovatelný output.

### 5-krokový průvodce výstavbou skillu

**Krok 1 — Define the Job**
Tři klíčové otázky:
1. Co skill dělá? (velmi specificky — ne "pomáhá s daty", ale "transformuje messy CSV soubory do strukturovaných spreadsheetů s clean headers, standardizovanými daty YYYY-MM-DD a bez prázdných řádků")
2. Kdy se aktivuje? (konkrétní user inputs jako triggery)
3. Jak vypadá úspěch? (before vs after příklad)

Většina skillů selhává právě zde — definice je příliš vágní.

**Krok 2 — YAML triggery**
Tři pravidla:
- Third-person jazyk: ❌ "I help users..." ✅ "Processes input data..."
- Buď explicitní s triggery — Claude nepředpokládá záměr
- Nastav negative boundaries (kdy se skill NEMÁ aktivovat)

**Krok 3 — Instrukce**
Jeden konkrétní příklad > desítky abstraktních instrukcí. Vždy zahrni: input + expected output.

**Krok 4 — Reference handling**
Soubory ukládej do `references/` složky. **Kritické pravidlo:** jen jedna úroveň hloubky — reference files nesmí odkazovat na jiné reference files (Claude může truncate context).

**Krok 5 — Deploy**
Umísti složku do `~/.claude/skills/`. Claude ji automaticky detekuje.

**Shortcut — automatizace tvorby skillu:**
1. Nový chat → požádej o build skillu pro tvůj task
2. Nahraj příklady, šablony, guidelines
3. Odpověz na strukturované otázky
4. Systém vygeneruje kompletní SKILL.md, správnou strukturu, ready-to-deploy setup

---

## Claude x TradingView — MCP integrace pro tradery

*Zdroj: @milesdeutscher na X, 15. 4. 2026 — https://x.com/milesdeutscher/status/2044536031991763414*

TradingView nemá veřejné API. MCP server od @Tradesdontlie (github.com/tradesdontlie/tradingview-mcp) toto obchází a dává Claude přístup k live datům z TradingView Desktop.

**Jak to funguje:**
Claude nečte jen screenshot grafu. Čte skutečné underlying hodnoty — stejně jako developer console čte živou webovou stránku.

**Požadavky:** Claude Code, Node.js 18+, TradingView Desktop app, placený TradingView plán (real-time data)

**Setup (2 kroky):**
1. V Claude Code spusť: *"Install the TradingView MCP server. Clone and explore https://github.com/tradesdontlie/tradingview-mcp, run npm install, add to my MCP config at ~/.claude/.mcp.json, and launch TradingView with the debug port."* → klikej Allow
2. Health check: *"Use tv_health_check to confirm TradingView is connected."*

**Reálné use cases:**
- **Live price data:** "Go to my TradingView charts and overlay the live price of $BTC versus $SOL — which one is outperforming today?"
- **Market research report:** "I haven't been at my desk all day. Take a screenshot of the SP500. Give me a detailed research report."
- **Add indicators:** "Source the best indicators for volume, 100D moving average, and a volatility index, and put them on my charts."
- **Technical analysis + drawing:** "Conduct TA on Bitcoin. Draw what you're seeing on my charts."
- **Price alerts:** "Set price alerts for $BTC breaking above $75,000, for SP500 breaking ATH, and go through my watchlist for dip-buying opportunities."
- **Pine Script development, backtesting via Replay mode, tab management, timeframe changes**

**Praktické limitace:**
- Manuální "babysitting" (klikání Allow) je zdlouhavé — lepší na druhém monitoru na pozadí
- Složitější prompty mohou trvat 10+ minut
- Spotřebovává Claude tokeny — používej na high-leverage tasky (strategie, Pine Scripts), ne jednoduché akce

**Tip:** Kombinuj s Claude Scheduled Tasks nebo Remote Control pro autonomní ranní scan watchlistu.

---

## GitHub repos pro Claude Code — 12 nejlepších

*Zdroj: @InduTripat82427 na X, 16. 4. 2026 — https://x.com/InduTripat82427/status/2044796125811740893*

| # | Repo | Co dělá |
|---|---|---|
| 1 | **claude-mem** (github.com/thedotmack/claude-mem) | Persistent memory across sessions — stop re-teaching Claude codebase |
| 2 | **UI UX Pro Max** | 50+ stylů, 161 color palettes, 99 UX guidelines — Claude přestane budovat ugly UI |
| 3 | **n8n-MCP** (github.com/czlonkowski/n8n-mcp) | Napojení Claude Code na 400+ n8n integrací přes MCP |
| 4 | **LightRAG** (github.com/HKUDS/LightRAG) | Graph + vector RAG — Claude chápe velké codebases strukturálně |
| 5 | **Everything Claude Code** (github.com/affaan-m/everything-claude-code) | Skills, instincts, security scanning, multi-language coverage — full agent harness |
| 6 | **Antigravity Awesome Skills** (github.com/sickn33/antigravity-awesome-skills) | Community bible — curated skills, hooks, slash commands, orchestrators |
| 7 | **Superpowers** (github.com/obra/superpowers) | Vynucuje strukturované myšlení před psaním kódu |
| 8 | **Claude Code Ultimate Guide** (github.com/FlorianBruniaux/claude-code-ultimate-guide) | 23K+ řádků dokumentace, 219 šablon, 271 kvízů — začátečník → power user |
| 9 | **Antigravity Awesome Skills** | 1 200+ ready-to-use skills — jedna z největších kolekcí |
| 10 | **Claude Agent Blueprints** (github.com/danielrosehill/Claude-Agent-Blueprints) | 75+ agent workspace šablon mimo coding |
| 11 | **VoiceMode MCP** (github.com/mbailey/voicemode) | Hlasové konverzace s Claude Code přes Whisper + Kokoro |
| 12 | **Awesome Claude Plugins** (github.com/ComposioHQ/awesome-claude-plugins) | 9 000+ repozitářů s adoption metrics — najdeš co lidi skutečně instalují |

---

## AI Speed-to-Lead Agent — postav a prodej za $2K+

*Zdroj: @coreyganim na X, 4. 4. 2026 — https://x.com/coreyganim/status/2040394205537714324*

**Co to je:** AI systém který reaguje na příchozí leady okamžitě, 24/7, bez lidského zapojení. Formulář vyplněn → agent odpoví za sekundy, klade kvalifikační otázky, zachytí detaily, bookne schůzku, pošle majiteli souhrn.

**Proč to funguje:**
- 78% zákazníků koupí od toho kdo odpoví první
- 5minutová odpověď = 21× větší pravděpodobnost kvalifikace vs. 30 minut
- Průměrná B2B response time: 42 hodin → lead je pryč

Klíč: inteligentní odpověď, ne jen potvrzení. "Hey [Name], thanks for asking about [specific service]. Is this residential or commercial?" = konverzace, ne autoresponder.

**Tři způsoby výstavby:**

| Nástroj | Čas | Cena/měs | Vhodné pro |
|---|---|---|---|
| **Zapier** | 1–2 hod | $50–150 | Dead-simple workflows |
| **Make** | 2–4 hod | $9–16 | Nejlepší poměr výkon/jednoduchost |
| **n8n** | 4–8 hod | Self-hosted = zdarma | Maximální výkon |

**Doporučený stack:** Make.com + Twilio SMS ($0.0079/zpráva) + OpenAI API + Calendly + klientův CRM. Celkem $20–50/měs.

**Cenotvorba:**
- Setup: $1 500–5 000 (single SMS responder → multi-channel AI agent)
- Monthly retainer: $300–1 000
- Jak justifikovat: roofing firma zavře 2 extra joby po $5K = $10K nový revenue. Tvůj $500/měs retainer = 20× návratnost. Klient si spočítá sám.

**Jak najít prvního klienta:**
1. Vyber jeden niche (contractors jsou nejsnazší)
2. Najdi 10 firem s kontaktními formuláři
3. Odešli inquiry, sleduj response time
4. Email těm nejpomalejším: "I submitted an inquiry 3 days ago. Never heard back. How many leads like me do you lose each month? I can fix that."
5. První klient zdarma za testimonial → case study → dalších 10 klientů

---

## $12K/měsíc — AI Implementation Consulting Service

*Zdroj: @Zephyr_hg na X, 18. 4. 2026 — https://x.com/Zephyr_hg/status/2045575416010686889*

**Co to je:** Pracuješ s 10–50 person businessem. Auditujete jak firma skutečně funguje → identifikujete 3–5 workflows které krvácejí hodiny týdně → navrhnete a postavíte AI/automation systémy → trénujete tým → zůstanete na retaineru pro tuning a next batch.

**Proč AI nemůže nahradit:** AI sice staví workflows, ale nevybírá které. Výběr vyžaduje pochopení businessu — rozhovor s ops ledem, sledování jak sales tým operuje mezi 5 nástroji, identifikace bottlenecku. To je lidská práce. Zodpovědnost. Lidský hlas v telefonu když workflow padne v 21:00 před launchem.

**Co $12K/měsíc skutečně kupuje:**
- Měsíc 1: Operační audit → prioritized list automation příležitostí + projected hours saved/týden
- Měsíc 2: Build 3 systémy, integrace do existujících nástrojů
- Měsíc 3: Training týmu, dokumentace, monitoring setup
- Měsíc 4+: Tuning, next wave, opravy

**Matematika:** 20-person tým ztrácí 15 hod/týden na manuální práci = 60 hod/měsíc × $75/hod = $4 500 ztracený čas. $12 000 za službu co šetří $18 000–25 000 na práci = triviální math pro každého majitele.

**Tři nabídky (pick one per client):**
1. **Audit only** — $3 000 flat, 1 týden. 30-stránkový prioritized playbook. 20% se změní v full engagement. (Trojanský kůň)
2. **Build only** — $15 000 fixed, 3–5 systémů za 6 týdnů
3. **Full engagement** — $12 000/měsíc, 6-měsíční minimum

**Jak najít první 3 klienty:**
- Start s vlastní sítí — nabídni audit za $1 500 místo $3 000 za case study
- Case study → LinkedIn post s konkrétními čísly + 10-min video before/after
- Post weekly, DM každého 20–50-person business ownera který interaguje
- Lead otázkou: "Where are you losing time?" — 3 konverzace → discovery call → 1 audit

**Proč August 2026 je deadline:**
Každý měsíc přichází nová vlna businessů která zjistí že jejich AI purchases nic nevyřešily. Poptávka stoupá. Konkurence je stále nízká — do Q4 2026 to nebude platit.

---

## Claude tokeny — 10 způsobů jak přestat narážet na limity

*Zdroj: @0xWast3 na X, 21. 4. 2026 — https://x.com/0xWast3/status/2046603104678818303*

Claude nepočítá zprávy. Počítá tokeny. Zpráva č. 30 stojí 31× více než zpráva č. 1 — stejný chat, stejný Claude, jen delší historie.

**10 návyků pro efektivní využití:**

1. **Edituj prompt místo follow-upu** — klikni Edit na původní zprávu → oprav → regeneruj. Stará výměna se nahradí, ne přidá. Ušetří až 21× méně tokenů vs. follow-up.

2. **Nový chat každých 15–20 zpráv** — 98.5% tokenů se spotřebuje na čtení staré historie, jen 1.5% na skutečný výstup. Shrnutí staré konverzace + nový chat = efektivita.

3. **Dávkuj otázky do jedné zprávy** — 3 oddělené prompty = 3 context loads. 1 prompt se 3 tasky = 1 context load. Claude navíc vidí celý kontext najednou → lepší výstupy.

4. **Projects pro opakující se soubory** — upload jednou → cached. Každá nová konverzace v projektu na ni odkazuje. Smlouvy, briefingy, style guides → obrovská úspora.

5. **Memory & User Preferences** — Settings → ulož roli, styl, preference jednou. Claude je aplikuje automaticky. Ušetří 3–5 setup zpráv na nový chat.

6. **Vypni features co nepoužíváš** — Web search, connectors, Advanced Thinking přidávají tokeny k KAŽDÉ odpovědi. Pravidlo: pokud jsi to záměrně nezapnul, vypni to.

7. **Haiku pro jednoduché tasky** — gramatika, brainstorming, formátování, překlady. Ušetří 50–70% budgetu pro práci která skutečně potřebuje silnější model.

8. **Rozlož práci přes den** — Claude používá rolling 5-hour window, ne půlnoční reset. Zprávy z 9:00 přestávají počítat ve 14:00. Rozděl do 2–3 session: ráno, odpoledne, večer.

9. **Pracuj mimo peak hours** (od 26. 3. 2026) — stejný query, stejný chat, ale v peak hodinách spaluje limity rychleji. Peak (vyhnout se pro těžké tasky): **5:00–11:00 AM PT / 8:00 AM–2:00 PM ET ve všední dny**. V Evropě = odpoledne.

10. **Extra Usage jako safety net** — Pro/Max subscribers: Settings → Usage → Overage. Když dojde session limit, Claude nepřestane — přepne na pay-as-you-go při API sazbách.

---

## Prompt Engineering — expert úroveň

*Zdroj: @eng_khairallah1 na X, 22. 4. 2026 — https://x.com/eng_khairallah1/status/2046881340977782970*

Model není bottleneck. Prompt je.

**Proč špatné prompty existují:** LLM předpovídají nejpravděpodobnější next token. Vágní prompt → model vyplní mezery nejstatisticky průměrným obsahem.

"Write a blog post about AI" = průměr milionu blogpostů. Specifický prompt s tonálem, strukturou, délkou a cílovou skupinou = unikátní výstup.

**Princip: specifičnost porazí obecnost.** Každý detail odstraní stupeň volnosti kde by model jinak defaultoval na průměr.

### 6 elementů každého expert promptu

1. **Role** — ne "helpful assistant", ale "Senior product strategist s 15 lety B2B SaaS zkušeností"
2. **Context** — co Claude potřebuje vědět o tvé situaci (industry, audience, constraints, goals)
3. **Task** — co přesně má udělat (ne "help with marketing", ale "write competitive analysis comparing our positioning against 3 specific competitors")
4. **Format** — jak má output vypadat ("tabulka + 2-paragraph recommendation")
5. **Constraints** — co nemá dělat ("no marketing jargon, no generic advice")
6. **Quality standard** — co znamená "dost dobré" ("analysis specific enough pro product team decision do 5 minut")

Expert prompt zasahuje všech 6. Beginner typicky 1–2.

### Strukturální techniky

**XML tagy pro jasnost** — Claude byl trénován na strukturovaných inputech:
```xml
<context>B2B SaaS, 50 zaměstnanců, project management pro construction</context>
<task>Napiš cold outreach email na VP of Operations</task>
<constraints>pod 150 slov, žádný generic opener, specifický pain point, low-commitment CTA</constraints>
<output_format>Subject line, pak email body. Nic jiného.</output_format>
```

**Context First, Question Last** — dlouhé dokumenty vždy PŘED otázkou. Model zpracuje dokument, vybuduje porozumění, pak narazí na otázku s plným kontextem. Opačné pořadí = retroaktivní reinterpretace = horší výsledky.

**Few-shot příklady** — 1 konkrétní příklad > 10 paragrafů popisu. Zahrn normální případy I edge cases. 3–5 příkladů dá lepší výstup než jakákoliv descriptivní instrukce.

### Pokročilé techniky

**Chain metoda** — nikdy nežádej Claude o 5 věcí v jednom promptu. Rozeřaď do sekvence. Každý prompt fokusovaný → každý výstup hluboký. Kvalita se na každém kroku násobí. Navíc: v každém bodě můžeš zkontrolovat a opravit.

**Self-correction loop** — každá první odpověď je draft. Přidej: "Reread your response. Rate it 1–10 on accuracy, specificity, actionability. Fix anything below 8." Zlepšení v 85–90% případů. Trvá 15 sekund.

**Motivated Constraint** — řekni PROČ constraint existuje:
- ❌ "Keep it under 200 words."
- ✅ "Keep it under 200 words — this goes into a Telegram post where anything longer gets cut off."

Když Claude chápe důvod, aplikuje constraint inteligentněji a zachytí edge cases.

**Multi-Perspective Analysis** — pro strategická rozhodnutí:
```
Analyze this pricing decision from three perspectives:
1. Growth-focused CEO (maximize market capture)
2. CFO watching margins
3. Customer who wants fair value
Each perspective: 3 sentences. Then synthesize + flag which perspective you weighted most and why.
```

**Meta-Prompt** — když nevíš jak napsat dobrý prompt, nech Claude ho napsat:
```
I want to accomplish: [cíl]
Context: [background]
Good output looks like: [příklad]
Write me the most effective prompt for this result.
```
Vygenerovaný prompt je téměř vždy lepší než co bys napsal sám.

### System-Level mastery

**Context Files** — persistentní markdown soubory pro každý typ práce:
- `writing-rules.md` — hlas, audience, standardy
- `analysis-framework.md` — jak hodnotíš data, klíčové metriky
- `project-context.md` — aktuální projekty, rozhodnutí

Na začátku session: "Read [file] fully before starting. Follow every rule. If about to break a rule, stop and tell me."

**Template Library** — každý skvělý prompt ulož jako šablonu. Stripp specifika, nahraď proměnnými. Měsíce budování = library šablon pro každý typ tasku. Nikdy nezačínáš od nuly.

**Weekly Feedback Loop** — každý pátek: review AI výstupy z týdne. Co minulo cíl? Jaká prompt změna by to opravila? Jaké pravidlo přidat do context files?

---

## Services-as-Software — byznys model budoucnosti

*Zdroj: @itsalexvacca (Alex Vacca, ColdIQ) na X, 15. 4. 2026 — https://x.com/itsalexvacca/status/2044502868556992937*

**Teze (Sequoia partner Julien Bek):** Příští trillion-dollar firma bude prodávat práci, ne nástroj. Na každý dolar software spend existuje 6+ dolarů services spend. AI právě proměnil services budget na něco co startup může napadnout.

**Copilot vs. Autopilot:**
- **Copilot** — AI v rukou profesionála. Profesionál nese výsledek a vlastní vztah s klientem. (Harvey pro law firms, Rogo pro investment banks)
- **Autopilot** — přeskočí profesionála, prodává výsledek přímo zákazníkovi. (Crosby pošle NDA, WithCoverage uzavře pojistku, ColdIQ bookne meeting)

Firma prodávající nástroj = permanentní závod s modelem. Firma prodávající práci: zlepšuje se pokaždé, když se zlepší model, protože klesají náklady na delivery při stejné ceně pro zákazníka. Marže roste. Data moat se prohlubuje.

**6-krokový playbook (ověřeno na ColdIQ, $7M ARR):**

1. **Vyber jeden outsourcovaný line item v jednom oboru** — čím užší, tím rychleji sbíráš proprietární data (= moat). Tři ověřující otázky: Je práce již dnes outsourcována (existující budget line)? Je to spíš intelligence work (pattern recognition), ne pure strategy? Je services spend výrazně větší než software spend?

2. **Prvních klientů získej sám** — nepotřebuješ web, deck ani funnel. Potřebuješ klienty kteří ti řeknou co nenáviděli na předchozím vendorovi. Cenu nastav na floor kde chceš být za 3 roky. Zaznamenej a přepiš každý sales call — námitky z prvních 10 callů = copy na sales page po prvních 10 klientech.

3. **Dělej práci ručně co nejdéle** — data z manuálního provozu jsou cennější než jakýkoliv MVP. ColdIQ manuálně vedl první kampaně — tento training set poháněl 2 200+ kampaní pro stovky klientů v dalších letech. 4 artefakty od prvního dne: markdown soubor pro každý opakující se task, Loom pro work s cursorem, decision log per client, soubor neúspěšných kampaní s důvody.

4. **Cenotvorba jako service, reporting jako produkt** — prodávej outcome, buildi dashboardy jako SaaS firma. Fungující cenotvorba: upfront setup fee + měsíční retainer vázaný na outcome metric + performance bonus. Retention v services businessu začíná vypadat jako SaaS retention pokud klientská zkušenost vypadá jako SaaS.

5. **Nejdřív nahraď sebe v delivery** — pořadí náboru: 1. delivery operator (čistá exekuce), 2. technical automator (markdown workflows → agenti), 3. head of delivery. **Nepřijímej marketéra, salespersona ani COO dokud delivery layer neběží bez tebe.**

6. **Compound data moat před compound software** — ulož každý třetí-stránní vstup (raw i cleaned), každý deliverable tagovaný s outcome, reasoning týmu při judgment calls. 3 roky provozu = data asset co pure-SaaS competitor nemůže koupit ani replikovat.

---

## Google Maps AI Lead Gen — $5K–15K/měsíc

*Zdroj: @noisyb0y1 na X, 26. 4. 2026 — https://x.com/noisyb0y1/status/2048396579065799151*

**Insight:** 5 milionů local service businessů na Google Maps (HVAC, plumbing, elektrikáři, pest control, roofing) má problémy které vyřešíš za hodinu — zastaralý web, špatné recenze, žádná online přítomnost. Kombinace AI + Google Maps dává přístup k nevyčerpanému trhu.

### Tři revenue streamy

**1. Website business: $500–2 000 na klienta**
- Google Maps search "HVAC near me" → hledej firmy bez webu nebo s outdated webem
- Vezmi název firmy, services z Google Maps profilu, nejlepší customer reviews
- ChatGPT/Claude vygeneruje kompletní website brief za 2 minuty → AI website builder
- 4 klienti × $800 = $3 200 + monthly maintenance $100–300/klient

**2. Reputation management: $300–800/měsíc na klienta**
- Každá firma na Google Maps s méně než 4.2 hvězdami aktivně ztrácí zákazníky (92% zákazníků čte recenze před nákupem)
- Monitoruj recenze, odpovídej na každou přes AI, eskaluj negativní na majitele
- Prompt: "Act as a professional customer service manager. Write a warm, professional response to this [positive/negative] review for [business type]. Acknowledge their experience, [add apology if negative], and invite them back. Keep it under 100 words."
- Škálovatelné: 1 člověk zvládne 15–20 klientů

**3. Cold outreach na autopilotu: 500 leadů denně**
1. Scrape Google Maps přes Outscraper nebo PhantomBuster → spreadsheet firem s kontakty
2. Automatic qualification: dej AI spreadsheet → identifikuj firmy s problémy (nízké hodnocení, starý web, chybějící kontaktní info)
3. Personalizovaný outreach: pro každou qualified firmu AI napíše cold email s konkrétními daty z jejich profilu
4. Email landing rate: vypadá jako by ho napsal člověk co se skutečně podíval na jejich business

**Realistika:**
- Týden 1: 40–70 potenciálních klientů
- Zavřit 5% = 2–4 klienti
- $5 000–15 000 za měsíc s kombinací všech tří revenue streamů

---

## Multi-Agent Coding Stack 2026: Kimi K2.6 + Claude

*Zdroj: @eng_khairallah1 na X, 28. 4. 2026 — https://x.com/eng_khairallah1/status/2049055333054857612*

**Teze:** Vývojáři co nejvíce produkují nejsou loajální jednomu nástroji. Provozují více agentů a routují každý task tam kde dá nejlepší output za nejnižší cenu.

### Proč Kimi K2.6 jako alternativa k Claude

| Model | SWE-Bench Verified | Input tokens | Output tokens |
|---|---|---|---|
| Claude Opus 4.6 | 80.8% | $5/M | $25/M |
| **Kimi K2.6** | **80.2%** | **$0.80/M** | **$3.60/M** |
| GPT-5.2 | 80.0% | — | — |

**Kimi K2.6** od Moonshot AI: open-source (Apache 2.0), plné weights na Hugging Face, self-hostovatelný. Terminal-first coding agent **Kimi Code**. Na OpenRouter programming leaderboardu: #1.

**Setup:**
```bash
pip install kimi-code
kimi
# /login pro autentizaci
```
VS Code extension dostupná z marketplace. Nativní podpora Zed, integrace s Cursor a JetBrains přes ACP.

**2-týdenní test (reálné projekty):**

- **REST API od nuly** (DB models, auth, CRUD, tests): Kimi Code naplánovalo kompletní strukturu nejdříve, pak provádělo file po file, referovalo vlastní dřívější rozhodnutí. Výsledek: fungující API s minimálními tweaky. (K2.6 má thinking mode — architektura PŘED generováním kódu)
- **Refactor přes 12 souborů**: zůstalo koherentní celou cestu. Snížilo průměrný počet kroků o ~35% vs. předchozí stack.
- **Test suites pro existující codebase**: solid, konzistentní output za zlomek ceny.

**Výsledek:** 85–90% denní coding tasků → Kimi Code (cena 7× nižší). Zbylých 10–15% (komplexní architektura, dlouhé agentic loopty) → Claude.

**MCP kompatibilita — migrace bez tření:**
```bash
kimi mcp add-all ~/.claude/mcp.json  # přenes celou konfiguraci
kimi mcp add <server>               # přidej individuálně
kimi mcp list                       # přehled
kimi mcp test <server>              # test connection
```
Celý tool ecosystem se přesune okamžitě.

**Klíčové CLI příkazy:**
- `Ctrl-X` — toggle shell mode (terminál bez opuštění agenta)
- `/sessions` — view a switch sessions
- `--continue` — pokračuj přesně kde jsi skončil
- `/compact` — kompakce context window při plnění
- `kimi --yolo` — auto-approve všechny modifikace souborů (jen na vlastních projektech!)
- `kimi acp` — IDE integrace pro Zed/JetBrains

**Agent Swarm — bez ekvivalentu v Claude/GPT:**
Koordinuje až 100 sub-agentů pracujících paralelně. Real příklady:
- 40 akademických PDF → 100 000-slov literature review s fully cited datasetem
- 100 job descriptions → 100 individuálně přizpůsobených CV
- Jedna astrophysics paper → 40-stránkový report + 20 000-row dataset + 14 publication-grade chartů

**Kde Claude stále vede:**
- Nejkomplexnější English instruction following (perfektní adherence k detailním constraints přes stovky agentic steps)
- Context window: Claude 1M tokenů vs. K2.6 262K tokenů
- Ecosystem maturity (Západ)

**Aktuální stack autora:** 85% práce → Kimi Code, 15% → Claude, batch processing → Agent Swarm. Týdenní API výdaje klesly o ~85%.
