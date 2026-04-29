# Roadmap

## Hotovo
- [x] RAG pipeline: download → build_rag_docs → ingest → MCP server
- [x] 3 kanály: Nick Saraev (283), Cole Medin (181), Greg Isenberg (408) — celkem 866 videí
- [x] MCP nástroje: ask_ai_videos, search_articles, search_nick_saraev, summarize_video, list_videos
- [x] articles.md s keyword search (bez embeddingů)
- [x] Automatické zpracování X.com odkazů

## Nápady / budoucí
- [ ] Embeddingy pro articles.md (teď keyword overlap — méně přesné)
- [ ] Filtrování výsledků podle kanálu v ask_ai_videos
- [ ] Nový kanál: přidat do CHANNELS v download_transcripts.py a build_rag_docs.py
- [ ] Opravit .gitignore: mcp_server.py a .mcp.json jsou gitignored ale commitnuté
