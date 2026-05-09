# 27. Autonomní agenti: kde je hranice mezi užitečným a nebezpečným

Zdroj tématu: 03_agenti_automatizace.md

---

1/7 Autonomní agenti jsou mocné, protože sami rozhodují, jak použít dostupné nástroje. Jenže právě tahle samostatnost je zároveň jejich největší slabinou. Pojďme si vyjasnit, kde leží hranice mezi užitkem a rizikem.

2/7 Agent injection se stává novým fem. Zatímco dřív se hackeři snažili oklamat člověka, teď mohou skrytými instrukcemi manipulovat agenty skrz jejich context window. Agent má autonomii rozhodovat, to je jeho zranitelnost.

3/7 Čím více autonomie agentům dáte, tím více se násobí i možnosti selhání. Sub-agenti pracují paralelně a nezávisle, ale každý má přístup k nástrojům. Bez přesného omezení (readonly přístup, konkrétní nástroje) se riziko exponenciálně zvyšuje.

4/7 Prakticky: používejte guardrail nody. Ověřte vstupy před tím, než agent cokoliv udělá. Kontrolujte výstupy. A kde jde o rizikové akce (booking, emaily, transakce), přidejte schvalování člověkem do loop.

5/7 Rozhodněte jasně: potřebujete agenta, nebo vám stačí lineární workflow s LLM? Agent je overkill, pokud máte předvídatelný sled kroků. Agenti mají smysl jen u složitého rozhodování v šedé zóně.

6/7 Testujte vždy v bezpečném prostředí dřív než v produkci. Agent může halucinovat způsobem, který váš guardrail nenalezne. Ani nejlepší bezpečnostní vrstva není kultura.

7/7 Checklist: Definujte přesně, jaké nástroje má agent (max 10–15). Přidejte input i output guardrails. Kam jde o peníze či komunikaci, vyžadujte human approval. A otázka: máte vůbec nad agentem dostatečnou kontrolu?
