# Lessons — Naučené poučení

> Claude: přečti tento soubor na začátku každé session.
> Po každé korekci nebo chybě přidej poučení sem.

---

## 2026-04-29 — search_articles nespouštět bez triggeru

**Situace:** Claude automaticky hledal v articles.md/MCP i bez `ask [dotaz]` triggeru.

**Správně:** MCP nástroje (`search_articles`, `ask_ai_videos`) volat pouze když zpráva začíná `ask`. Jinak číst `articles.md` přímo.

---

## 2026-04-29 — mcp_server.py a .mcp.json jsou v .gitignore

**Situace:** Soubory jsou commitnuté, ale zároveň v `.gitignore` — Git je trackuje jen protože byly přidány dřív. Na novém počítači po `git clone` tyto soubory chybí.

**Správně:** Buď je z gitignore vyndat, nebo zajistit že setup sekce v README obsahuje instrukce pro jejich vytvoření.

---
