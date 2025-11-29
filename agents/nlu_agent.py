"""
NLU Agent - Natural Language Understanding

Classifies user intent and extracts entities from natural language queries.
Uses OpenAI structured outputs for reliable intent classification.
"""

import os
from typing import Dict, Any, Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class QueryIntent(str, Enum):
    """Possible user intents."""
    AGGREGATE_QUERY = "aggregate_query"  # Total value, counts, sums
    FILTERED_QUERY = "filtered_query"    # Show equipment matching criteria
    STATUS_QUERY = "status_query"        # Filter by status
    GROUP_BY_QUERY = "group_by_query"    # Group by department, category, etc.
    FINANCIAL_QUERY = "financial_query"  # Depreciation, costs, values
    INSERT = "insert"                    # Add new equipment
    UPDATE = "update"                    # Modify existing equipment
    DELETE = "delete"                    # Remove equipment
    MAINTENANCE_QUERY = "maintenance_query"  # Maintenance-related queries
    UNKNOWN = "unknown"                  # Cannot determine intent


class IntentClassification(BaseModel):
    """Structured output for intent classification."""
    intent: QueryIntent = Field(description="The classified intent of the user query")
    confidence: float = Field(description="Confidence score between 0 and 1", ge=0, le=1)
    
    # Extracted entities as optional string fields
    department: Optional[str] = Field(default=None, description="Department name if mentioned")
    category: Optional[str] = Field(default=None, description="Equipment category if mentioned")
    status: Optional[str] = Field(default=None, description="Equipment status if mentioned")
    condition: Optional[str] = Field(default=None, description="Equipment condition if mentioned")
    equipment_name: Optional[str] = Field(default=None, description="Specific equipment name or type")
    
    # Filter criteria
    price_min: Optional[float] = Field(default=None, description="Minimum price filter")
    price_max: Optional[float] = Field(default=None, description="Maximum price filter")
    
    # Aggregation and grouping
    aggregation_type: Optional[str] = Field(
        default=None,
        description="Type of aggregation: sum, count, avg, min, max"
    )
    group_by_field: Optional[str] = Field(
        default=None,
        description="Field to group by: department, category, status, location"
    )
    
    explanation: str = Field(description="Brief explanation of the classification")


class NLUAgent:
    """Natural Language Understanding Agent using OpenAI."""
    
    def __init__(self):
        """Initialize NLU agent with OpenAI model."""
        self.model = ChatOpenAI(
            model=os.getenv("AGENT_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("AGENT_TEMPERATURE", "0.1"))
        )
        
        # Create structured output model
        self.structured_llm = self.model.with_structured_output(IntentClassification)
    
    def classify_intent(self, user_query: str) -> IntentClassification:
        """Classify user intent and extract entities.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            IntentClassification with intent, entities, and metadata
        """
        system_prompt = """You are an expert at understanding equipment inventory queries.

Analyze the user's query and classify their intent. Extract relevant entities and filter criteria.

Available intents:
- aggregate_query: User wants totals, sums, counts (e.g., "total equipment value", "how many laptops")
- filtered_query: User wants to see equipment matching criteria (e.g., "show all laptops", "equipment over $10,000")
- status_query: User wants to filter by status (e.g., "out of service equipment", "active items")
- group_by_query: User wants data grouped (e.g., "equipment by department", "count by category")
- financial_query: User asks about money/depreciation (e.g., "depreciation this quarter", "maintenance costs")
- maintenance_query: User asks about maintenance (e.g., "equipment due for maintenance", "maintenance schedule")
- insert: User wants to add new equipment (e.g., "add a new laptop", "register equipment")
- update: User wants to modify equipment (e.g., "update status", "change location")
- delete: User wants to remove equipment (e.g., "delete equipment", "remove item")
- unknown: Cannot determine intent

Extract entities like:
- department: IT, Engineering, Manufacturing, etc.
- category: IT Equipment, Manufacturing Equipment, Office Equipment, Medical Devices, Vehicles, Tools
- status: Active, In Maintenance, Out of Service, Retired, On Loan
- condition: Excellent, Good, Fair, Poor, Needs Repair
- price_range: min and max values
- date_range: start and end dates
- equipment_name: specific equipment names or types

For filter criteria, extract SQL-compatible filters.
For aggregations, identify the type (sum, count, avg) and field.
For group by queries, identify the grouping field."""

        user_message = f"User query: {user_query}"
        
        messages = [
            ("system", system_prompt),
            ("human", user_message)
        ]
        
        result = self.structured_llm.invoke(messages)
        return result
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process user query and return structured command.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Dictionary with intent, entities, and database command info
        """
        classification = self.classify_intent(user_query)
        
        # Build entities dict from optional fields
        entities = {}
        if classification.department:
            entities["department"] = classification.department
        if classification.category:
            entities["category"] = classification.category
        if classification.status:
            entities["status"] = classification.status
        if classification.condition:
            entities["condition"] = classification.condition
        if classification.equipment_name:
            entities["equipment_name"] = classification.equipment_name
        
        # Build filter criteria
        filter_criteria = {}
        if classification.price_min is not None:
            filter_criteria["price_min"] = classification.price_min
        if classification.price_max is not None:
            filter_criteria["price_max"] = classification.price_max
        
        return {
            "intent": classification.intent.value,
            "confidence": classification.confidence,
            "entities": entities,
            "filter_criteria": filter_criteria if filter_criteria else None,
            "aggregation_type": classification.aggregation_type,
            "group_by_field": classification.group_by_field,
            "explanation": classification.explanation,
            "original_query": user_query
        }


# Global NLU agent instance
nlu_agent = NLUAgent()
