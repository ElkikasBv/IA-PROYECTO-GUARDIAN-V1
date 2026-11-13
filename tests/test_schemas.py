from ai_guardian.schemas import Claim, ClaimExtraction


def test_claim_extraction_structure():
    data = ClaimExtraction(claims=[Claim(text="La capital de Francia es París.")])
    assert len(data.claims) == 1
    assert data.claims[0].text == "La capital de Francia es París."
