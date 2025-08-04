"""
Test script to demonstrate LLM-based similarity detection with simple examples.
"""
import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.memory import SessionMemory
from src.core.llm_manager import get_default_llm

def test_similarity_detection():
    """Test the LLM-based similarity detection with simple examples."""
    
    # Initialize LLM and memory
    try:
        llm = get_default_llm()
        memory = SessionMemory(llm=llm)
        print("✓ Memory system initialized with LLM")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return
    
    # Add some sample questions to memory
    sample_questions = [
        "What is Python programming?",
        "How do I install Python?",
        "What are the benefits of machine learning?",
        "Explain database systems",
        "What is artificial intelligence?",
    ]
    
    print("Adding sample questions to memory...")
    for i, question in enumerate(sample_questions):
        response = f"Answer to: {question}"
        # Use existing method with proper state structure
        state = {
            "question": question,
            "sparql_query": "",
            "query_result": response,
            "relevance": "relevant",
            "attempts": 1,
            "sparql_error": False
        }
        memory.add_memory_entry(state)
    
    print(f"Added {len(sample_questions)} questions to memory.\n")
    
    # Test questions to check for similarity
    test_questions = [
        "Tell me about Python",           # Should match "What is Python programming?"
        "How to set up Python?",          # Should match "How do I install Python?"
        "What is ML?",                    # Should match "What are the benefits of machine learning?"
        "Tell me about databases",        # Should match "Explain database systems"
        "What's the weather like today?"  # Should not match anything
    ]
    
    print("Testing similarity detection...")
    print("=" * 50)
    
    for test_question in test_questions:
        print(f"\nTesting: '{test_question}'")
        print("-" * 30)
        
        # Use existing check_query_cache method
        cache_result = memory.check_query_cache(test_question, similarity_threshold=0.3)
        
        if cache_result:
            print(f"✅ SIMILARITY MATCHES FOUND!")
            print(f"   Similar question: '{cache_result['cached_question']}'")
            print(f"   Similarity score: {cache_result['similarity_score']:.2f}")
        else:
            print("❌ No similar questions found")
    
    print("\n" + "=" * 50)
    print("Similarity detection test completed!")

if __name__ == "__main__":
    test_similarity_detection() 