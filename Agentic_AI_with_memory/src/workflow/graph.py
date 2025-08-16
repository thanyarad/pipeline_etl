from langgraph.graph import StateGraph, END
from src.core.models import AgentState
from src.core.agent import StardogAgent
from src.utils.formatting import format_result_router

def build_workflow(agent: StardogAgent) -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("check_query_cache", agent.check_query_cache)
    workflow.add_node("convert_to_sparql", agent.convert_nl_to_sparql)
    workflow.add_node("execute_sparql", agent.execute_sparql)
    workflow.add_node("generate_human_readable_answer", agent.generate_human_readable_answer)
    workflow.add_node("regenerate_query", agent.regenerate_query)
    workflow.add_node("generate_irrelevant_response", agent.generate_irrelevant_response)
    workflow.add_node("end_max_iterations", lambda state: {"query_result": "Please try again."})
    workflow.add_node("format_result_router", format_result_router)
    workflow.add_node("update_memory", agent.update_memory)

    # Define edges with conditional routing for cache hits
    workflow.add_conditional_edges(
        "check_query_cache",
        lambda state: "execute_sparql" if state.get("cached_response", False) else "convert_to_sparql",
        {
            "convert_to_sparql": "convert_to_sparql",
            "execute_sparql": "execute_sparql",  # Direct path for cached SPARQL queries
        },
    )
    
    workflow.add_conditional_edges(
        "convert_to_sparql",
        lambda state: "generate_irrelevant_response" if state.get("irrelevant_query", False) else "execute_sparql",
        {
            "execute_sparql": "execute_sparql",
            "generate_irrelevant_response": "generate_irrelevant_response",
        },
    )
    workflow.add_edge("execute_sparql", "format_result_router")
    workflow.add_conditional_edges(
        "format_result_router",
        lambda state: state.get("next_step", "update_memory"),
        {
            "generate_human_readable_answer": "generate_human_readable_answer",
            "regenerate_query": "regenerate_query",
            "generate_irrelevant_response": "generate_irrelevant_response",
            "update_memory": "update_memory",
        },
    )
    workflow.add_conditional_edges(
        "regenerate_query",
        lambda state: "convert_to_sparql" if state["attempts"] < 3 else "end_max_iterations",
        {
            "convert_to_sparql": "convert_to_sparql",
            "end_max_iterations": "end_max_iterations",
        },
    )
    workflow.add_edge("generate_human_readable_answer", "update_memory")
    workflow.add_edge("generate_irrelevant_response", "update_memory")
    workflow.add_edge("end_max_iterations", "update_memory")
    workflow.add_edge("update_memory", END)
    workflow.set_entry_point("check_query_cache")
    
    return workflow.compile()