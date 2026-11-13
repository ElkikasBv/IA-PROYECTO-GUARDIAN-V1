# AI Guardian

Sistema para verificar automáticamente las afirmaciones de otras IAs.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
pip install pytest
cp .env.example .env
```

## Ejecutar

```bash
python -m ai_guardian.main
pytest
```
