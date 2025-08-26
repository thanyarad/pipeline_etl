from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config.settings import PREFIXES, EXECUTE_FROM_STARDOG
from src.core.client import StardogClient
from src.core.models import AgentState
from src.core.memory import SessionMemory
from src.core.llm_manager import get_default_llm, get_llm_provider

class StardogAgent:
    def __init__(self, client: StardogClient, memory: SessionMemory = None, llm_provider: str = None):
        self.client = client
        self.llm = self._initialize_llm(llm_provider)
        self.memory = memory or SessionMemory(llm=self.llm)
        # Initialize schema for the session
        self._initialize_session_schema()

    def _initialize_llm(self, llm_provider: str = None):
        """Initialize LLM using the specified provider or default."""
        if llm_provider:
            return get_llm_provider(llm_provider)
        else:
            return get_default_llm()

    def _initialize_session_schema(self):
        """Initialize the schema for the session and cache it in memory."""
        if not self.memory.has_schema():
            print("Initializing schema for new session...")
            formatted_schema = self.client.get_formatted_schema()
            if formatted_schema:
                self.memory.set_schema(formatted_schema)
                print("Schema initialized and cached for session.")
            else:
                print("Warning: Failed to initialize schema for session.")
        else:
            print("Using cached schema from existing session.")

    def get_kg_schema(self):
        """Get the cached schema from memory for the session."""
        schema = self.memory.get_schema()
        if schema is None:
            # Fallback: try to get schema if not cached
            print("Schema not cached, fetching from database...")
            formatted_schema = self.client.get_formatted_schema()
            if formatted_schema:
                self.memory.set_schema(formatted_schema)
                return formatted_schema
            else:
                print("Error: Could not retrieve schema from database.")
                return None
        return schema

    def refresh_schema(self):
        """Refresh the schema cache by fetching from database."""
        print("Refreshing schema cache...")
        formatted_schema = self.client.get_formatted_schema()
        if formatted_schema:
            self.memory.set_schema(formatted_schema)
            print("Schema cache refreshed successfully.")
            return True
        else:
            print("Error: Failed to refresh schema cache.")
            return False

    def check_query_cache(self, state: AgentState) -> AgentState:
        """Check if the question can be answered from cache."""
        question = state["question"]
        cached_result = self.memory.check_query_cache(question)
        
        if cached_result:
            print(f"Using cached SPARQL query for: {question}")
            # Cache the SPARQL query but don't set the result
            # This allows re-execution to get fresh data
            state["sparql_query"] = cached_result['cached_sparql']
            state["cached_response"] = True
            state["cache_similarity"] = cached_result['similarity_score']
        else:
            print(f"No cache hit for: {question}")
            state["cached_response"] = False
        
        return state



    def convert_nl_to_sparql(self, state: AgentState) -> AgentState:
        question = state["question"]
        schema = self.get_kg_schema()
        conversation_context = self.memory.get_conversation_context()
        print(f"Converting question to SPARQL: {question}")
        
        system = """You are an assistant that converts natural language questions into SPARQL queries based on the following knowledge graph schema:

{schema}

{context}

Understand the relationships between the classes and properties.
Include FROM {from_data} in the SPARQL query after the SELECT clause and before the WHERE clause.

Use these common prefixes:
{prefixes}

Consider the conversation context when generating queries. If this is a follow-up question, reference previous successful queries for consistency.

IMPORTANT: Only respond with "IRRELEVANT_QUERY" if the question is completely unrelated to the knowledge graph data (e.g., weather, sports, general knowledge, etc.). If the question is related to the data but you're unsure about the exact query structure, still attempt to generate a SPARQL query.

Provide only the SPARQL query without any explanations. Use appropriate variable names and include necessary JOINs via triple patterns.
""".format(schema=schema, context=conversation_context if conversation_context else "", 
           prefixes=PREFIXES, from_data=EXECUTE_FROM_STARDOG)
        
        convert_prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "Question: {question}")])
        sparql_generator = convert_prompt | self.llm | StrOutputParser()
        try:
            sparql_query = sparql_generator.invoke({"question": question})
            sparql_query = sparql_query.strip()
            
            # Check if the LLM determined the query is irrelevant
            if "IRRELEVANT_QUERY" in sparql_query.upper():
                print("LLM determined query is irrelevant to knowledge graph schema.")
                state["sparql_query"] = ""
                state["sparql_error"] = False
                state["irrelevant_query"] = True
                return state
            
            if sparql_query.startswith("```sparql"):
                sparql_query = sparql_query.replace("```sparql", "").replace("```", "").strip()
            elif sparql_query.startswith("```"):
                sparql_query = sparql_query.replace("```", "").strip()
            if not sparql_query.startswith("PREFIX"):
                sparql_query = PREFIXES + "\n" + sparql_query
            state["sparql_query"] = sparql_query
            state["sparql_error"] = False
            state["irrelevant_query"] = False
            print(f"Generated SPARQL query: {state['sparql_query']}")
        except Exception as e:
            print(f"Error generating SPARQL: {str(e)}")
            # This is a technical error, not an irrelevant query
            state["sparql_query"] = "SELECT 'Error generating SPARQL query' as ?error WHERE {}"
            state["sparql_error"] = True
            state["irrelevant_query"] = False
        return state

    def execute_sparql(self, state: AgentState) -> AgentState:
        sparql_query = state["sparql_query"].strip()
        print(f"Executing SPARQL query: {sparql_query}")
        try:
            result = self.client.query(sparql_query, use_reasoning=True)
            print("Executed Result", result)
            if result and isinstance(result, dict):
                # Store the complete SPARQL result including head and results
                state["query_results"] = result
                
                # Extract bindings for result count
                bindings = result.get('results', {}).get('bindings', [])
                if bindings:
                    formatted_result = f"Found {len(bindings)} results."
                else:
                    formatted_result = "No results found."
                    
                state["query_result"] = formatted_result
                state["sparql_error"] = False
                print("SPARQL SELECT query executed successfully.")
            else:
                state["query_result"] = "Query executed but returned no data."
                state["sparql_error"] = False
                print("SPARQL query executed successfully.")
        except Exception as e:
            state["query_result"] = f"Error executing SPARQL query: {str(e)}"
            state["sparql_error"] = True
            print(f"Error executing SPARQL query: {str(e)}")
        return state

    def generate_human_readable_answer(self, state: AgentState) -> AgentState:
        sparql = state["sparql_query"].replace("{", "{{").replace("}", "}}")
        result = str(state["query_result"]).replace("{", "{{").replace("}", "}}")
        query_results = state.get("query_results", [])
        sparql_error = state.get("sparql_error", False)
        conversation_context = self.memory.get_conversation_context()
        print("Generating a human-readable answer.")
        
        system = """You are an assistant that converts SPARQL query results into clear, natural language responses for the knowledge graph system.

{context}

Consider the conversation context when formulating responses. If this is a follow-up question, reference previous information appropriately.
""".format(context=conversation_context if conversation_context else "")
        
        if sparql_error:
            generate_prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", f"""SPARQL Query:\n{{sparql}}\n\nResult:\n\n{{result}}\n\nFormulate a clear and understandable error message informing about the issue."""),
            ])
        elif not query_results:
            generate_prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", f"""SPARQL Query:\n{{sparql}}\n\nResult:\n\n{{result}}\n\nFormulate a clear and understandable answer to the original question and mention that no results were found for their query."""),
            ])
        else:
            generate_prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", f"""SPARQL Query:\n{{sparql}}\n\nResult:\n\n{{result}}\n\nFormulate a clear and understandable answer to the original question and present the information in a natural way. For purchases, mention product names and relevant details like prices or quantities."""),
            ])
        human_response = generate_prompt | self.llm | StrOutputParser()
        answer = human_response.invoke({"sparql": sparql, "result": result})
        state["query_result_small"] = answer
        state["query_result"] = answer  # Keep for backward compatibility
        print("Generated human-readable answer.")
        return state

    def regenerate_query(self, state: AgentState) -> AgentState:
        question = state["question"]
        print("Regenerating the SPARQL query by rewriting the question.")
        system = """You are an assistant that reformulates an original question to enable more precise SPARQL queries for knowledge graphs. Ensure that all necessary details, such as entity relationships and properties, are preserved to retrieve complete and accurate data.
        
        Return only the reformulated question, nothing else."""
        rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", f"Original Question: {question}\nReformulate the question to enable more precise SPARQL queries, ensuring all necessary details are preserved."),
        ])
        rewriter = rewrite_prompt | self.llm | StrOutputParser()
        try:
            rewritten_question = rewriter.invoke({})
            state["question"] = rewritten_question.strip()
            state["attempts"] += 1
            print(f"Rewritten question: {state['question']}")
        except Exception as e:
            print(f"Error rewriting question: {str(e)}")
            state["attempts"] += 1
        return state

    def generate_irrelevant_response(self, state: AgentState) -> AgentState:
        """Generate a hardcoded response for irrelevant queries."""
        print("Query is not relevant to the knowledge graph schema.")
        state["query_result"] = "I'm sorry, but I cannot process this query as it's not related to the knowledge graph data. Please ask questions about the available data in the knowledge graph for products."
        print("Generated hardcoded irrelevant response.")
        return state
    
    def update_memory(self, state: AgentState) -> AgentState:
        """Update the agent's memory with the current interaction."""
        print("Agent State : ", state)
        self.memory.add_memory_entry(state)
        print(f"Memory updated for session: {self.memory.session_id}")
        return state
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get information about the current memory state."""
        return {
            "session_id": self.memory.session_id,
            "conversation_count": len(self.memory.conversation_history),
            "context_summary": self.memory.context_summary,
            "schema_cached": self.memory.has_schema()
        }
    
    def clear_memory(self) -> None:
        """Clear the agent's memory."""
        self.memory.clear_memory()
        print("Memory cleared.")