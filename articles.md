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

---

## 2. LLM Knowledge Base — Karpathyho metoda

**Základní myšlenka (Andrej Karpathy, ex-OpenAI/Tesla):**
Většina AI nástrojů funguje jako RAG: nahraješ soubory, LLM při každém dotazu od nuly hledá relevantní části. Karpathyho přístup je jiný — LLM postupně buduje a udržuje persistentní wiki z markdown souborů, která sedí mezi tebou a surovými zdroji. Znalost se kompiluje jednou a průběžně aktualizuje, ne znovu odvozuje při každém dotazu.

**Tři vrstvy systému:**
- **Raw sources** (`raw/`) — tvoje kurátorované zdrojové dokumenty. Neměnné, LLM z nich pouze čte.
- **Wiki** (`wiki/`) — LLM-generované markdown soubory. Souhrny, entity stránky, koncepty, porovnání. LLM tuto vrstvu vlastní celou.
- **Schema** (`CLAUDE.md` nebo `AGENTS.md`) — říká LLM jak je wiki strukturována, jaké jsou konvence a jaké workflow následovat.

**Tři operace:**
- **Ingest:** Přidáš nový zdroj do `raw/`, LLM ho zpracuje — jeden zdroj může ovlivnit 10–15 wiki stránek.
- **Query:** Kladeš otázky proti wiki, odpovědi se ukládají zpět jako nové wiki stránky.
- **Lint:** Periodická kontrola — kontradikce, zastaralé tvrzení, orphan stránky, chybějící cross-reference.

**Praktické nastavení (víkendový MVP):**
- **Den 1:** Obsidian + vault se složkami `raw/`, `wiki/`, `reports/` + Obsidian Web Clipper + 20–30 naklipen článků na jedno téma
- **Den 2:** Skill `/kb-compile` → Claude vytvoří wiki stránky → Obsidian graph view → Skill `/kb-report` → první dotaz

**Proč lepší než stateless "New Chat":**
- Dnešní odpověď se stává zítřejším kontextem
- Tvá terminologie a frameworky se stávají kanonickými wiki stránkami
- 6 měsíců práce = privátní korpus, který model dokáže ingested v jednom context window

**Obsidian MCP integrace:**
Claude čte a zapisuje přímo do vaultu v reálném čase. Setup: Community Plugins → Local REST API → API key → `claude_desktop_config.json`. Prompty jako: *"Find all notes mentioning Polymarket and give me a short summary of each"* fungují bez copy-paste.

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

---

## 4. Claude Managed Agents — infrastruktura v cloudu

**Co to je:**
Dosud: stavíš celou infrastrukturu sám (sandboxing, state management, error recovery, credential handling) — měsíce engineeringu. Managed Agents = Anthropic říká: *"My to zvládneme. Ty jen řekni co má agent dělat."*

**4 stavební bloky:**
1. **Agent** — konfigurace: model, system prompt, nástroje. Vytvoříš jednou, znovu použiješ.
2. **Environment** — izolovaný kontejner s předinstalovaným Python, Node.js, Go.
3. **Session** — běžící instance agenta, pamatuje si stav, může běžet hodiny.
4. **Events** — zprávy tam a zpět, agent streamuje výsledky.

**Jak nasadit prvního agenta:**
```bash
curl https://api.anthropic.com/v1/agents \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -d '{"name": "My Agent", "model": "claude-sonnet-4-6",
       "tools": [{"type": "agent_toolset_20260401"}]}'
```
`agent_toolset_20260401` aktivuje vše: bash, file read/write, web search, web fetch, grep, glob.

**Systém oprávnění:**
- `always_allow` — automatické spouštění (interní agenti)
- `always_ask` — čeká na schválení každého tool callu (zákaznicky orientované)
- Lze kombinovat: agent automaticky čte soubory, ale čeká na souhlas před odesláním emailu

**Cena:**
- Standardní Claude API token sazby + $0.08/session-hour
- Web search: $10/1000 hledání
- Typická 10minutová session = pár centů

**Příklady co se buduje:**
- Sentry/Seer: klonuje repo → čte kód → píše opravu → otevírá PR
- Rakuten: specialistické agenty pro každé oddělení, nasazení za méně než týden
- Asana AI Teammates: agent pracuje v Asaně vedle lidí

**Rychlý start:**
```
start onboarding for managed agents in Claude API
```

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

**V prohlížeči (claude.ai):**

| Zkratka | Funkce |
|---|---|
| `Cmd/Ctrl+K` | Nový chat okamžitě |
| `↑` (šipka nahoru) | Upravit poslední zprávu místo follow-up (21× úspora tokenů) |
| `Cmd/Ctrl+.` | Zastavit generování okamžitě |
| `Cmd/Ctrl+/` | Přepnout/skrýt sidebar (+24% pracovního prostoru) |
| `Cmd/Ctrl+Shift+L` | Přepnout dark/light mode |
| `Shift+Enter` | Nový řádek bez odeslání |

**V Claude Code (terminál):**

| Zkratka | Funkce |
|---|---|
| `Esc Esc` (dvojité) | Rewind na libovolný checkpoint |
| `Ctrl+R` | Zpětné vyhledávání v historii promptů |
| `Alt/Option+T` | Přepnout extended thinking per zpráva |
| `Ctrl+G` | Otevřít prompt v externím editoru |
| `Shift+Tab` | Cyklovat: normal → auto-accept → plan |
| `/btw` | Boční otázka bez přerušení úkolu |

**Naměřená úspora:** 51 min/den → 22 min/den = 29 minut denně, ~120 hodin ročně.

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

---

## 6 AI Business Opportunities Nobody Is Building Yet (2027)

*Zdroj: @zephyr_hg na X, 13. 4. 2026*

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

*Zdroj: @noisyb0y1 na X, 13. 4. 2026*

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

*Zdroj: @coreyganim na X, 14. 4. 2026*

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

*Zdroj: @cyrilXBT na X, 15. 4. 2026*

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

*Zdroj: @larsencc (Larsen Cundric, Browser Use) na X, 27. 2. 2026*

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
