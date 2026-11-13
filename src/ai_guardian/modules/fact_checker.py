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
        f"[{i}] Fuente: {e.source} ({e.url})\n{e.snippet}"
        for i, e in enumerate(evidence, start=1)
    )

    instrucciones = (
        "Eres un verificador de afirmaciones. Recibirás una AFIRMACIÓN y una EVIDENCIA. "
        "Decide usando SOLO el texto de la evidencia, nunca lo que tú creas saber. "
        "Responde con una de estas etiquetas: "
        "supported (la evidencia respalda la afirmación), "
        "contradicted (la evidencia dice algo distinto o la contradice), "
        "not_enough_info (la evidencia no habla de esto o no alcanza para decidir). "
        "Primero comprueba que la evidencia hable del MISMO sujeto de la afirmación "
        "(la misma persona, lugar o cosa). Si habla de otro sujeto, "
        "responde not_enough_info. "
        "Si dudas, elige not_enough_info. "
        "Escribe una explicación corta, de una o dos oraciones, en español."
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