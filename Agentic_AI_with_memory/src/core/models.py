from typing_extensions import TypedDict
from typing import Dict, Any

class AgentState(TypedDict):
    question: str
    sparql_query: str
    query_result: str  # General query result or error message
    query_results: Dict[str, Any]  # Raw SPARQL results with bindings
    query_result_large: Any  # Formatted results for large datasets
    query_result_small: Any  # Human readable answer for small datasets
    attempts: int
    relevance: str  # Keep for backward compatibility
    sparql_error: bool
    irrelevant_query: bool
    cached_response: bool
    cache_similarity: float