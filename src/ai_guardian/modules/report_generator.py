import ollama

from ai_guardian.config import OLLAMA_HOST, OLLAMA_MODEL
from ai_guardian.schemas import Evidence


def generate_report(claim: str, evidences: list[Evidence]) -> str:
    if not evidences:
        return f"No se encontró evidencia para verificar: {claim}"

    fuentes = "\n\n".join(
        f"[{i}] {e.url}\n{e.snippet}"
        for i, e in enumerate(evidences, start=1)
    )

    prompt = (
        f"Afirmación: {claim}\n\n"
        f"Fuentes:\n{fuentes}\n\n"
        "Escribe un informe corto en español con EXACTAMENTE estas tres secciones:\n\n"
        "Resumen: una frase que repita la afirmación.\n"
        "Evidencia: una línea por fuente relevante, citándola como [1], [2] o [3]. "
        "Ignora las fuentes que no tengan relación con la afirmación.\n"
        "Conclusión: escribe solo UNA de estas opciones: "
        "RESPALDADA, CONTRADICHA o INFORMACIÓN INSUFICIENTE, "
        "seguida de una frase de justificación.\n\n"
        "Usa solo las fuentes dadas. No inventes datos ni te contradigas."
    )

    client = ollama.Client(host=OLLAMA_HOST)
    respuesta = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Eres un verificador de hechos riguroso. Respondes en español.",
            },
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0},
    )
    return respuesta.message.content