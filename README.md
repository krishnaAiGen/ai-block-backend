# AI Block Backend

A semantic search API for Kusama blockchain data using ChromaDB, OpenAI, and GraphQL. This system provides natural language querying capabilities for blockchain data through intelligent agents.

## Features

- **Semantic Search**: Uses ChromaDB with OpenAI embeddings for intelligent chunk retrieval
- **AI Agents**: Two specialized agents using OpenAI models for query generation and response formatting
- **GraphQL Integration**: Automatic query generation and execution against Kusama blockchain data
- **Natural Language Responses**: Converts complex blockchain data into readable explanations
- **Flexible Embeddings**: Supports both OpenAI and local sentence-transformers models

## Architecture

The system consists of several key components:

1. **Embedding Manager** (`source/embedding/`): Handles ChromaDB operations and semantic search
2. **GraphQL Query Agent** (`source/agents/`): Generates GraphQL queries from natural language
3. **Response Agent** (`source/agents/`): Converts GraphQL results into natural language responses
4. **FastAPI Server** (`source/api/`): Provides REST API endpoints
5. **Configuration** (`source/config/`): Centralized settings management

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-block-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env and add your OpenAI API key and model preferences
```

4. Run the server:
```bash
python main.py
```

The server will start on `http://localhost:8000`

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for AI agents and embeddings
- `OPENAI_MODEL`: Model for query generation (default: gpt-3.5-turbo)
- `OPENAI_EMBEDDING_MODEL`: Model for embeddings (default: text-embedding-ada-002)
- `GRAPHQL_ENDPOINT`: GraphQL endpoint for Kusama blockchain data
- `GRAPHQL_TIMEOUT`: GraphQL request timeout in seconds (default: 30)
- `LOG_LEVEL`: Optional logging level (default: INFO)

### Embedding Models

The system supports two embedding approaches:

1. **OpenAI Embeddings** (Default): Uses OpenAI's text-embedding-ada-002
   - Pros: High quality, no local model download
   - Cons: Requires API calls (costs per request)

2. **Local Embeddings** (Optional): Uses sentence-transformers
   - Pros: No API costs, works offline
   - Cons: Requires model download, dependency issues possible

The system automatically falls back to OpenAI embeddings if sentence-transformers is not available.

## API Endpoints

### Main Endpoints

#### POST `/answer`
Main endpoint that accepts a natural language query and returns a complete answer.

**Request Body:**
```json
{
  "query": "What are the recent large transfers on Kusama?",
  "max_chunks": 5
}
```

**Response:**
```json
{
  "answer": "Based on the recent data, here are the large transfers...",
  "graphql_query": "query { transfers(where: { amount_gte: \"1000000000000\" }) { ... } }",
  "raw_data": { "data": { "transfers": [...] } },
  "relevant_chunks": [...]
}
```

#### GET `/health`
Health check endpoint to verify system status.

#### GET `/stats`
Get system statistics including chunk count and endpoint information.

### Utility Endpoints

#### POST `/search-chunks`
Search for relevant schema chunks without executing queries.

#### POST `/generate-query`
Generate GraphQL query from natural language without execution.

## Usage Examples

### Finding Recent Transfers
```bash
curl -X POST "http://localhost:8000/answer" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the last 10 transfers on Kusama"}'
```

### Account Information
```bash
curl -X POST "http://localhost:8000/answer" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the transfer history for account GcqKn3HHodwcFc3Pg3Evcbc43m7qJNMiMv744e5WMSS7TGn?"}'
```

### Large Value Transfers
```bash
curl -X POST "http://localhost:8000/answer" \
  -H "Content-Type: application/json" \
  -d '{"query": "Find transfers larger than 1000 KSM"}'
```

## Schema Chunks

The system includes 18 pre-defined schema chunks covering:

- **Types**: Account, Transfer
- **Queries**: accountById, accounts, transferById, transfers
- **Filters**: TransferWhereInput, ordering options
- **Relationships**: Account-Transfer connections
- **Concepts**: Kusama basics, pagination
- **Examples**: Common query patterns

## Technical Details

### Embeddings
- **Default**: OpenAI text-embedding-ada-002 (1536 dimensions)
- **Alternative**: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
- ChromaDB for vector storage and similarity search
- Persistent storage in `./chroma_db` directory

### AI Agents
- **GraphQL Query Agent**: Uses gpt-3.5-turbo for query generation
- **Response Agent**: Uses gpt-3.5-turbo for natural language responses
- Both agents use schema context for accurate results

### GraphQL Endpoint
- Configurable endpoint via environment variables
- Supports complex queries with filtering, sorting, and pagination
- Handles Kusama blockchain data including accounts and transfers

## Testing

Run the test suite:
```bash
python test_api.py
```

Test OpenAI embeddings specifically:
```bash
python test_openai_embeddings.py
```

## Development

### File Structure
```
ai-block-backend/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── env.example               # Environment variables template
├── start.py                  # Quick start script
├── test_api.py               # API testing suite
├── test_openai_embeddings.py # OpenAI embeddings test
├── README.md                 # This file
└── source/                   # Source code package
    ├── __init__.py
    ├── api/                  # FastAPI application
    │   ├── __init__.py
    │   └── main.py
    ├── agents/               # AI agents
    │   ├── __init__.py
    │   └── agents.py
    ├── embedding/            # ChromaDB operations
    │   ├── __init__.py
    │   ├── embeddings.py (sentence-transformers)
    │   └── embeddings_openai.py (OpenAI embeddings)
    ├── data/                 # Data and schema chunks
    │   ├── __init__.py
    │   └── schema_chunks.py
    ├── config/               # Configuration settings
    │   ├── __init__.py
    │   └── settings.py
    └── utils/                # Utility functions
        ├── __init__.py
        └── helpers.py
```

### Adding New Schema Chunks
To add new schema chunks, edit `source/data/schema_chunks.py` and add entries to the `SCHEMA_CHUNKS` list:

```python
{
    'id': 'new-chunk-id',
    'content': 'Description of the new functionality...',
    'metadata': {
        'category': 'type|query|filter|relationship|concept|example',
        'graphqlType': 'GraphQL type name',
        'examples': ['example queries'],
        'keywords': ['searchable', 'keywords']
    }
}
```

## Performance & Costs

### OpenAI Embeddings
- **Cost**: ~$0.0001 per 1K tokens
- **Performance**: ~100ms per batch of chunks
- **Quality**: High semantic understanding

### Local Embeddings
- **Cost**: Free after setup
- **Performance**: ~10ms per batch (after model load)
- **Quality**: Good for most use cases

## License

[Add your license here]

## Contributing

[Add contributing guidelines here]