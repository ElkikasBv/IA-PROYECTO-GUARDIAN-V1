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
                "Extrae afirmaciones verificables del texto. "
                "Cada afirmación debe ser una oración completa que se entienda sola: "
                "SIEMPRE incluye el sujeto con su nombre, nunca uses pronombres "
                "ni omitas el sujeto. Ignora opiniones.\n\n"
                "Ejemplo:\n"
                "Texto: Messi nació en Rosario y tiene 3 Mundiales.\n"
                "Afirmaciones: "
                '{"claims": [{"text": "Messi nació en Rosario."}, '
                '{"text": "Messi tiene 3 Mundiales."}]}'
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