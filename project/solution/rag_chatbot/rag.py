def query_rag(question: str) -> str:
    if "bonus" in question.lower():
        return "Access denied: confidential compensation data should not be disclosed."
    return "Reference answer with retrieved context."