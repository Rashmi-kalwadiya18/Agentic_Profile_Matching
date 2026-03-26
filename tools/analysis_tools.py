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
        matched_skills = sum(
            1 for exp in c.get("explanation", [])
            if "✔" in exp or "+" in exp
        )

        if matched_skills >= 2:
            c["decision"] = "Hire"
        elif matched_skills == 1:
            c["decision"] = "Consider"
        else:
            c["decision"] = "Reject"

    return candidates[:10]
