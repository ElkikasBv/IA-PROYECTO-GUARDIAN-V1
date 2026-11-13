from ai_guardian.modules.claim_extractor import extract_claims
from ai_guardian.modules.evidence_retriever import search_evidence
from ai_guardian.modules.fact_checker import check_claim
from ai_guardian.modules.report_generator import generate_report


def main():
    texto = (
        "La capital de Francia es París. "
        "La Tierra tiene dos lunas. "
        "Creo que el cine de antes era mejor, aunque Titanic salió en 1997."
    )

    for i, claim in enumerate(extract_claims(texto).claims, start=1):
        evidencia = search_evidence(claim.text, limit=2)

        veredicto = check_claim(claim.text, evidencia)
        informe = generate_report(claim.text, evidencia)

        print("=" * 60)
        print(f"{i}. {claim.text}")
        print(f"VEREDICTO (fact_checker): {veredicto.label}")
        print(f"Explicación: {veredicto.explanation}")
        print()
        print("INFORME (report_generator):")
        print(informe)
        print()


if __name__ == "__main__":
    main()