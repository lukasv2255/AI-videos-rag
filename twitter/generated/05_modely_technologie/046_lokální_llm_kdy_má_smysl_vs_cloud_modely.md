# 46. Lokální LLM: kdy má smysl vs. cloud modely

Zdroj tématu: 05_modely_technologie.md

---

1/6 Rozhodování mezi lokálním a cloudovým AI není černobílé. Každý přístup má místo. Klíč: položit si správné otázky v pořadí a odvětví se rozhodovat na základě vašich skutečných potřeb.

2/6 Nejprve: staváte jen proof of concept? Jděte do cloudu. Ušetříte čas na setup, rychle otestujete, rychle zapomeňete, pokud to není správné. Lokální vyžaduje prvotní investici do konfigurace.

3/6 Pak: pracujete se citlivými daty? Zdravotnictví, finance, právní věci, intelektuální vlastnictví? Lokální je povinný. Data zůstávají u vás, nikdy neodcházejí na servery třetích stran.

4/6 Bez citlivých dat a bez nutnosti nejlepších modelů je rozumné jít lokálně, pokud plánujete skálovat na desítky tisíc uživatelů. Pak se splaťuje hardware. Při nízkém provozu je cloud levnější.

5/6 Tvrdá realita: výkonné lokální modely (llama, mistral) potřebují drahý hardware a elektřinu. Buď velká předem investice, nebo pay-per-token v cloudu a později switch.

6/6 Co dělat: Nejdřív si odpovězte: Je to POC? Jsou data citlivá? Potřebuji nejlepší model? Planuji skálování? Pak se rozhodněte. Zkoušejte proof of concept v cloudu, produkci lokálně jen s dobrým důvodem. Jaké jsou vaše nejcitlivější data?
