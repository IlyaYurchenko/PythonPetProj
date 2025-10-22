import re

def analyze_text(text:str) -> dict:
    score = 10
    comments = []

    bad_patterns = {
        "неуверенность": ["можливо", "не впевнений", "я не знаю", "не впевнений"],
        "негатив": ["проблема", "погано", "не працює"]
    }

    for category, words in bad_patterns.items():
        for w in words:
            if re.search(rf"\b{w}\b", text.lower()):
                score -= 2
                comments.append(f"{category} : '{w}'")
    score = max(score, 1)
    return {"comments": comments, "score": score}
