# 43. RAG: proč je lepší než jen nahrát soubory do chatu

Zdroj tématu: 05_modely_technologie.md

---

1/5 RAG agenti nejsou kouzelníci, ale řeší to, kde tradiční přístup selhává. Nahrát soubor do chatu a doufat není strategie, kterou můžete škálovat nebo spoléhat na přesnost.

2/5 Klíčový rozdíl: RAG vám dá kontrolu nad tím, KDY a JAK agent hledá informace. Různé typy souborů potřebují různý přístup—tabulky nejsou text. Agent se to musí naučit z vašeho promptu.

3/5 Prakticky: tabulková data ukládejte jako jednotlivé řádky, ne jako kusy textu. Agent pak může generovat SQL dotazy na součty, průměry, maxima. To normální RAG úplně selhává—tady se chytá.

4/5 Paměť agenta je kritická. Ukládejte do historie i to, co agent našel v nástrojích—ne jen jeho finální odpovědi. Jinak si agent vás položené věci znovu hledá zbytečně.

5/5 Co dělat teď: (1) Určete, jaké typy souborů máte; (2) Jinak zpracujte text vs. tabulky vs. krátké dokumenty; (3) Nechte agenta v promptu rozhodovat, kterou strategii použít; (4) Testujte v chatu, zatímco iterujete. Máte v týmu někoho, kdo řeší RAG?
