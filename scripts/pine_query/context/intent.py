"""IntentExtractor — rule-based: extract verb, object, domain, filters from task text.

No NLP. No embedding. Just keyword heuristics.
"""

# Pine domain keywords → search targets
DOMAIN_KEYWORDS = {
    "momentum": "momentum", "trend": "trend", "volatility": "volatility",
    "volume": "volume", "price": "price",
    "skor": "score", "score": "score", "nilai": "score",
    "sektor": "sektor", "sector": "sektor",
    "energi": "energy", "energi": "energy",
    "keuangan": "financial", "financial": "financial",
    "kesehatan": "health", "health": "health",
    "dividen": "dividend", "dividend": "dividend",
    "pertumbuhan": "growth", "growth": "growth",
    "alert": "alert", "peringatan": "alert",
    "tabel": "table", "table": "table",
    "input": "input", "pengaturan": "input",
}

OBJECT_KEYWORDS = {
    "indikator": "indicator", "fungsi": "function", "function": "function",
    "variable": "variable", "variabel": "variable",
    "modul": "module", "module": "module",
    "alert": "alert", "table": "table",
}

VERB_KEYWORDS = {
    "tambah": "create", "buat": "create", "create": "create", "add": "create",
    "ubah": "modify", "edit": "modify", "modify": "modify",
    "hapus": "delete", "remove": "delete", "delete": "delete",
    "refactor": "refactor", "perbaiki": "fix", "fix": "fix", "bug": "fix",
}

FILTER_WORDS = {
    "untuk": True, "pada": True, "di": True, "dengan": True,
    "yang": True, "dan": True, "atau": True, "serta": True,
}


def extract_intent(task: str) -> dict:
    words = task.lower().split()
    result = {"verbs": [], "objects": [], "domains": [], "filters": []}

    i = 0
    while i < len(words):
        w = words[i]
        # Multi-word: "sektor energi" → "energy"
        if w in ("sektor", "sector") and i + 1 < len(words):
            result["filters"].append(f"{words[i]}_{words[i+1]}")
            i += 2
            continue
        if w in FILTER_WORDS:
            i += 1
            continue
        if w in VERB_KEYWORDS:
            result["verbs"].append(VERB_KEYWORDS[w])
        elif w in OBJECT_KEYWORDS:
            result["objects"].append(OBJECT_KEYWORDS[w])
        elif w in DOMAIN_KEYWORDS:
            result["domains"].append(DOMAIN_KEYWORDS[w])
        elif len(w) > 2:
            result["filters"].append(w)
        i += 1

    return result
