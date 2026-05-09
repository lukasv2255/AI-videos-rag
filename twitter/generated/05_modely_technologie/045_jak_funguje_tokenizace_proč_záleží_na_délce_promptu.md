# 45. Jak funguje tokenizace — proč záleží na délce promptu

Zdroj tématu: 05_modely_technologie.md

---

1/5 Když zadáš prompt, neplatíš jen za svá slova. Systémové soubory, pravidla a nástroje už konzumují tisíce tokenů dřív, než AI vůbec začne odpovídat. Rozumět tokenům znamená šetřit peníze i kvalitu.

2/5 Jeden token se nepřibližně rovná jednomu slovu — spíš je to fyzická jednotka, kterou model zpracovává. Věta "Ahoj, jak se máš?" není čtyři tokeny, ale spíš šest až sedm. Krátký prompt = méně tokenů = lepší odpověď. Model funguje přesněji s kompaktnějšími instrukcemi.

3/5 Delší kontext vede na horší výkony. Čím více historie chatů a nastavení máš aktivní, tím horší kvalita odpovědí. Zároveň roste účet. Řešení: spravuj kontext proaktivně — vyvětšuj neužitečné starší zprávy, zjednodušuj pravidla.

4/5 Příkazem "/context" vidíš, co konzumuje tvoje tokeny ještě před odesláním prvního promptu. Systémové soubory, nástroje, paměť — někdy až deset tisíc tokenů v záloze. Pak si ty musíš zadat svou otázku.

5/5 Co dělat teď: Zkontroluj svůj kontext příkazem /context. Zkrácuj prompty — jednoduché věty, přesné zadání. Odstraňuj starý obsah z chatu. Dostat kvalitu s nízkými tokeny. Jaký je tvůj největší prompt, který teď máš otevřený?
