"""
Query Handler Utilities

Helper functions for building SQL queries with proper parameterization.
Separates query construction logic from business logic.
"""

from typing import Dict, Any, List, Tuple


def build_where_clause(
    entities: Dict[str, Any],
    filter_criteria: Dict[str, Any] = None
) -> Tuple[str, List[Any]]:
    """
    Build WHERE clause from entities and filter criteria.
    
    Args:
        entities: Dictionary of entity filters (category, department, status, etc.)
        filter_criteria: Dictionary of additional filters (price_min, price_max, etc.)
        
    Returns:
        Tuple of (where_clause_string, parameters_list)
    """
    where_conditions = []
    params = []
    
    # Entity-based filters
    entity_mappings = {
        "category": "category",
        "department": "department",
        "status": "status",
        "condition": "condition"
    }
    
    for entity_key, column_name in entity_mappings.items():
        if entity_key in entities:
            where_conditions.append(f"{column_name} = ?")
            params.append(entities[entity_key])
    
    # Price range filters
    if filter_criteria:
        if "price_min" in filter_criteria:
            where_conditions.append("current_value >= ?")
            params.append(filter_criteria["price_min"])
        
        if "price_max" in filter_criteria:
            where_conditions.append("current_value <= ?")
            params.append(filter_criteria["price_max"])
    
    # Build WHERE clause
    where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
    
    return where_clause, params


def get_aggregation_query(
    query_text: str,
    agg_type: str,
    where_clause: str
) -> Tuple[str, str]:
    """
    Determine the appropriate aggregation query based on query text.
    
    Args:
        query_text: Original user query text
        agg_type: Aggregation type hint
        where_clause: Pre-built WHERE clause
        
    Returns:
        Tuple of (sql_query, field_name)
    """
    query_lower = query_text.lower()
    
    if "value" in query_lower:
        query = f"SELECT SUM(current_value) as total FROM equipment {where_clause}"
        field = "total"
    elif "count" in query_lower or agg_type == "count":
        query = f"SELECT COUNT(*) as count FROM equipment {where_clause}"
        field = "count"
    elif "price" in query_lower:
        query = f"SELECT AVG(purchase_price) as avg_price FROM equipment {where_clause}"
        field = "avg_price"
    else:
        query = f"SELECT COUNT(*) as count FROM equipment {where_clause}"
        field = "count"
    
    return query, field


FIELD_MAPPING = {
    "department": "department",
    "category": "category",
    "status": "status",
    "location": "location",
    "condition": "condition"
}
