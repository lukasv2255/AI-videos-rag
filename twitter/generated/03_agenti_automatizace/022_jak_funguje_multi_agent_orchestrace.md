# 22. Jak funguje multi-agent orchestrace

Zdroj tématu: 03_agenti_automatizace.md

---

1/5 Agent orchestrace není hype. Je to způsob, jak rozdělit práci mezi specialisty místo, aby jeden model dělal všechno. Funguje to jako organizační struktura: manažer řídí týmy, týmy dělají konkrétní úkoly.

2/5 Klíč je jednoduchost. Jedna velká úloha > jeden agent s patnácti nástroji = chaos. Raději: nadřízený agent rozdělí práci na paralelu. Týmy pracují současně, pak se spojí výsledky. Výrazně rychlejší.

3/5 Pro to, aby agent dělal správně, musíš mu dát persisten context. Použij agents.mmd soubor: vloží se na začátek každé konverzace. Agent hned ví, jak má pracovat. Nepředstavuješ mu to pokaždé znovu.

4/5 Orchestrace má tři vrstvy: direktivy (co dělat, zapsáno přirozeným jazykem jako SOP), agenti (inteligentní routing), skripty (konkrétní nástroje). Agent volí, co zavolat a v jakém pořadí. Zbytek je automatika.

5/5 Zkus teď: Napiš své SOP jako markdown direktivy. Přidej agents.mmd soubor s instrukcemi. Vyber jeden konkrétní úkol, který chceš paralelizovat. Jaký problém řešíš tím, že máš dnes jednoho agenta místo týmu?
