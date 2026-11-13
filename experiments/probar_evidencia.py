from ai_guardian.modules.evidence_retriever import search_evidence

for e in search_evidence("La capital de Francia es París"):
    print(e.url)
    print(e.snippet)
    print("---")