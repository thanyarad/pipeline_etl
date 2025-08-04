from typing import List, Dict, Any, Optional
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
    query_result: str
    relevance: str
    attempts: int
    sparql_error: bool
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
        self.user_preferences: Dict[str, Any] = {}
        self.llm = llm
        
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _check_semantic_similarity(self, question1: str, question2: str) -> float:
        """
        Use LLM to check semantic similarity between two questions.
        
        Args:
            question1: First question
            question2: Second question
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        if not self.llm:
            # Fallback to simple similarity if no LLM available
            return self._simple_similarity(question1, question2)
        
        try:
            system_prompt = """You are an expert at determining semantic similarity between questions. 
            Analyze if two questions are asking for the same information, even if they use different words or phrasing.
            
            Consider:
            - Are they asking about the same entities, relationships, or data?
            - Do they have the same intent and expected outcome?
            - Are they requesting similar information from a knowledge graph?
            
            Respond with only a number between 0.0 and 1.0, where:
            - 1.0 = Exactly the same question (same meaning, same intent)
            - 0.8-0.9 = Very similar questions (same intent, slightly different phrasing)
            - 0.6-0.7 = Similar questions (related intent, different approach)
            - 0.4-0.5 = Somewhat related questions
            - 0.0-0.3 = Different questions (different intent or topic)
            
            Examples:
            "Show me all products" vs "What products do you have" = 0.9
            "List customers" vs "Who are the users" = 0.8
            "Products under $100" vs "Show expensive items" = 0.3
            """
            
            human_prompt = f"""Question 1: {question1}
Question 2: {question2}

Rate the semantic similarity (0.0 to 1.0):"""
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({})
            
            # Extract numeric value from response
            import re
            match = re.search(r'0\.\d+|1\.0', response.strip())
            if match:
                return float(match.group())
            else:
                # Fallback if parsing fails
                return self._simple_similarity(question1, question2)
                
        except Exception as e:
            print(f"Error in LLM similarity check: {e}")
            # Fallback to simple similarity
            return self._simple_similarity(question1, question2)
    
    def _simple_similarity(self, question1: str, question2: str) -> float:
        """
        Fallback simple similarity method using Jaccard similarity.
        
        Args:
            question1: First question
            question2: Second question
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        question1_lower = question1.lower().strip()
        question2_lower = question2.lower().strip()
        
        # Exact match
        if question1_lower == question2_lower:
            return 1.0
        
        question1_words = set(question1_lower.split())
        question2_words = set(question2_lower.split())
        
        if len(question1_words) == 0 or len(question2_words) == 0:
            return 0.0
        
        # Jaccard similarity
        intersection = len(question1_words.intersection(question2_words))
        union = len(question1_words.union(question2_words))
        similarity = intersection / union if union > 0 else 0
        
        # Bonus for length similarity
        length_diff = abs(len(question1_words) - len(question2_words))
        length_similarity = 1.0 / (1.0 + length_diff)
        similarity = (similarity + length_similarity) / 2
        
        return similarity
    
    def check_query_cache(self, question: str, similarity_threshold: float = 0.8) -> Optional[Dict[str, Any]]:
        """
        Check if a similar question was asked before and return cached result using LLM-based similarity.
        
        Args:
            question: The current question to check
            similarity_threshold: Minimum similarity score to consider as match
            
        Returns:
            Cached result if found, None otherwise
        """
        if len(self.conversation_history) == 0:
            return None
        
        best_match = None
        best_score = 0
        
        print(f"Checking cache for question: {question}")
        
        for entry in self.conversation_history:
            if entry.relevance != "relevant" or entry.sparql_error:
                continue
            
            # Use LLM-based semantic similarity
            similarity = self._check_semantic_similarity(question, entry.question)
            
            print(f"Similarity with '{entry.question}': {similarity:.2f}")
            
            if similarity > best_score and similarity >= similarity_threshold:
                best_score = similarity
                best_match = {
                    "cached_question": entry.question,
                    "cached_result": entry.query_result,
                    "cached_sparql": entry.sparql_query,
                    "similarity_score": similarity,
                    "timestamp": entry.timestamp
                }
        
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
        # Store only essential information to save memory
        # Store SPARQL query for re-execution and minimal result info
        raw_results = state.get("query_results", [])
        query_result = state.get("query_result", "")
        
        # Create a minimal result summary for memory efficiency
        if raw_results:
            result_summary = f"Found {len(raw_results)} results"
        else:
            result_summary = query_result[:100] + "..." if len(query_result) > 100 else query_result
        
        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            question=state.get("question", ""),
            sparql_query=state.get("sparql_query", ""),
            query_result=result_summary,  # Store minimal summary to save memory
            relevance=state.get("relevance", ""),
            attempts=state.get("attempts", 0),
            sparql_error=state.get("sparql_error", False),
            session_id=self.session_id
        )
        self.conversation_history.append(entry)
        self._update_context_summary()
        print(f"Memory entry added: {entry.question} -> {len(self.conversation_history)} total entries")
    
    def _update_context_summary(self) -> None:
        """Update the context summary based on recent conversation history."""
        if len(self.conversation_history) == 0:
            return
            
        recent_entries = list(self.conversation_history)[-3:]  # Last 3 entries
        summary_parts = []
        
        for entry in recent_entries:
            if entry.relevance == "relevant":
                # Use SPARQL query if response is too long, otherwise use truncated response
                if len(entry.query_result) > self.RESPONSE_LENGTH_LIMIT:
                    summary_parts.append(f"User asked: '{entry.question}' - SPARQL: {entry.sparql_query[:100]}...")
                else:
                    summary_parts.append(f"User asked: '{entry.question}' - Result: {entry.query_result[:100]}...")
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
        
        # Add recent successful queries for reference
        successful_queries = [
            entry for entry in self.conversation_history 
            if entry.relevance == "relevant" and not entry.sparql_error
        ][-2:]  # Last 2 successful queries
        
        if successful_queries:
            context_parts.append("Recent successful queries:")
            for entry in successful_queries:
                context_parts.append(f"- Q: {entry.question}")
                # Use SPARQL query if response is too long, otherwise use truncated response
                if len(entry.query_result) > self.RESPONSE_LENGTH_LIMIT:
                    context_parts.append(f"  SPARQL: {entry.sparql_query[:150]}...")
                else:
                    context_parts.append(f"  A: {entry.query_result[:150]}...")
        
        return "\n".join(context_parts)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences based on conversation history."""
        if len(self.conversation_history) == 0:
            return {}
        
        # Analyze conversation patterns
        preferences = {
            "query_complexity": self._analyze_query_complexity(),
            "preferred_detail_level": self._analyze_detail_preference()
        }
        
        return preferences
    

    
    def _analyze_query_complexity(self) -> str:
        """Analyze the complexity level of user queries."""
        if len(self.conversation_history) == 0:
            return "unknown"
        
        complex_queries = 0
        total_queries = 0
        
        for entry in self.conversation_history:
            if entry.relevance == "relevant":
                total_queries += 1
                # Simple complexity detection
                if len(entry.question.split()) > 10 or "and" in entry.question.lower():
                    complex_queries += 1
        
        if total_queries == 0:
            return "unknown"
        
        complexity_ratio = complex_queries / total_queries
        if complexity_ratio > 0.7:
            return "high"
        elif complexity_ratio > 0.3:
            return "medium"
        else:
            return "low"
    
    def _analyze_detail_preference(self) -> str:
        """Analyze user's preference for detail level in responses."""
        if len(self.conversation_history) == 0:
            return "medium"
        
        detail_levels = []
        for entry in self.conversation_history:
            if entry.relevance == "relevant" and entry.query_result:
                result_length = len(entry.query_result)
                if result_length > 500:
                    detail_levels.append("high")
                elif result_length > 200:
                    detail_levels.append("medium")
                else:
                    detail_levels.append("low")
        
        if not detail_levels:
            return "medium"
        
        # Return most common detail level
        from collections import Counter
        return Counter(detail_levels).most_common(1)[0][0]
    
    def clear_memory(self) -> None:
        """Clear all memory for the current session."""
        self.conversation_history.clear()
        self.context_summary = ""
        self.user_preferences = {}
    
    def export_memory(self) -> Dict[str, Any]:
        """Export memory data for persistence."""
        return {
            "session_id": self.session_id,
            "max_history": self.max_history,
            "conversation_history": [asdict(entry) for entry in self.conversation_history],
            "context_summary": self.context_summary,
            "user_preferences": self.user_preferences
        }
    
    def set_llm(self, llm: BaseLanguageModel) -> None:
        """Set the LLM instance for semantic similarity checking."""
        self.llm = llm
    
    def import_memory(self, memory_data: Dict[str, Any]) -> None:
        """Import memory data from persistence."""
        self.session_id = memory_data.get("session_id", self.session_id)
        self.max_history = memory_data.get("max_history", self.max_history)
        self.context_summary = memory_data.get("context_summary", "")
        self.user_preferences = memory_data.get("user_preferences", {})
        
        # Reconstruct conversation history
        self.conversation_history.clear()
        for entry_data in memory_data.get("conversation_history", []):
            entry = MemoryEntry(**entry_data)
            self.conversation_history.append(entry)
    
 