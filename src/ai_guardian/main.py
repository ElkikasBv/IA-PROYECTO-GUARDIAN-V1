from ai_guardian.modules.claim_extractor import extract_claims

def main():
    texto = "La capital de Francia es París y tiene aproximadamente 2 millones de habitantes."

    resultado = extract_claims(texto)

    for i, claim in enumerate(resultado.claims, start=1):
        print(f"{i}. {claim.text}")

if __name__ == "__main__":
    main()