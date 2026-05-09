1. Jak jsem zkrátil práci z 8 hodin na 2 pomocí Claude Code

---

Google engineer s 11 lety praxe pracuje 2–3 hodiny denně místo 8.

3 kroky, 15 minut setup:

**1/** CLAUDE.md — jeden soubor který AI zastaví než začne over-engineerovat. 4 principy od Andrej Karpathy. Funguje.

**2/** Skills — opakující se práci popíšeš jednou, Claude ji dělá pořád. Onboarding, návrhy, monitoring.

**3/** Zeptej se AI: "Co pro mě můžeš dělat každý den?" Překvapí tě co vymyslí samo.

Z 8 hodin na 2–3 denně. Stačí začít.

---

2. 5 věcí které AI dělá lépe než Google Search

---

Google ti dá 10 odkazů. AI ti dá odpověď.

Konkrétně:

**1/** AI rozloží tvůj dotaz na 100 variant, prohledá tisíce stránek najednou a vrátí syntézu. (Perplexity, ChatGPT)

**2/** Složité otázky — "jak nastavit RAG pro malou firmu" Google neví, AI vysvětlí krok za krokem.

**3/** Srovnání produktů a technologií bez reklamy.

**4/** Research do hloubky — dáš AI 10 zdrojů, dostaneš strukturovaný přehled.

**5/** Opakované dotazy — AI má kontext, Google začíná od nuly pokaždé.

Není to náhrada. Je to upgrade.

---

3. Jak správně promptovat — chyby které dělá 90% lidí

---

Špatný prompt = AI odpovídá na otázku kterou jsi nepoložil.

Nejčastější chyby:

**1/** Vágní zadání. "Vylepši text" vs "Zkrať na 3 věty, tón profesionální, bez adjektiv." Druhé funguje.

**2/** Negace. "Nepiš složitě" AI ignoruje. "Piš na úrovni 5. třídy" AI poslouchá.

**3/** Žádná role. "Jsi senior copywriter s 10 lety praxe" zlepší výstup o cca 40% bez jiné změny.

**4/** Kontradiktor v instrukci. "Buď stručný a zahrň historický kontext i praktické příklady" — co má AI udělat?

**5/** Žádný příklad. Ukáž jak má výstup vypadat. Few-shot prompting funguje.

Specifičnost je vše.

---

4. CLAUDE.md: proč ho každý AI uživatel potřebuje

---

Každou session Claude začíná od nuly. CLAUDE.md to mění.

Je to soubor v projektu který se automaticky načte na začátku každého chatu. Komprimuje kontext, nastavuje pravidla, šetří tokeny.

Andrej Karpathy zdokumentoval 4 principy které zastaví nejčastější LLM chyby: Think Before Coding, Simplicity First, žádné zbytečné závislosti, respektuj existující patterns.

Výsledek? AI nepřepisuje co funguje, nepřidává co jsi nepotřeboval, začíná tam kde jsi skončil.

Lodní kompas: malá korekce na startu = obrovský rozdíl po 10 000 km.

---

5. Jak buildovat s AI bez znalosti programování

---

Nepotřebuješ umět kódovat. Potřebuješ vědět co chceš.

Realita v roce 2026:

Make.com — drag and drop automatizace za 15 dolarů měsíčně. Spojíš Gmail s Notion s AI bez jediného řádku kódu.

N8N — pro složitější workflow, open source, víc kontroly.

Lovable, Bolt.new — napíšeš co chceš a dostaneš funkční frontend.

Klíčový insight: "Very basic AI knowledge can put you ahead of 90% of the market." Nestaví to nejlepší programátor. Staví to ten kdo nejlíp ví co zákazník chce.

Technologie je teď nejlevnější část.

---

6. Moje denní AI stack (nástroje + jak je používám)

---

Nestačí mít Claude. Záleží jak ho propojíš.

Stack podle Cole Medin:

Claude Desktop — hlavní mozek, bounce off ideas, psaní, analýzy.

Perplexity — research nových technologií kde chci citovatelné zdroje.

N8N nebo Make — automatizace které běží bez mě.

Aqua Voice — diktuju místo píšu, text se upraví sám.

Supabase — databáze pro RAG a memory.

Jedno pravidlo: nástroj musí žít ve tvém workflow. Pokud se musíš přepínat, nepoužiješ ho.

---

7. Jak AI mění práci freelancera — osobní zkušenost

---

AI nezabil freelancing. Přepsal pravidla hry.

Co se děje:

Komoditní práce (přepisy, překlady, jednoduché texty) zmizela nebo je za zlomek ceny. To je fakt.

Ale freelancer který AI používá dělá práci 3 lidí. Dostane projekt, AI udělá 80%, on udělá kvalitu a kontext.

Nové příležitosti: AI agent development (175–300 dolarů za hodinu), RAG implementace, workflow automation.

Pointa: neztratíš práci AI. Ztratíš ji někomu kdo AI používá a ty ne.

Otázka není "použít AI" — otázka je "jak rychle."

---

8. 10 promptů které používám každý den

---

Konkrétní prompty které šetří čas:

**1/** "Jsi [role]. [Úkol]. Formát: [co chceš dostat]."
**2/** "Shrň tohle ve 3 bodech. Žádný fluff."
**3/** "Jaké jsou 3 největší chyby při [téma]?"
**4/** "Kritizuj svou vlastní odpověď. Co ti chybí?"
**5/** "Přemýšlej nahlas krok za krokem než odpovíš."
**6/** "Přepiš pro [cílová skupina]. Tón: [tón]."
**7/** "Co by [expert v oboru] řekl na [problém]?"
**8/** "Navrhni 5 variant. Já vyberu."
**9/** "Co v tomhle textu nefunguje a proč?"
**10/** "Zeptej se mě na 3 věci než začneš — chybí ti kontext."

Poslední je podceňovaný. AI se neptá samo od sebe. Nauč ho ptát se.

---

9. Proč většina lidí z AI nevytěží ani 20 % možností

---

Problém není AI. Problém je představa co AI umí.

Většina lidí si myslí: domácí úkoly, překlad, generování textu. To je 5% schopností.

Co AI reálně zvládne dnes: autonomní výzkum, komplexní analýzy, řízení prodejního procesu, onboarding klientů, monitoring, konkurenční analýza každé ráno automaticky.

Nick Saraev: "Zeptej se AI: Co pro mě můžeš dělat každý den? Překvapí tě."

Okno se zavírá. Kdo se naučí teď, bude dělat věci které ostatní považují za magii.

Neztratíš práci AI. Ztratíš ji někomu kdo AI takhle používá.

---

10. Jak jsem zautomatizoval 3 hodiny admin práce týdně

---

Admin práce existuje ve dvou kategoriích: důležitá a opakující se.

Tu opakující se si nech dělat AI.

Konkrétně:

Faktury a příjmy — každý email s "invoice" v předmětu se automaticky označí a kategorizuje. 15 minut setup, nula minut týdně.

Onboarding emaily — šablona plus AI personalizace = pošle se sama po podpisu smlouvy.

Denní briefing — AI každé ráno zkompiluje co se děje v tvém oboru.

Pravidlo: nejdřív identifikuj co děláš každý týden bez přemýšlení. To je tvůj seznam k automatizaci.

Automatizuj nízkohodnotové, ponech si čas na to co vydělává.
