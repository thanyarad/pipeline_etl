from typing_extensions import TypedDict

class AgentState(TypedDict):
    question: str
    sparql_query: str
    query_result: str
    query_results: list
    attempts: int
    relevance: str  # Keep for backward compatibility
    sparql_error: bool
    irrelevant_query: bool
    cached_response: bool
    cache_similarity: float