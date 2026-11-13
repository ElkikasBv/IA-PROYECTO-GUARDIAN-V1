# TODO: implementar claim_extractor
import ollama
from ai_guardian.config import OLLAMA_HOST, OLLAMA_MODEL
from ai_guardian.schemas import ClaimExtraction

def extract_claims(text: str) -> ClaimExtraction:
    client = ollama.Client(host=OLLAMA_HOST)

    mensajes = [
        {

            "role": "system",
            "content": (
                "Extrae SOLO afirmaciones verificables (datos que se pueden comprobar). "
                "NO extraigas opiniones, gustos ni creencias personales. "
                "Cada afirmación debe ser una oración completa que se entienda sola: "
                "SIEMPRE incluye el sujeto con su nombre, nunca uses pronombres.\n\n"
                "Ejemplo 1:\n"
                "Texto: Messi nació en Rosario y tiene 3 Mundiales.\n"
                '{"claims": [{"text": "Messi nació en Rosario."}, '
                '{"text": "Messi tiene 3 Mundiales."}]}\n\n'
                "Ejemplo 2:\n"
                "Texto: Pienso que el café es horrible, pero Brasil produce mucho café.\n"
                '{"claims": [{"text": "Brasil produce mucho café."}]}'
            ),
        },
        {"role": "user", "content": text},
    ]

    respuesta = client.chat(
        model=OLLAMA_MODEL,
        messages=mensajes,
        format=ClaimExtraction.model_json_schema(),
        options={"temperature": 0},
    )

    return ClaimExtraction.model_validate_json(respuesta.message.content)