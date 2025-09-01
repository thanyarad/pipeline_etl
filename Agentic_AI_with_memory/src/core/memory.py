from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import deque
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

@dataclass
class MemoryEntry:
    """Represents a single memory entry in the conversation."""
    timestamp: str
    question: str
    sparql_query: str
    query_result: str  # Keep for backward compatibility
    query_result_large: Any  # For large result sets (tabulated)
    query_result_small: Any  # For human readable answers
    relevance: str  # Keep for backward compatibility
    attempts: int
    sparql_error: bool
    irrelevant_query: bool
    session_id: str

class SessionMemory:
    """Manages session-based memory for the agent."""
    
    # Response length limit for context - if response is longer, use SPARQL query instead
    RESPONSE_LENGTH_LIMIT = 200
    
    def __init__(self, max_history: int = 10, session_id: Optional[str] = None, llm: Optional[BaseLanguageModel] = None):
        """
        Initialize session memory.
        
        Args:
            max_history: Maximum number of conversation turns to remember
            session_id: Unique identifier for the session
            llm: LLM instance for semantic similarity checking
        """
        self.max_history = max_history
        self.session_id = session_id or self._generate_session_id()
        self.conversation_history: deque = deque(maxlen=max_history)
        self.context_summary: str = ""

        self.llm = llm
        # Add schema storage for session-long caching
        self._cached_schema: Optional[str] = None
        self._schema_formatted: bool = False
        
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def set_schema(self, schema: str) -> None:
        """
        Set the cached schema for the session.
        
        Args:
            schema: The formatted schema string
        """
        self._cached_schema = schema
        self._schema_formatted = True
        print(f"Schema cached for session: {self.session_id}")
    
    def get_schema(self) -> Optional[str]:
        """
        Get the cached schema for the session.
        
        Returns:
            The cached schema string or None if not set
        """
        return self._cached_schema
    
    def has_schema(self) -> bool:
        """
        Check if schema is cached for this session.
        
        Returns:
            True if schema is cached, False otherwise
        """
        return self._cached_schema is not None and self._schema_formatted
    

    

    
    def _find_best_match_single_call(self, question: str, valid_entries: list, similarity_threshold: float) -> Optional[Dict[str, Any]]:
        """
        Find the best matching cached question using a single LLM call.
        
        Args:
            question: The current question to check
            valid_entries: List of valid memory entries to compare against
            similarity_threshold: Minimum similarity score to consider as match
            
        Returns:
            Best match dictionary if found, None otherwise
        """
        if not self.llm:
            print("No LLM available for cache matching.")
            return None
        
        try:
            # Prepare the list of cached questions for comparison
            cached_questions = []
            for i, entry in enumerate(valid_entries):
                cached_questions.append(f"{i+1}. {entry.question}")
            
            cached_questions_text = "\n".join(cached_questions)
            
            system_prompt = """You are an expert at determining semantic similarity between questions. 
            Analyze if the current question is asking for the EXACT SAME information as any of the cached questions.
            
            IMPORTANT: Only match questions that are asking for the same specific entities or data, not just similar patterns.
            
            Consider:
            - Are they asking about the same specific entities (same names, IDs, categories)?
            - Do they have the same intent AND the same target data?
            - Would the same SPARQL query work for both questions?
            
            If you find a match that would use the same SPARQL query, respond with ONLY the number of the best matching question (e.g., "3").
            If no question matches with sufficient similarity, respond with "NONE".
            
            Examples:
            - "Show me all products" vs "What products do you have" = Match (same query)
            - "Describe category Baseball Uniforms" vs "Describe category Suits" = No match (different categories)
            - "List customers" vs "Who are the users" = Match (same query)
            - "Products under $100" vs "Show expensive items" = No match (different criteria)
            """
            
            human_prompt = f"""Current Question: {question}

Cached Questions:
{cached_questions_text}

Which cached question (if any) is semantically similar to the current question? Respond with only the number or "NONE":"""
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({}).strip()
            
            print(f"LLM response for cache matching: {response}")
            
            # Parse the response
            if response.upper() == "NONE":
                return None
            
            # Extract number from response
            import re
            match = re.search(r'\d+', response)
            if match:
                index = int(match.group()) - 1  # Convert to 0-based index
                if 0 <= index < len(valid_entries):
                    selected_entry = valid_entries[index]
                    # Calculate a high similarity score since LLM confirmed it's a match
                    similarity_score = 0.9  # High confidence since LLM selected it
                    
                    return {
                        "cached_question": selected_entry.question,
                        "cached_result": selected_entry.query_result,
                        "cached_sparql": selected_entry.sparql_query,
                        "similarity_score": similarity_score,
                        "timestamp": selected_entry.timestamp
                    }
            
            return None
                
        except Exception as e:
            print(f"Error in LLM cache matching: {e}")
            return None
    

        
    def check_query_cache(self, question: str, similarity_threshold: float = 0.8) -> Optional[Dict[str, Any]]:
        """
        Check if a similar question was asked before and return cached result using a single LLM call.
        
        Args:
            question: The current question to check
            similarity_threshold: Minimum similarity score to consider as match
            
        Returns:
            Cached result if found, None otherwise
        """
        if len(self.conversation_history) == 0:
            return None
        
        # Filter out irrelevant queries and errors
        valid_entries = [
            entry for entry in self.conversation_history 
            if not entry.irrelevant_query and not entry.sparql_error
        ]
        
        if not valid_entries:
            return None
        
        print(f"Checking cache for question: {question}")
        
        # Use single LLM call to find the best match
        best_match = self._find_best_match_single_call(question, valid_entries[-5:], similarity_threshold)
        
        if best_match:
            print(f"Query cache hit! Similarity: {best_match['similarity_score']:.2f}")
            print(f"Cached question: {best_match['cached_question']}")
        else:
            print("No cache hit found.")
        
        return best_match
    
    def add_memory_entry(self, state: Dict[str, Any]) -> None:
        """
        Add a new memory entry from the agent state.
        
        Args:
            state: The agent state dictionary
        """

        # Store SPARQL query for re-execution
        query_result = state.get("query_result", None)
        result_summary = query_result     
        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            question=state.get("question", ""),
            sparql_query=state.get("sparql_query", ""),
            query_result=result_summary,
            query_result_large=state.get("query_result_large", None),
            query_result_small=state.get("query_result_small", None),
            relevance="relevant" if not state.get("irrelevant_query", False) else "not_relevant",
            attempts=state.get("attempts", 0),
            sparql_error=state.get("sparql_error", False),
            irrelevant_query=state.get("irrelevant_query", False),
            session_id=self.session_id
        )
        self.conversation_history.append(entry)
        self._update_context_summary()
        print(f"Memory entry added: {entry.question} -> {len(self.conversation_history)} total entries")
    
    def _update_context_summary(self) -> None:
        """Update the context summary based on recent conversation history."""
        if len(self.conversation_history) == 0:
            return
            
        recent_entries = list(self.conversation_history)[-5:]  # Last 5 entries
        summary_parts = []
        
        for entry in recent_entries:
            if not entry.irrelevant_query:
                summary_parts.append(f"User asked: '{entry.question}' - SPARQL: {entry.sparql_query}...")
            else:
                summary_parts.append(f"User asked unrelated question: '{entry.question}'")
        
        self.context_summary = " | ".join(summary_parts)
    
    def get_conversation_context(self) -> str:
        """
        Get a formatted conversation context for the LLM.
        
        Returns:
            Formatted context string
        """
        if len(self.conversation_history) == 0:
            return ""
        
        context_parts = [f"Session ID: {self.session_id}"]
        context_parts.append(f"Previous conversation context: {self.context_summary}")
        
        return "\n".join(context_parts)
    
    def clear_memory(self) -> None:
        """Clear all memory for the current session."""
        self.conversation_history.clear()
        self.context_summary = ""

        self._cached_schema = None
        self._schema_formatted = False
    
    def export_memory(self) -> Dict[str, Any]:
        """Export memory data for persistence."""
        return {
            "session_id": self.session_id,
            "max_history": self.max_history,
            "conversation_history": [asdict(entry) for entry in self.conversation_history],
            "context_summary": self.context_summary,

            "cached_schema": self._cached_schema,
            "schema_formatted": self._schema_formatted
        }
    
    def set_llm(self, llm: BaseLanguageModel) -> None:
        """Set the LLM instance for semantic similarity checking."""
        self.llm = llm
    
    def import_memory(self, memory_data: Dict[str, Any]) -> None:
        """Import memory data from persistence."""
        self.session_id = memory_data.get("session_id", self.session_id)
        self.max_history = memory_data.get("max_history", self.max_history)
        self.context_summary = memory_data.get("context_summary", "")

        self._cached_schema = memory_data.get("cached_schema")
        self._schema_formatted = memory_data.get("schema_formatted", False)
        
        # Reconstruct conversation history
        self.conversation_history.clear()
        for entry_data in memory_data.get("conversation_history", []):
            entry = MemoryEntry(**entry_data)
            self.conversation_history.append(entry)
    
 