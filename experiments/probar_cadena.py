from ai_guardian.modules.claim_extractor import extract_claims
from ai_guardian.modules.evidence_retriever import search_evidence
from ai_guardian.modules.fact_checker import check_claim

CASOS = [
    ("Messi ganó el Mundial de 2022 con Argentina.", "supported"),
    ("La Tierra tiene dos lunas y el Sol es un planeta.", "contradicted"),
    ("Creo que el cine de antes era mejor, aunque Titanic salió en 1997.", "solo Titanic"),
    ("Mi vecino Pedro compró un coche rojo ayer.", "not_enough_info"),
]

for texto, esperado in CASOS:
    print("=" * 60)
    print(f"TEXTO: {texto}")
    print(f"ESPERADO: {esperado}")

    for claim in extract_claims(texto).claims:
        evidencia = search_evidence(claim.text, limit=2)
        resultado = check_claim(claim.text, evidencia)
        print(f"  - {resultado.claim}")
        print(f"    -> {resultado.label}: {resultado.explanation}")
    print()