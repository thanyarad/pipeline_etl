from tabulate import tabulate
from src.core.models import AgentState

def format_result_router(state: AgentState) -> dict:
    """Decides whether to format results as a table or generate a human-readable answer based on result size."""
    query_results = state.get("query_results", {})
    sparql_error = state.get("sparql_error", False)

    # Extract bindings from SPARQL results format if present
    if isinstance(query_results, dict):
        results = query_results.get('results', {})
        bindings = results.get('bindings', [])
    else:
        bindings = query_results if isinstance(query_results, list) else []
        
    print(f"Routing result format: {len(bindings)} results found.")
    RESULT_THRESHOLD = 15

    # Check if there's a SPARQL error (relevant query but failed to execute)
    if sparql_error:
        print("SPARQL error detected, routing to regenerate_query.")
        return {"next_step": "regenerate_query", "query_result": state["query_result"]}
    
    if not bindings:
        print("No results found, routing to generate_human_readable_answer.")
        return {"next_step": "generate_human_readable_answer", "query_result": state["query_result"]}

    if len(bindings) > RESULT_THRESHOLD:
        print("Large result set detected, formatting as structured data.")
        formatted_results = []

        # Process SPARQL bindings format
        for binding in bindings:
            row = {}
            for var, value in binding.items():
                if isinstance(value, dict):
                    # Extract value and type from SPARQL binding format
                    raw_value = value.get('value', '')
                    value_type = value.get('type', '')
                    
                    # Handle different value types
                    if value_type == 'uri' and raw_value.startswith('https://product.org/product_catalog/apparel'):
                        # Extract category name from URI
                        parts = raw_value.split('#')
                        if len(parts) > 1:
                            clean_value = parts[1]
                            # If it's purely numeric, keep it as is
                            if not clean_value.isdigit():
                                # Convert camelCase or underscores to spaces and capitalize
                                clean_value = ' '.join(word.capitalize() for word in clean_value.replace('_', ' ').split())
                            row[var] = clean_value
                        else:
                            row[var] = raw_value.split('/')[-1]
                    elif value_type == 'literal':
                        # Use literal values as-is
                        row[var] = raw_value
                    else:
                        row[var] = raw_value
                else:
                    row[var] = str(value)
            formatted_results.append(row)

        # Store both formatted results and count
        state["query_result_large"] = formatted_results
        state["query_result_small"] = None

        print(f"Data formatted successfully into {len(formatted_results)} rows.")
        return {"next_step": "update_memory", "query_result": state["query_result_small"], "query_result_large": state["query_result_large"], "query_result_small": state["query_result_small"]}
    else:
        print("Small result set, routing to generate_human_readable_answer.")
        state["query_result_large"] = None
        return {"next_step": "generate_human_readable_answer", "query_result": state["query_result"], "query_result_large": state["query_result_large"], "query_result_small": state["query_result"]}