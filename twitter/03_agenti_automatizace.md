21. Rozdíl mezi chatbotem a AI agentem (vysvětleno jednoduše)

---

ChatGPT na otázku odpoví. AI agent otázku vyřeší.

Konkrétní rozdíl:

Chatbot: dostane vstup, vrátí výstup. Hotovo. Nemůže se rozhodnout co dělat dál.

AI agent: dostane cíl. Sám se rozhodne jaké nástroje použít, v jakém pořadí, zda opakovat, zda si vyžádat více dat. Booking schůzky — sám zjistí co chybí, zavolá Google Calendar, potvrdí.

Bez toolu to není agent. Jen LLM.

Klíčové slovo: autonomie rozhodování.

---

22. Jak funguje multi-agent orchestrace

---

Jeden agent dělá práci sériově. Více agentů paralelně a specializovaně.

5 vzorů které fungují:

**1/** Prompt chaining — agent A předá výsledek agentovi B.
**2/** Routing — jeden LLM rozhodne komu úkol přiřadit.
**3/** Orchestrator + Workers — jeden řídí, ostatní plní.
**4/** Paralelizace — skupina specializovaných agentů běží najednou, výsledky se spojí.
**5/** Evaluator loop — jeden agent tvoří, druhý hodnotí a vrací zpět.

Pravidlo: čím užší role agenta, tím lépe. LLM se zahltí rychle. Max 10–15 nástrojů na agenta. Nad tím jdi do multi-agent.

AI agenti fungují lépe čím víc se podobají specialistovi, ne generalistovi.

---

23. 5 věcí které AI agent zvládne bez tvého dohledu

---

AI agenti nejsou spolehliví na vše. Ale na tohle ano:

**1/** Autonomní výběr nástrojů — sám rozhodne co zavolat a v jakém pořadí.

**2/** Paralelní zpracování stejného problému více cestami najednou.

**3/** Opakující se smyčky — observe, reason, act. Opakuje dokud nemá výsledek.

**4/** Reakce na triggery v reálném čase — nový lead, příchozí email, změna v databázi.

**5/** Sběr a strukturování dat z více zdrojů bez lidského překladu.

Kde agenti selhávají: dlouhodobé projekty vyžadující adaptivní učení. Tam jsou lidé stále "sniper rifles." Agenti jsou sprinteré, ne maratonci.

---

24. Kdy použít agenta a kdy stačí jednoduchý prompt

---

Nepoužívej agenta tam kde stačí prompt. Je to jako jet autem pro noviny za rohem.

Prompt stačí když:
Chceš textovou odpověď. Proces je jasně definovaný. Výsledky musí být přesné a kontrolovatelné.

Agent potřebuješ když:
Interakce s externími systémy (email, kalendář, databáze, API). Vstupy jsou nepředvídatelné. LLM by si jinak věci vymyslel. Customer-facing chatbot kde "wow faktor" má hodnotu.

Zlaté pravidlo Nick Saraev: "Bez toolu to není agent." Přidej alespoň jeden nástroj. Jinak stavíš drahý chatbot.

---

25. Jak jsem postavil agenta který mi posílá denní briefing

---

Denní briefing agent má jednu práci: ráno mi řekne co se děje.

Architektura:

Heartbeat — každý den v 7:00 se agent spustí. Přečte kdo je, jaký má plán, co má za úkoly.

Datové zdroje: RSS feedů z oboru, Google Alerts, monitoring konkurence, calendar eventy.

Output: strukturovaný email nebo Telegram zpráva. 3 sekce, max 10 položek celkem.

Stack: Claude API plus cron job plus MCP servery pro zdroje. Nebo jednoduše N8N s AI uzly.

Čas na setup: 2–3 hodiny. Čas ušetřený každý týden: hodina ranního scrollování.

---

26. n8n vs. Zapier vs. vlastní agent — srovnání

---

Nejsou to konkurenti. Jsou to různé nástroje pro různé problémy.

Zapier a Make: lineární automatizace. Spouštěč plus akce. Spolehlivé, předvídatelné, ověřené po letech. Ideální pro jednoduché opakující se tasky.

N8N: hybridní. Můžeš přidat AI uzel kamkoli do workflow. Víc flexibility, open source. Ale stále jde o automatizaci, ne agenturu.

Vlastní agent: kontextová vědomost, přirozený jazyk, adaptivní rozhodování. Komplikovanější na setup, nepředvídatelnější výstupy.

Varování od Nick Saraev: "n8n AI agenty zatím nespolehlivě produkují ROI který bys nedostal jednoduší automatizací." Začni jednodušeji, přidávej složitost postupně.

---

27. Autonomní agenti: kde je hranice mezi užitečným a nebezpečným

---

Čím víc autonomie dáš agentovi, tím víc ho musíš hlídat.

Kde agent funguje bezpečně: nízko-rizikové úlohy, customer support, booking, content tvorba. Chyba stojí málo.

Kde agent nesmí rozhodovat autonomně: finanční transakce, právní dokumenty, kritické business procesy. Chyba stojí hodně.

Nové riziko: agent injection. Cole Medin: "Mohlo by být nebezpečnější než phishing z roku 2010." Skryté instrukce v context windows, malicious MCP servery, permission escalation.

Pravidlo: agent by měl mít přístup jen k tomu co potřebuje pro svůj konkrétní úkol. Nic víc.

Autonomie je superschopnost i slabina ve stejný čas.

---

28. Jak agenti komunikují mezi sebou (A2A protokol)

---

MCP propojuje agenta s nástroji. A2A propojuje agenty navzájem.

A2A (Agent-to-Agent) je open-source protokol od Googlu. Funguje jako microservices architektura — každý agent běží jako server, ostatní ho volají přes HTTP.

Jak to funguje:

Agent card — metadata soubor který popisuje co agent umí a jak s ním mluvit.

Task discovery — klientský agent stáhne agent card a ví co může požádat.

JSON komunikace — pošle request, dostane response s metadaty.

Push notifikace — pro live aktualizace v reálném čase.

Výhoda: agenti se mohou dynamicky dozvědět schopnosti ostatních za běhu. Žádné pevné napojení, žádné padání při aktualizaci.

---

29. Nejčastější chyby při stavbě AI agentů

---

"Building AI agents is 25% coding and 75% evaluation." — Cole Medin

Nejčastější chyby:

**1/** Příliš mnoho nástrojů. Max 10–15 na jednoho agenta. Nad tím LLM vybírá špatně a zapomíná volat.

**2/** Přeceňování deterministiky. Agent zvládne 50× správně a 51× zpacká. Plánuj pro selhání, nejen pro úspěch.

**3/** Přeengineering od začátku. Nezačínej orchestrací. Začni s jedním agentem, jedním toolem, RAG.

**4/** Nula evaluací. Tweakuješ prompt jednou a doufáš. Správně: průběžné testování, metriky, CI pro prompty.

**5/** Negace v system promptu. "Neodpovídej na X" AI ignoruje. Formuluj pozitivně.

---

30. Budoucnost práce: člověk jako orchestrátor agentů

---

Do roku 2030 bude 20% obchodu agent-to-agent. Agenti budou najímat agenty.

Tvoje role se mění.

Ne: dělám úkoly.

Ano: říkám agentům co dělat, kontroluji výstupy, rozhoduji co zautomatizovat a co ne.

Vznikají ambient businesses — podniky které běží autonomně. Ty nastavíš pravidla, agenti vykonávají.

Co si ponecháš: kritické myšlení, klíčová rozhodnutí, osobní vztahy. To AI nenahradí.

Co outsourcuješ: opakující se práci, sběr dat, první drafty, monitoring.

Lidé kteří toto pochopí a adaptují se budou dělat věci které ostatní považují za magii. Okno se zavírá.
