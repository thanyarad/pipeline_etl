import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.memory import SessionMemory

def test_memory_storage_and_persistence():
    """Test basic memory storage and persistence functionality."""
    
    print("=== Memory Storage and Persistence Test ===\n")
    
    # Initialize memory
    try:
        memory = SessionMemory(max_history=5)
        print("✓ Memory system initialized")
        print(f"Session ID: {memory.session_id}")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return
    
    print("=" * 50)
    
    # Test conversation storage
    conversations = [
        "What is the weather like today?",
        "Tell me about Python programming",
        "What are the benefits of machine learning?",
        "Explain database systems",
        "What is artificial intelligence?"
    ]
    
    print("\n--- Testing Conversation Storage ---")
    for i, question in enumerate(conversations, 1):
        print(f"\nTurn {i}: {question}")
        
        # Simulate processing the question
        response = f"Response to: {question}"
        
        # Add to memory using existing method
        state = {
            "question": question,
            "sparql_query": "",
            "query_result": response,
            "relevance": "relevant",
            "attempts": 1,
            "sparql_error": False
        }
        memory.add_memory_entry(state)
        
        # Show memory state
        print(f"  Memory entries: {len(memory.conversation_history)}")
        print(f"  Context summary: {memory.context_summary[:50]}...")
    
    print("\n" + "=" * 50)
    print("=== Testing Memory Export/Import ===")
    
    # Export memory
    memory_data = memory.export_memory()
    print(f"✓ Memory exported with {len(memory_data['conversation_history'])} entries")
    
    # Create new memory instance and import
    new_memory = SessionMemory()
    new_memory.import_memory(memory_data)
    print(f"✓ Memory imported to new session: {new_memory.session_id}")
    
    # Verify imported data
    print(f"Imported conversations: {len(new_memory.conversation_history)}")
    print(f"Context summary: {new_memory.context_summary[:100]}...")
    
    print("\n" + "=" * 50)
    print("=== Testing Memory Reset ===")
    
    # Clear memory
    memory.clear_memory()
    print(f"✓ Memory cleared. Conversations: {len(memory.conversation_history)}")

def test_memory_operations():
    """Test various memory operations and properties."""
    
    print("\n" + "=" * 50)
    print("=== Memory Operations Test ===")
    
    try:
        memory = SessionMemory(max_history=3)
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return
    
    # Test adding conversations
    print("\n--- Adding Conversations ---")
    test_conversations = [
        ("What is Python?", "Python is a programming language"),
        ("How to install Python?", "Download from python.org"),
        ("What are Python libraries?", "Collections of reusable code")
    ]
    
    for question, answer in test_conversations:
        state = {
            "question": question,
            "sparql_query": "",
            "query_result": answer,
            "relevance": "relevant",
            "attempts": 1,
            "sparql_error": False
        }
        memory.add_memory_entry(state)
        print(f"Added: Q: {question}")
        print(f"       A: {answer}")
        print(f"       Total entries: {len(memory.conversation_history)}")
    
    print(f"\n--- Memory Properties ---")
    print(f"Session ID: {memory.session_id}")
    print(f"Total conversations: {len(memory.conversation_history)}")
    print(f"Max history: {memory.max_history}")
    print(f"Context summary: {memory.context_summary}")
    
    print(f"\n--- Conversation History ---")
    for i, entry in enumerate(memory.conversation_history, 1):
        print(f"{i}. Q: {entry.question}")
        print(f"   A: {entry.query_result}")
        print(f"   Timestamp: {entry.timestamp}")

if __name__ == "__main__":
    test_memory_storage_and_persistence()
    test_memory_operations() 