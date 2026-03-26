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
        explanation = c.get("explanation", [])

        # Count matches
        matched = sum(1 for exp in explanation if "✔" in exp or "+" in exp)
        missing = sum(1 for exp in explanation if "✗" in exp or "X" in exp)

        # 🚨 IMPORTANT RULE
        if missing > 0:
            c["decision"] = "Reject"
        elif matched >= 2:
            c["decision"] = "Hire"
        elif matched == 1:
            c["decision"] = "Consider"
        else:
            c["decision"] = "Reject"

    return candidates[:10]
