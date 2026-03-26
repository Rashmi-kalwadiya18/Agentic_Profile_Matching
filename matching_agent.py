from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict

from tools.llm_tools import extract_requirements_llm
from tools.rag_tools import rag_search
from tools.analysis_tools import score_candidate, multi_round_selection

class AgentState(TypedDict):
    conversation_history: List[str]
    job_description: str
    requirements: Dict
    retrieved_candidates: List[Dict]
    ranked_candidates: List[Dict]
    final_candidates: List[Dict]
    report: str
    feedback: str

def parse_jd(state): 
    print("📄 Parsing JD...")
    return state

def extract_requirements_node(state):
    print("🧠 Extracting requirements...")
    req = extract_requirements_llm(state["job_description"])
    return {**state, "requirements": req}

def search_resumes_node(state):
    print("🔍 Searching resumes...")
    candidates = rag_search(state["job_description"])
    return {**state, "retrieved_candidates": candidates}

def rank_candidates_node(state):
    print("⚖️ Ranking candidates...")
    for c in state["retrieved_candidates"]:
        score_candidate(c, state["requirements"])
    ranked = sorted(state["retrieved_candidates"], key=lambda x: x["score"], reverse=True)
    return {**state, "ranked_candidates": ranked}

def multi_round_node(state):
    print("📊 Multi-round screening...")
    final = multi_round_selection(state["ranked_candidates"])
    return {**state, "final_candidates": final}

def generate_report_node(state):
    if not state["final_candidates"]:
        return {**state, "report": "⚠️ No matching candidates found."}
    report = "\n\n".join([
        f"{c['name']} | Score: {c['score']} | Decision: {c['decision']}\n{c['explanation']}"
        for c in state["final_candidates"]
    ])
    return {**state, "report": report}

def feedback_node(state):
    return state

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("parse_jd", parse_jd)
    graph.add_node("extract_requirements", extract_requirements_node)
    graph.add_node("search_resumes", search_resumes_node)
    graph.add_node("rank_candidates", rank_candidates_node)
    graph.add_node("multi_round", multi_round_node)
    graph.add_node("generate_report", generate_report_node)
    graph.add_node("feedback", feedback_node)

    graph.set_entry_point("parse_jd")

    graph.add_edge("parse_jd", "extract_requirements")
    graph.add_edge("extract_requirements", "search_resumes")
    graph.add_edge("search_resumes", "rank_candidates")
    graph.add_edge("rank_candidates", "multi_round")
    graph.add_edge("multi_round", "generate_report")
    graph.add_edge("generate_report", "feedback")

    return graph.compile()

if __name__ == "__main__":
    app = build_graph()

    while True:
        query = input("\nEnter Job Description (or type exit): ")
        if query.lower() == "exit":
            break

        state = {
            "conversation_history": [],
            "job_description": query,
            "requirements": {},
            "retrieved_candidates": [],
            "ranked_candidates": [],
            "final_candidates": [],
            "report": "",
            "feedback": ""
        }

        result = app.invoke(state)

        print("\n" + "="*50)
        print("🎯 MATCHING RESULT")
        print("="*50)
        print(result["report"])
