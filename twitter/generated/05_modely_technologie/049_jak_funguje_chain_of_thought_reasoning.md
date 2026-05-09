# 49. Jak funguje Chain of Thought reasoning

Zdroj tématu: 05_modely_technologie.md

---

1/5 Agent není pro každou úlohu. Potřebuješ ho, když se rozhodování větvý a logika šedivé zóny. Když je vše předvídatelné, stačí normální kód.

2/5 Čtyři pilíře každého agenta: model (mozek), nástroje (interact), instrukce (chování), paměť (kontext). Selhává-li agent, problém je vždy v jedné z těchto čtyř věcí.

3/5 Chain of Thought je klasika: řekni modelu, aby řešil step-by-step. Jednoduchý postup, ale fungující. Agent si sám projde logiku krok za krokem místo skoku na odpověď.

4/5 Prakticky: Když agent hallucin najednou a udělá chybu, necháš ho znovu pokusit. Druhý pokus často vyjde. Chyba je feedback, ne selhání procesu.

5/5 Checklist na start: Jasně definuj čtyři pilíře (LLM, nástroje, prompt, paměť). Začni s jednoduchým step-by-step logováním. Chyby věř a nech agenta se opravit. Jaký je tvůj největší problém s agentem teď—selhává model, nástroje, či paměť?
