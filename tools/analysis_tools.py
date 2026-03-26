def score_candidate(candidate, requirements):
    score = 0
    explanation = []

    for skill in requirements.get("must_have", []):
        if skill.lower() in candidate["text"].lower():
            score += 25
            explanation.append(f"✔ {skill}")
        else:
            explanation.append(f"✘ {skill}")

    for skill in requirements.get("nice_to_have", []):
        if skill.lower() in candidate["text"].lower():
            score += 10
            explanation.append(f"+ {skill}")

    candidate["score"] = score
    candidate["explanation"] = explanation

def multi_round_selection(candidates):
    for c in candidates:
        if c["score"] > 70:
            c["decision"] = "Hire"
        elif c["score"] > 40:
            c["decision"] = "Consider"
        else:
            c["decision"] = "Reject"
    return candidates[:10]
