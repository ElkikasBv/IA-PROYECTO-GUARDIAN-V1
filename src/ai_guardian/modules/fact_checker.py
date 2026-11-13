import ollama

from ai_guardian.config import OLLAMA_HOST, OLLAMA_MODEL
from ai_guardian.schemas import CheckResult, Evidence, Verdict


def check_claim(claim: str, evidence: list[Evidence]) -> CheckResult:
    if not evidence:
        return CheckResult(
            claim=claim,
            label="not_enough_info",
            explanation="No se encontró evidencia para esta afirmación.",
            evidence_urls=[],
        )

    texto_evidencia = "\n\n".join(
        f"[{i}] Fuente: {e.source} ({e.url})\n{e.snippet[:500]}"
        for i, e in enumerate(evidence, start=1)
    )

    instrucciones = (
        "Eres un verificador de afirmaciones. Recibirás una AFIRMACIÓN y una EVIDENCIA. "
        "Decide usando SOLO el texto de la evidencia, nunca lo que tú creas saber. "
        "Primero escribe una explicación corta, de una o dos oraciones, en español. "
        "Después elige la etiqueta que coincida con tu explicación: "
        "supported (la evidencia dice lo mismo que la afirmación), "
        "contradicted (la evidencia dice explícitamente lo contrario), "
        "not_enough_info (la evidencia no habla del tema o de ese sujeto). "
        "Si tu explicación dice que la evidencia no menciona el tema, "
        "la etiqueta DEBE ser not_enough_info."
    )

    mensajes = [
        {"role": "system", "content": instrucciones},
        {
            "role": "user",
            "content": f"AFIRMACIÓN:\n{claim}\n\nEVIDENCIA:\n{texto_evidencia}",
        },
    ]

    client = ollama.Client(host=OLLAMA_HOST)

    respuesta = client.chat(
        model=OLLAMA_MODEL,
        messages=mensajes,
        format=Verdict.model_json_schema(),
        options={"temperature": 0},
    )

    veredicto = Verdict.model_validate_json(respuesta.message.content)

    return CheckResult(
        claim=claim,
        label=veredicto.label,
        explanation=veredicto.explanation,
        evidence_urls=[e.url for e in evidence],
    )