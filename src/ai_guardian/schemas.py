from pydantic import BaseModel
from typing import Literal

class Claim(BaseModel):
    text: str


class ClaimExtraction(BaseModel):
    claims: list[Claim]

class Verdict(BaseModel):
    explanation: str
    label: Literal["supported", "contradicted", "not_enough_info"]


class CheckResult(BaseModel):
    claim: str
    label: Literal["supported", "contradicted", "not_enough_info"]
    explanation: str
    evidence_urls: list[str]
    
class Evidence(BaseModel):
     claim: str
     source: str
     url: str
     snippet: str