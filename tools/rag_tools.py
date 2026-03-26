from tools.file_tools import load_resumes

def rag_search(query):
    resumes = load_resumes()
    query_words = query.lower().split()
    return [r for r in resumes if any(word in r["text"].lower() for word in query_words)]
