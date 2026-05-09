11. Claude Code vs. Cursor — čím se liší a kdy použít který

---

Nemusíš si vybrat. Nejlepší výsledky dává kombinace obou.

Rozdíly:

Claude Code — lepší na design, animace, interakce. Klíčové slovo "ultrathink" a Claude opravdu přemýšlí. Plan mode dostupný.

Cursor — výrazně silnější plan mode pro komplexní problémy, detailnější plány, lepší follow-up otázky. Lepší integrace s Xcode pro iOS.

Workflow který funguje: Cursor plan mode pro návrh architektury, Claude Code pro samotný build a UI.

Vždy zapni plan mode. Výstup se zlepší o 20% bez jiné změny.

---

12. Jak funguje Claude Code memory systém

---

Claude každou session začíná od nuly. Pokud to nevyřešíš, opakuješ se stále dokola.

Jak paměť funguje:

Memory.md — globální soubor, injektuje se automaticky na začátek každé session. Napíšeš "zapamatuj si X" a příště to ví.

CLAUDE.md — projektová paměť. Pravidla, architektura, rozhodnutí, co neopakovat.

docs/project_notes/ — strukturovaná paměť: bugs.md, decisions.md, key_facts.md. Před každým debuggingem Claude přečte bugs.md. Před každou změnou přečte decisions.md.

Pokročilý setup: denní log plus cron job který extrahuje klíčová rozhodnutí do wiki. Claude se postupně učí jak pracuješ.

---

13. 5 Claude Code hooks které mi šetří čas každý den

---

Hooks jsou deterministická kontrola — spouštíš vlastní příkazy před nebo po akci Claude.

5 které používám:

**1/** Zvukové upozornění po dokončení tasku — nemusím sedět a čekat. Claude pípne.

**2/** Logování každého tool use — vím co Claude dělal v pozadí.

**3/** Pre-compact hook — před komprimací session se uloží shrnutí do memory.

**4/** Session end hook — po zavření session se klíčová rozhodnutí zapíší do docs.

**5/** Auto-commit po úspěšném testu — hotový kód se sám commitne.

Hooks jsou jen v Claude Code. Cursor je nemá. To je jeden z důvodů proč Claude Code vedou.

---

14. Jak nastavit multi-agent workflow v Claude Code

---

Jeden agent dělá práci sériově. Multi-agent dělá práci paralelně.

Setup:

Nastav CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=true v prostředí.

Vytvoř 3 základní sub-agenty: Code Reviewer, QA Tester, Researcher.

Definuj workflow v CLAUDE.md: Write, Code Review, QA, Ship.

Pak prostě řekni: "Create an agent team to review my codebase" — Claude sám rozdělí práci a spustí agenty paralelně.

Důležité varování: nepoužívej sub-agenty na jednoduché úkoly. Startup čas může být delší než benefit. Pro komplexní projekty je to ale game-changer.

---

15. Claude Code plan mode — proč ho ignoruješ a neměl bys

---

"A minute of planning saves you 10 minutes of building."

Plan mode je jednoduché: Claude čte kód, prohledává web, přemýšlí — ale nic nemění. Výstup je dokument s plánem. Ty ho schválíš nebo opravíš, pak teprve Claude staví.

Výhoda: pracuješ v teoretickém prostoru. Žádné opravy po faktu.

Spustíš přes Shift+Tab nebo explicitně napíšeš "plan mode."

Cole Medin: výstup vzroste minimálně o 20% jen tím že plan mode používáš. Stojí to 2 minuty navíc a ušetří hodiny.

Proč to ignoruješ? Protože chceš výsledky hned. To je přesně ta chyba.

---

16. Jak buildovat vlastní AI skills pro Claude Code

---

Skill je soubor SKILL.md který naučí Clauda jak přesně zvládat opakující se úkol.

Popíšeš jednou. Pak funguje pořád.

Jak na to:

**1/** Explore — nech Clauda zkusit úkol bez guidance. Uvidíš kde selhává.

**2/** Research — nastuduj doménu. Claude potřebuje principy, ne kroky.

**3/** Draft — napiš první verzi skill.

**4/** Self-critique — nechej Clauda ohodnotit vlastní instrukce.

**5/** Iterate — testuj na čerstvé instanci, opravuj dokud nemáš 95%+ fidelity.

Cole Medin používá skills na: klasifikaci leads, automatické návrhy, onboarding klientů, editaci videí. Každý skill = jeden "AI zaměstnanec" pro konkrétní úkol.

---

17. MCP servery — co to je a jak ti mohou změnit workflow

---

AI umí psát a přemýšlet. MCP mu dá přístup k tvým systémům.

MCP = Model Context Protocol. Anthropic ho vydal v listopadu 2024. Funguje s Claude, OpenAI, Gemini.

Jak to funguje: Napíšeš MCP server který vystavuje funkce. Claude Desktop nebo IDE se připojí. Najednou Claude může číst tvou databázi, posílat emaily, kontrolovat GitHub, číst Notion — bez copy-paste.

Analogie: USB-C. Místo stovky různých kabelů jeden standard. Drive MCP plus Sheets MCP plus Apollo MCP a zřetězíš je bez custom kódu.

Prakticky: AI asistent který skutečně ví co se děje v tvém projektu.

---

18. Claude Code pro ne-programátory: co je reálně možné

---

Nick Saraev přímo říká: "You don't need to be a programmer to understand what's going on."

Co neprogramátor reálně může postavit s Claude Code:

Portfolio web — "make a simple portfolio for [jméno]" a je to.

Automatizace — napojenou na email, kalendář, Notion.

AI agenti — s MCP servery a bez psaní kódu.

Jak to funguje: Claude dekonstruuje úkol na high-level kroky. Vidíš co dělá, můžeš zastavit a dát nové instrukce. Nemusíš číst kód.

Cena 17–20 dolarů měsíčně. Nick říká 100–200x ROI v prvním měsíci. Kdo to nezkusí, nevěří.

---

19. Jak spravovat kontext v dlouhých Claude sezeních

---

Dlouhé sezení = Claude zapomíná co bylo na začátku. Nebo se ztrácí v detailech.

Jak na to:

CLAUDE.md max 200–500 řádků. Vše delší snižuje kvalitu a zvyšuje náklady.

Nejdůležitější pravidla dej nahoru — AI si pamatuje začátek lépe (primacy bias).

Bullet pointy a krátké nadpisy, ne dlouhé odstavce.

Hooks na konci sezení — automaticky se uloží shrnutí do memory.md.

Pokud Claude dělá stejnou chybu 2–3x, přidej pravidlo do CLAUDE.md. Jednou, navždy.

CLAUDE.md je živý kód. Pravidelně ho audituj a odstraňuj co přestalo platit.

---

20. Vibe coding: jak jsem postavil funkční app za víkend

---

Vibe coding = dáváš vibes, AI staví. Ty jen ověřuješ že to funguje.

Stack za víkend:

Claude Code — hlavní builder.

GitHub — verzování.

Vercel — deploy. Každý push = automatický update.

Jak na to:

Napiš co chceš. Jednoduše. "Track my daily habits, 3 screens, minimal design."

Plan mode zapni jako první.

Nevysvětluj technické detaily — řekni co má dělat, ne jak.

Dostaň MVP do rukou reálných uživatelů. Ne perfektní produkt — fungující produkt.

Platíš 20 dolarů měsíčně za Claude Code. Stavíš co by dřív stálo 10 000 dolarů. Matematika mluví sama.
