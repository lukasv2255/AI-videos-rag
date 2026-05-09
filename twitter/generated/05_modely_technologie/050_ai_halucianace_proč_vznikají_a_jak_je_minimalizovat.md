# 50. AI halucianace: proč vznikají a jak je minimalizovat

Zdroj tématu: 05_modely_technologie.md

---

1/5 AI agenti mají zásadní slabinu: nejsou determinističtí. Tentýž vstup může dát jiný výstup, přestože prošel korektně padesátkrát. Důvod? Mohou si vymyslet informace s naprostou sebejistotou. Tomu se říká halucinace.

2/5 Halucinace se zesilují když agentů pracuje více najednou. Mají tři spolehliví agenti svého dílčího úkolu na 95 procent, společný úspěch padá na 86 procent. Chyby se navzájem skládají. To je důvod, proč víc agentů znamená víc rizika.

3/5 Řešení: Nechte agenty ušetřit čas, nenahrazujte s nimi sebe zcela. Místo aby agent sám posílal emaily, ať vytvoří návrhy. Pořád vám ušetří čas, ale halucinace vás nebude rozpadat za zády.

4/5 Při plánování agenta nešetřete. Pět hodin plánu vám ušetří dvacet hodin vývoje později. Jakmile začnete kódovat bez jasné strategie, budete se muset vrátit na start. Bolí to, ale pak si to sjedete.

5/5 Jak na halucinace teď:
• Používejte ochranné zábrany (guardrails) – jednoduše ověřujte výstupy
• Specializujte agenty – každý ovládá jinou sadu nástrojů
• Buďte explicitní v příkazech – vyhněte se rozporem v system promptu
• Přidejte příklady – LLM se z nich učí

Jaký proces byste vyzkoušeli první?
