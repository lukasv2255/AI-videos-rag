# 24. Kdy použít agenta a kdy stačí jednoduchý prompt

Zdroj tématu: 03_agenti_automatizace.md

---

1/5 Agenta máš postavit kolem systémového promptu. Ten je klíčový. Všechno ostatní se kolem něj točí. Ale předtím se ptej: opravdu ti agent stojí za to?

2/5 Agent má cenu jen když řeší konkrétní workflow. Chceš delegovat úkoly mezi specializované agenty? Potřebuješ paměť a sekvenci kroků? Pak ano. Jednoduchý prompt stačí na jednorázové otázky.

3/5 Máš-li agenta, drž se minima. Ne více než deset nástrojů. Každý nástroj a instrukce ti zabírá tokeny, které stojí peníze a zpomalují odpověď. Střídmě s MCP servery, pokud nejsou hyper standardizované.

4/5 Systémový prompt se skládá ze čtyř částí: persona a cíle, instrukce pro nástroje, příklady workflow, ostatní návody. Začni tímto šablonem a vylepšuj ručně na základě toho, co agent dělá špatně.

5/5 Kontrolka: Máš konkrétní workflow? Potřebuješ paměť mezi kroky? Více než jeden nástroj? Pokud vše ne, prostě použij prompt v chatu. Aby agent měl smysl, musí dělat víc než jen odpovídání.
