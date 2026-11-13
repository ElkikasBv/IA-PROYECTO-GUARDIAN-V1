from ai_guardian.modules.claim_extractor import extract_claims
from ai_guardian.modules.evidence_retriever import search_evidence
from ai_guardian.modules.fact_checker import check_claim


def main():
    texto = "La capital de Francia es París y tiene aproximadamente 2 millones de habitantes."

    afirmaciones = extract_claims(texto).claims

    for i, claim in enumerate(afirmaciones, start=1):
        evidencia = search_evidence(claim.text)
        for e in evidencia:
            print(e.snippet)
        resultado = check_claim(claim.text, evidencia)

        print(f"{i}. {resultado.claim}")
        print(f"   Resultado: {resultado.label}")
        print(f"   Explicación: {resultado.explanation}")
        for url in resultado.evidence_urls:
            print(f"   Fuente: {url}")
        print()


if __name__ == "__main__":
    main()