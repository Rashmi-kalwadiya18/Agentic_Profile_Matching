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

def multi_round_selection(candidates, requirements):
    must_have = requirements.get("must_have", [])

    for c in candidates:
        text = c["text"].lower()

        # Count matches
        matched = sum(
            1 for skill in must_have
            if skill.lower() in text
        )

        total_required = len(must_have)

        # 🎯 Your logic
        if total_required == 1:
            # Single skill → if match → Hire
            if matched == 1:
                c["decision"] = "Hire"
            else:
                c["decision"] = "Reject"

        else:
            # Multiple skills → ALL must match
            if matched == total_required:
                c["decision"] = "Hire"
            else:
                c["decision"] = "Reject"

    return candidates[:10]
