from ai_guardian.modules.evidence_retriever import search_evidence
from ai_guardian.modules.report_generator import generate_report

claim = "La capital de Francia es Paris"

evidencias = search_evidence(claim)
print(f"Evidencias encontradas: {len(evidencias)}\n")

informe = generate_report(claim, evidencias)
print(informe)