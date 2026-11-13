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
                "Extrae afirmaciones verificables e independientes del texto. "
                "cada afirmación debe ser una oracion corta y autocoontenida"
            ),
        },
        {"role": "user", "content": text},
    ]

    respuesta = client.chat(
        model=OLLAMA_MODEL,
        messages=mensajes,
        format=ClaimExtraction.model_json_schema(),
    )

    return ClaimExtraction.model_validate_json(respuesta.message.content)