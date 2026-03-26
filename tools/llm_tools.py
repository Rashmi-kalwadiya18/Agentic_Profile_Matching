def extract_requirements_llm(jd):
    jd = jd.lower()
    return {
        "must_have": [s for s in ["java","react","spring"] if s in jd],
        "nice_to_have": [s for s in ["aws","docker"] if s in jd]
    }
