from pydantic import BaseModel


class Claim(BaseModel):
    text: str


class ClaimExtraction(BaseModel):
    claims: list[Claim]
