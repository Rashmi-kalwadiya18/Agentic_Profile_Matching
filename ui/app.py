import streamlit as st
from matching_agent import build_graph

app = build_graph()

st.title("Agentic Profile Matching System")

jd = st.text_area("Enter Job Description")

if st.button("Analyze"):
    state = {
        "conversation_history": [],
        "job_description": jd,
        "requirements": {},
        "retrieved_candidates": [],
        "ranked_candidates": [],
        "final_candidates": [],
        "report": "",
        "feedback": ""
    }

    result = app.invoke(state)

    for c in result["final_candidates"]:
        st.subheader(c["name"])
        st.write("Score:", c["score"])
        st.write("Decision:", c["decision"])
        st.write(c["explanation"])
