from typing_extensions import TypedDict

class AgentState(TypedDict):
    question: str
    sparql_query: str
    query_result: str
    query_results: list
    attempts: int
    relevance: str
    sparql_error: bool