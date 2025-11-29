"""
Database Agent - SQL Operations

Handles all database operations including query generation, execution,
and result formatting. Ensures SQL safety and data integrity.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from database.db_manager import db_manager


class DatabaseAgent:
    """Agent responsible for database operations."""
    
    def __init__(self):
        """Initialize database agent."""
        self.db = db_manager
    
    def execute_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database query based on classified intent.
        
        Args:
            intent_data: Intent classification from NLU agent
            
        Returns:
            Dictionary with query results and metadata
        """
        intent = intent_data.get("intent")
        
        # Route to appropriate handler
        if intent == "aggregate_query":
            return self._handle_aggregate_query(intent_data)
        elif intent == "filtered_query":
            return self._handle_filtered_query(intent_data)
        elif intent == "status_query":
            return self._handle_status_query(intent_data)
        elif intent == "group_by_query":
            return self._handle_group_by_query(intent_data)
        elif intent == "financial_query":
            return self._handle_financial_query(intent_data)
        elif intent == "maintenance_query":
            return self._handle_maintenance_query(intent_data)
        elif intent == "insert":
            return self._handle_insert(intent_data)
        elif intent == "update":
            return self._handle_update(intent_data)
        elif intent == "delete":
            return self._handle_delete(intent_data)
        else:
            return {
                "success": False,
                "error": "Unknown intent",
                "data": None
            }
    
    
    def _handle_aggregate_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle aggregate queries like totals, counts, averages."""
        from agents.query_utils import build_where_clause, get_aggregation_query
        
        agg_type = intent_data.get("aggregation_type", "count")
        entities = intent_data.get("entities", {})
        filter_criteria = intent_data.get("filter_criteria", {})
        
        # Build WHERE clause using utility
        where_clause, params = build_where_clause(entities, filter_criteria)
        
        # Get appropriate aggregation query
        query, agg_field = get_aggregation_query(
            intent_data.get("original_query", ""),
            agg_type,
            where_clause
        )
        
        try:
            results = self.db.execute_query(query, tuple(params) if params else None)
            value = results[0][agg_field] if results else 0
            
            return {
                "success": True,
                "data": {"value": value, "field": agg_field},
                "query_type": "aggregate",
                "row_count": 1
            }
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    def _handle_filtered_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle filtered queries that return equipment lists."""
        from agents.query_utils import build_where_clause
        
        entities = intent_data.get("entities", {})
        filter_criteria = intent_data.get("filter_criteria", {})
        
        # Build WHERE clause using utility
        where_clause, params = build_where_clause(entities, filter_criteria)
        
        query = f"""
            SELECT asset_tag, name, category, department, status, 
                   current_value, location, assigned_to
            FROM equipment 
            {where_clause}
            ORDER BY name
            LIMIT 100
        """
        
        try:
            results = self.db.execute_query(query, tuple(params) if params else None)
            return {
                "success": True,
                "data": results,
                "query_type": "filtered",
                "row_count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    def _handle_status_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle status-specific queries."""
        entities = intent_data.get("entities", {})
        status = entities.get("status", "Active")
        
        query = """
            SELECT asset_tag, name, category, department, status, 
                   current_value, location, condition
            FROM equipment 
            WHERE status = ?
            ORDER BY name
            LIMIT 100
        """
        
        try:
            results = self.db.execute_query(query, (status,))
            return {
                "success": True,
                "data": results,
                "query_type": "status",
                "row_count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    
    def _handle_group_by_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle group by queries."""
        from agents.query_utils import FIELD_MAPPING
        
        group_field = intent_data.get("group_by_field", "department")
        column = FIELD_MAPPING.get(group_field, "department")
        
        query = f"""
            SELECT {column} as group_name, 
                   COUNT(*) as count,
                   SUM(current_value) as total_value
            FROM equipment
            GROUP BY {column}
            ORDER BY count DESC
        """
        
        try:
            results = self.db.execute_query(query)
            return {
                "success": True,
                "data": results,
                "query_type": "group_by",
                "group_field": column,
                "row_count": len(results)
            }
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    def _handle_financial_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle financial queries like depreciation."""
        query_text = intent_data.get("original_query", "").lower()
        
        if "depreciation" in query_text:
            # Calculate total depreciation
            query = """
                SELECT SUM(purchase_price - current_value) as total_depreciation
                FROM equipment
            """
            try:
                results = self.db.execute_query(query)
                value = results[0]["total_depreciation"] if results else 0
                return {
                    "success": True,
                    "data": {"value": value, "field": "total_depreciation"},
                    "query_type": "financial",
                    "row_count": 1
                }
            except Exception as e:
                return {"success": False, "error": str(e), "data": None}
        else:
            # Default to total value
            return self._handle_aggregate_query(intent_data)
    
    def _handle_maintenance_query(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle maintenance-related queries."""
        query_text = intent_data.get("original_query", "").lower()
        
        if "due" in query_text or "upcoming" in query_text:
            # Equipment due for maintenance
            today = datetime.now().date()
            next_month = (datetime.now() + timedelta(days=30)).date()
            
            query = """
                SELECT asset_tag, name, category, department, 
                       next_maintenance_date, last_maintenance_date
                FROM equipment
                WHERE next_maintenance_date BETWEEN ? AND ?
                ORDER BY next_maintenance_date
                LIMIT 100
            """
            
            try:
                results = self.db.execute_query(query, (today, next_month))
                return {
                    "success": True,
                    "data": results,
                    "query_type": "maintenance",
                    "row_count": len(results)
                }
            except Exception as e:
                return {"success": False, "error": str(e), "data": None}
        else:
            # General maintenance info
            return self._handle_filtered_query(intent_data)
    
    def _handle_insert(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle equipment insertion."""
        # For now, return a message that this requires more info
        return {
            "success": False,
            "error": "Insert operation requires more detailed information",
            "data": None,
            "message": "Please provide: equipment name, category, department, and purchase price"
        }
    
    def _handle_update(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle equipment updates."""
        return {
            "success": False,
            "error": "Update operation not yet implemented",
            "data": None
        }
    
    def _handle_delete(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle equipment deletion."""
        return {
            "success": False,
            "error": "Delete operation requires confirmation",
            "data": None
        }


# Global database agent instance
database_agent = DatabaseAgent()
