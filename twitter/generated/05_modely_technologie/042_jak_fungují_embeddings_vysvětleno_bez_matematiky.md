# 42. Jak fungují embeddings (vysvětleno bez matematiky)

Zdroj tématu: 05_modely_technologie.md

---

1/5 Vektorové embeddingy převádějí text na matematické reprezentace, které chápou význam lépe než hledání klíčových slov. Rozdíl mezi "Apple sues Google" a "Google sues Apple" je pro ně jasný.

2/5 Prakticky: místo hledání slov v textu ukládáš matematické reprezentace do databáze. Clustering algoritmy pak najdou souvisejicí obsah bez ohledu na přesný výběr slov. Dává to smysl pro články, dokumenty, knowledge base.

3/5 Problém se starou cestou: keyword search nerozumí synonýmům ani konceptuálnímu smyslu. Hledáš-li "Star Wars lodě", budeš chybět X-wing nebo Millenium Falcon. Embeddingy chytí podobnost i bez explicitního zápisu.

4/5 Omezení embeddingy: jsou skvělé pro nestrukturovaná data a přirozený jazyk. U kódu to nestojí za to – tam jsou soubory a syntaxe strukturované, keyword search funguje lépe a je to jednodušší.

5/5 Co dělat teď:
- Zváž embeddingy pro News, články, dlouhý obsah, FAQ
- Pro kód stačí klasické hledání a navigace po souborech
- Zkombinuj přístup podle typu dat, který máš

Jakou databázi s embeddingy jsi zkoušel?
