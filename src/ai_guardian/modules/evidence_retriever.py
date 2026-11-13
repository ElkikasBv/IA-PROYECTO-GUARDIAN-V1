import json
import urllib.parse
import urllib.request

from ai_guardian.schemas import Evidence


def search_evidence(claim: str, limit: int = 3, lang: str = "es") -> list[Evidence]:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": claim,
            "gsrlimit": limit,
            "prop": "extracts|info",
            "exintro": 1,
            "explaintext": 1,
            "exsentences": 3,
            "inprop": "url",
            "format": "json",
        }
    )
    url = f"https://{lang}.wikipedia.org/w/api.php?{params}"
    request = urllib.request.Request(url, headers={"User-Agent": "AI-Guardian/0.1"})

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)

    pages = data.get("query", {}).get("pages", {})
    results = []
    for page in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        results.append(
            Evidence(
                claim=claim,
                source=f"Wikipedia ({lang})",
                url=page.get("fullurl", ""),
                snippet=page.get("extract", ""),
            )
        )
    return results