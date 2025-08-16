# Agentic AI with Memory - Knowledge Graph Assistant

## Overview

This is an advanced **Agentic AI system** that provides intelligent, context-aware interactions with knowledge graphs using Stardog. Unlike traditional chatbots, this system features autonomous decision-making, persistent memory, semantic caching, and sophisticated workflow orchestration.

## 🏗️ System Architecture

### Core Components

```
┌──────────────────────────────────────────────────────┐
│                    Agentic AI System                 │
├──────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Memory    │  │    Agent    │  │   Client    │   │
│  │   Manager   │  │    Core     │  │  (Stardog)  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
├──────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌────────────┐  ┌─────────────┐    │
│  │  Workflow   │  │    LLM     │  │  Utils &    │    │
│  │   Graph     │  │  Manager   │  │ Formatting  │    │
│  └─────────────┘  └────────────┘  └─────────────┘    │
└──────────────────────────────────────────────────────┘
```

### Component Details

#### 1. **StardogAgent** (`src/core/agent.py`)

The central intelligence unit that orchestrates all operations:

-   **Natural Language Processing**: Converts user questions to SPARQL queries
-   **Query Execution**: Manages database interactions
-   **Response Generation**: Creates human-readable answers
-   **Error Handling**: Implements retry mechanisms and fallback strategies
-   **Memory Integration**: Updates and utilizes conversation history

#### 2. **SessionMemory** (`src/core/memory.py`)

Advanced memory system with semantic capabilities:

-   **Session Persistence**: Maintains context across conversation turns
-   **Semantic Caching**: Uses LLM-based similarity to cache similar queries
-   **Schema Caching**: Stores knowledge graph schema for session efficiency
-   **Context Building**: Creates conversation summaries for better responses
-   **Memory Management**: Efficient storage with configurable limits

#### 3. **StardogClient** (`src/core/client.py`)

Database interface layer:

-   **Connection Management**: Handles Stardog database connections
-   **Query Execution**: Executes SPARQL queries with reasoning
-   **Schema Retrieval**: Fetches and formats knowledge graph schema
-   **Error Handling**: Manages database-level errors

#### 4. **Workflow Graph** (`src/workflow/graph.py`)

Intelligent routing and decision-making:

-   **Conditional Logic**: Routes requests based on context and state
-   **Cache Integration**: Checks for similar previous queries
-   **Error Recovery**: Implements retry mechanisms
-   **Result Formatting**: Routes to appropriate output formatters

#### 5. **LLM Manager** (`src/core/llm_manager.py`)

Centralized LLM provider management:

-   **Provider Abstraction**: Supports multiple LLM providers (OpenAI, Google, etc.)
-   **Configuration Management**: Handles API keys, models, and settings
-   **Default Provider**: Provides fallback to default LLM when no specific provider is requested
-   **Flexible Initialization**: Allows easy switching between different LLM providers

## 🔄 Workflow Architecture

### Processing Pipeline

```
┌─────────────────┐
│ User Querying   │ ← Get the user query as input
└─────────────────┘
     ↓
┌─────────────────┐
│ Cache Check     │ ← Check for similar previous queries
└─────────────────┘
     ↓
┌─────────────────┐
│ NL to SPARQL    │ ← Convert natural language to database query
└─────────────────┘
     ↓
┌─────────────────┐
│ Query Execution │ ← Execute against knowledge graph
└─────────────────┘
     ↓
┌─────────────────┐
│ Result Routing  │ ← Decide on output format
└─────────────────┘
     ↓
┌─────────────────┐
│ Response Gen    │ ← Generate human-readable answer
└─────────────────┘
     ↓
┌─────────────────┐
│ Memory Update   │ ← Store interaction for future use
└─────────────────┘
```

### Decision Points

1. **Cache Hit Detection**: Uses semantic similarity to identify reusable queries
2. **Relevance Filtering**: Determines if query is related to knowledge graph data
3. **Error Recovery**: Implements retry logic for failed queries
4. **Result Formatting**: Chooses between table format and natural language based on result size

## 🧠 Memory System Architecture

### Memory Components

```python
@dataclass
class MemoryEntry:
    timestamp: str           # When the interaction occurred
    question: str           # Original user question
    sparql_query: str       # Generated SPARQL query
    query_result: str       # Result summary (optimized for memory)
    attempts: int           # Number of retry attempts
    sparql_error: bool      # Whether query failed
    irrelevant_query: bool  # Whether query was relevant
    session_id: str         # Session identifier
```

### Semantic Caching Algorithm

1. **Similarity Calculation**: Uses LLM to compute semantic similarity between questions
2. **Threshold Matching**: Requires 80% similarity for cache hits
3. **Fallback Mechanism**: Uses Jaccard similarity if LLM unavailable
4. **Cache Storage**: Stores SPARQL queries for re-execution (not results)

### Memory Features

-   **Session Persistence**: Maintains context across conversation turns
-   **Schema Caching**: Stores knowledge graph schema for efficiency
-   **Context Summarization**: Creates conversation summaries for LLM context
-   **Memory Limits**: Configurable maximum history size (default: 10 entries)

## 🔧 Configuration System

### Environment Variables

```env
# Stardog Configuration
STARDOG_ENDPOINT=http://localhost:5820
STARDOG_DATABASE=your_database_name
STARDOG_USERNAME=admin
STARDOG_PASSWORD=admin

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
DEFAULT_LLM_PROVIDER=openai

# Google AI Configuration (Optional)
# GOOGLE_API_KEY=your_google_api_key
# GOOGLE_MODEL=gemini-pro

# System Configuration
MAX_HISTORY=10
SIMILARITY_THRESHOLD=0.8
RESPONSE_LENGTH_LIMIT=200
```

### Settings Management (`src/config/settings.py`)

-   **Database Configuration**: Stardog connection parameters
-   **LLM Configuration**: Model selection and API settings
-   **System Parameters**: Memory limits, similarity thresholds
-   **SPARQL Prefixes**: Common RDF prefixes for query generation

### Supported LLM Models

#### **OpenAI Models**

-   **Primary Model**: `gpt-3.5-turbo` (default)
-   **Alternative Models**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo-16k`
-   **Configuration**: Set via `OPENAI_MODEL` environment variable

#### **Google AI Models** (Currently Commented Out)

-   **Primary Model**: `gemini-pro`
-   **Configuration**: Set via `GOOGLE_MODEL` environment variable
-   **Status**: Ready for implementation, requires uncommenting in `llm_manager.py`

#### **LLM Manager Features**

-   **Provider Selection**: Choose between OpenAI and Google AI
-   **Model Configuration**: Customize temperature, base URLs, and API settings
-   **Fallback Mechanism**: Automatic fallback to default provider
-   **Extensible Design**: Easy to add new LLM providers

## 📊 Data Flow

### Query Processing Flow

1. **Input Reception**: User question received in natural language
2. **Cache Check**: System checks for semantically similar previous queries
3. **Query Generation**: LLM converts question to SPARQL using schema context
4. **Execution**: SPARQL query executed against Stardog with reasoning
5. **Result Processing**: Raw results formatted and analyzed
6. **Response Generation**: Human-readable answer created with context
7. **Memory Update**: Interaction stored for future reference

### Memory Integration

```python
# Memory is integrated at multiple points:
1. Schema caching for session efficiency
2. Query similarity checking for cache hits
3. Conversation context for better responses
4. Learning from successful/failed interactions
```

### LLM Manager Integration

```python
# LLM Manager is used throughout the system:
1. Agent initialization with flexible provider selection
2. Memory system for semantic similarity calculations
3. Query generation with configurable model parameters
4. Response generation with context-aware processing
5. Testing and development with consistent LLM instances
```

## 🚀 Usage Examples

### Basic Usage

```python
from src.core.client import StardogClient
from src.core.agent import StardogAgent
from src.core.memory import SessionMemory
from src.core.llm_manager import get_default_llm, get_llm_provider

# Initialize components
client = StardogClient(endpoint, database, username, password)

# Initialize agent with default LLM (OpenAI)
agent = StardogAgent(client)

# Or specify a different LLM provider
# agent = StardogAgent(client, llm_provider="openai")

# Initialize memory with LLM for semantic similarity
memory = SessionMemory(max_history=10, llm=agent.llm)
agent.memory = memory

# Process questions
result = agent.process_question("Show me all products with protein in keywords")
print(result)
```

### Advanced Usage with Workflow

```python
from src.workflow.graph import build_workflow

# Build and compile workflow
app = build_workflow(agent)

# Process with full workflow
result = app.invoke({
    "question": "Find products with high ratings and low prices",
    "attempts": 1
})
```

### Memory Management

```python
# Check memory status
memory_info = agent.get_memory_info()
print(f"Session: {memory_info['session_id']}")
print(f"Conversations: {memory_info['conversation_count']}")

# Clear memory
agent.clear_memory()

# Export/Import memory
memory_data = memory.export_memory()
memory.import_memory(memory_data)
```

### LLM Provider Management

```python
from src.core.llm_manager import get_llm_provider, get_available_providers

# Get available LLM providers
providers = get_available_providers()
print(f"Available providers: {providers}")

# Initialize specific LLM provider
openai_llm = get_llm_provider("openai")
google_llm = get_llm_provider("google")  # If enabled

# Custom LLM configuration
custom_config = {
    "temperature": 0.7,
    "model": "gpt-4",
    "api_key": "your_custom_key"
}
custom_llm = get_llm_provider("openai", config=custom_config)
```

## 🧪 Testing

### Test Structure

```
src/test/
├── memory_test.py          # Memory system tests
├── stardog_test.py         # Database connection tests
└── test_cache_similarity.py # Cache similarity tests
```

### Running Tests

```bash
# Windows
run_tests.bat

# Direct execution
python -m pytest src/test/
```

## 📈 Performance Features

### Optimization Strategies

1. **Schema Caching**: Reduces database calls for schema information
2. **Semantic Caching**: Avoids redundant query generation
3. **Memory Limits**: Prevents memory overflow in long sessions
4. **Result Summarization**: Stores minimal data for memory efficiency
5. **LLM Fallbacks**: Graceful degradation when LLM unavailable
6. **LLM Provider Optimization**: Efficient model selection and configuration
7. **Query Caching**: Reuses successful SPARQL queries for similar questions

### Scalability Considerations

-   **Session Isolation**: Each session has independent memory
-   **Configurable Limits**: Adjustable memory and cache sizes
-   **Error Recovery**: Robust handling of failures
-   **Resource Management**: Efficient memory usage patterns

## 🔍 Troubleshooting

### Common Issues

1. **Stardog Connection Failed**

    - Verify Stardog server is running
    - Check connection parameters in settings
    - Ensure database exists and is accessible

2. **LLM API Errors**

    - Verify API key is valid
    - Check internet connectivity
    - Ensure sufficient API credits

3. **Memory Issues**

    - Reduce `MAX_HISTORY` setting
    - Clear memory periodically
    - Monitor memory usage

4. **Query Generation Failures**
    - Check schema accessibility
    - Verify SPARQL syntax
    - Review LLM model configuration
    - Verify LLM provider settings and API keys

## 🛠️ Development

### Project Structure

```
Agentic_AI_with_memory/
├── src/
│   ├── core/              # Core system components
│   │   ├── agent.py       # Main agent logic
│   │   ├── client.py      # Database client
│   │   ├── memory.py      # Memory management
│   │   ├── llm_manager.py # LLM integration
│   │   └── models.py      # Data models
│   ├── config/            # Configuration
│   │   └── settings.py    # System settings
│   ├── workflow/          # Workflow orchestration
│   │   └── graph.py       # Processing graph
│   ├── utils/             # Utilities
│   │   └── formatting.py  # Output formatting
│   └── test/              # Test suite
├── main.py                # Entry point
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Adding New Features

1. **New Memory Types**: Extend `MemoryEntry` dataclass
2. **Additional LLM Providers**: Implement in `llm_manager.py`
3. **Custom Workflows**: Add nodes to workflow graph
4. **Enhanced Caching**: Extend similarity algorithms
5. **New LLM Models**: Add support for additional models in `llm_manager.py`
6. **Provider-Specific Features**: Implement provider-specific optimizations

## 📚 Dependencies

### Core Dependencies

-   **langchain**: LLM integration and workflow management
-   **langgraph**: Workflow orchestration and state management
-   **requests**: HTTP client for API interactions
-   **tabulate**: Table formatting for results
-   **python-dotenv**: Environment variable management

### Optional Dependencies

-   **pytest**: Testing framework
-   **jupyter**: Notebook support for development

---