# Equipment Inventory Multi-Agent System - Setup Instructions

## Prerequisites
- Python 3.11+
- OpenAI API key

## Setup Steps

### 1. Install Dependencies
```bash
cd /home/renan/src-mydev/dynamic_dashboard
uv sync
```

### 2. Configure OpenAI API Key
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Initialize Database (if not already done)
```bash
uv run python database/sample_data.py
```

This will create:
- SQLite database at `database/equipment.db`
- ~2000 sample equipment records
- Total value: ~$37M across 10 departments

### 4. Run the Application
```bash
uv run streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Example Queries

Try these natural language queries:

**Aggregate Queries:**
- "What's our total equipment value?"
- "How many equipment items do we have?"
- "Count of IT equipment"

**Filtered Queries:**
- "Show me all laptops"
- "Equipment over $10,000"
- "Show IT department equipment"

**Status Queries:**
- "Show equipment out of service"
- "Active equipment"
- "Equipment in maintenance"

**Group By Queries:**
- "Show equipment by department"
- "Equipment count by category"
- "Group by status"

**Maintenance Queries:**
- "Equipment due for maintenance this month"
- "Show maintenance schedule"

**Financial Queries:**
- "What's our total depreciation?"
- "Equipment depreciation"

## Architecture

The system uses 4 agents coordinated by LangGraph:

1. **NLU Agent** - Classifies intent using OpenAI structured outputs
2. **Database Agent** - Generates and executes SQL queries
3. **Response Generator** - Creates dashboard widgets
4. **Orchestrator** - Coordinates the workflow

## Troubleshooting

**Error: "OpenAI API key not found"**
- Make sure `.env` file exists with `OPENAI_API_KEY`

**Error: "Database not found"**
- Run `uv run python database/sample_data.py`

**Error: "Module not found"**
- Run `uv sync` to install dependencies
