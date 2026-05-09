# 28. Jak agenti komunikují mezi sebou (A2A protokol)

Zdroj tématu: 03_agenti_automatizace.md

---

1/5 Agenti potřebují způsob, jak si navzájem říci, co umí. Google na to přišel s A2A protokolem – standardem pro komunikaci mezi agenty. Bez něj jsou propojení křehká a náchylná na chyby.

2/5 Agent card je jednoduchý metadata soubor. Popisuje, co agent dělá, jak s ním komunikovat a jaké má požadavky. Jeden agent se na něj podívá a hned ví, co od druhého agenta chce.

3/5 Bez standardu musíte hardcodovat integraci. Aktualizujete finance agenta? Risikujete rozbití v prodejenním agentovi. S A2A se agent dozví schopnosti druhého v reálném čase. Flexibilita místo křehkosti.

4/5 A2A je otevřená architektura, není to nástroj k instalaci. Je to model pro stavbu – můžete ji aplikovat na svou infrastrukturu, na kterýkoliv framework. Proto bude využitá, i když se A2A projekt změní.

5/5 Agent teams vs subagenti: subagenti pracují izolovaně (rychle, levně), agent teams si navzájem píšou zprávy a koordinují práci (pomalejší, ale lepší výsledky pro složitý kód). Jak stavíte své agenty – distribuovaně nebo v týmech?
