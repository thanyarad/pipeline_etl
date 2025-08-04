from tabulate import tabulate
from src.core.models import AgentState

def format_result_router(state: AgentState) -> dict:
    """Decides whether to format results as a table or generate a human-readable answer based on result size."""
    query_results = state.get("query_results", [])
    sparql_error = state.get("sparql_error", False)
    print(f"Routing result format: {len(query_results)} results found.")
    RESULT_THRESHOLD = 15

    if sparql_error:
        print("SPARQL error detected, routing to regenerate_query.")
        return {"next_step": "regenerate_query", "query_result": state["query_result"]}
    
    if not query_results:
        print("No results found, routing to generate_human_readable_answer.")
        return {"next_step": "generate_human_readable_answer", "query_result": state["query_result"]}

    if len(query_results) > RESULT_THRESHOLD:
        print("Large result set detected, formatting as table.")
        headers = list(query_results[0].keys())
        table_data = [[str(result.get(h, {}).get('value', "")) for h in headers] for result in query_results[:50]]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        if len(query_results) > 50:
            table += f"\n\n*Showing first 50 of {len(query_results)} results.*"
        state["query_result"] = table
        print("Table formatted successfully.")
        return {"next_step": "update_memory", "query_result": table}  # Changed: route to update_memory instead of END
    else:
        print("Small result set, routing to generate_human_readable_answer.")
        return {"next_step": "generate_human_readable_answer", "query_result": state["query_result"]}