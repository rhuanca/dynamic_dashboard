"""
Response Generator Agent - Widget Creation

Converts database results into dashboard widgets and natural language responses.
"""

from typing import Dict, Any, List
import pandas as pd
from core.specs import WidgetSpec, WidgetType


class ResponseGenerator:
    """Agent responsible for generating dashboard widgets and responses."""
    
    def generate_response(
        self,
        intent_data: Dict[str, Any],
        db_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate dashboard widgets and text response from database results.
        
        Args:
            intent_data: Intent classification from NLU agent
            db_results: Results from database agent
            
        Returns:
            Dictionary with widgets and response message
        """
        if not db_results.get("success"):
            return {
                "widgets": [],
                "message": f"❌ Error: {db_results.get('error', 'Unknown error')}",
                "success": False
            }
        
        query_type = db_results.get("query_type")
        
        if query_type == "aggregate":
            return self._create_aggregate_response(intent_data, db_results)
        elif query_type == "filtered" or query_type == "status" or query_type == "maintenance":
            return self._create_table_response(intent_data, db_results)
        elif query_type == "group_by":
            return self._create_group_by_response(intent_data, db_results)
        elif query_type == "financial":
            return self._create_financial_response(intent_data, db_results)
        else:
            return {
                "widgets": [],
                "message": "✓ Query executed successfully",
                "success": True
            }
    
    def _create_aggregate_response(
        self,
        intent_data: Dict[str, Any],
        db_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create scorecard widget for aggregate queries."""
        data = db_results.get("data", {})
        value = data.get("value", 0)
        field = data.get("field", "count")
        
        # Determine title and format
        if field == "total" or "value" in intent_data.get("original_query", "").lower():
            title = "Total Equipment Value"
            formatted_value = f"${value:,.2f}"
        elif field == "count":
            title = "Equipment Count"
            formatted_value = f"{int(value):,}"
        elif field == "avg_price":
            title = "Average Price"
            formatted_value = f"${value:,.2f}"
        else:
            title = "Result"
            formatted_value = f"{value:,.2f}"
        
        widget = WidgetSpec(
            widget_id=f"aggregate_{field}",
            widget_type=WidgetType.SCORECARD,
            title=title,
            data={"value": value}
        )
        
        message = f"✓ {title}: {formatted_value}"
        
        return {
            "widgets": [widget],
            "message": message,
            "success": True
        }
    
    def _create_table_response(
        self,
        intent_data: Dict[str, Any],
        db_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create table widget for filtered queries."""
        data = db_results.get("data", [])
        row_count = db_results.get("row_count", 0)
        
        if not data:
            return {
                "widgets": [],
                "message": "No equipment found matching your criteria",
                "success": True
            }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Format currency columns
        if "current_value" in df.columns:
            df["current_value"] = df["current_value"].apply(
                lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A"
            )
        
        # Rename columns for display
        column_mapping = {
            "asset_tag": "Asset Tag",
            "name": "Equipment Name",
            "category": "Category",
            "department": "Department",
            "status": "Status",
            "current_value": "Value",
            "location": "Location",
            "assigned_to": "Assigned To",
            "condition": "Condition",
            "next_maintenance_date": "Next Maintenance",
            "last_maintenance_date": "Last Maintenance"
        }
        
        df = df.rename(columns=column_mapping)
        
        widget = WidgetSpec(
            widget_id="equipment_table",
            widget_type=WidgetType.TABLE,
            title="Equipment List",
            data=df
        )
        
        message = f"✓ Found {row_count} equipment item{'s' if row_count != 1 else ''}"
        
        return {
            "widgets": [widget],
            "message": message,
            "success": True
        }
    
    def _create_group_by_response(
        self,
        intent_data: Dict[str, Any],
        db_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create bar chart widget for group by queries."""
        data = db_results.get("data", [])
        group_field = db_results.get("group_field", "department")
        
        if not data:
            return {
                "widgets": [],
                "message": "No data found",
                "success": True
            }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Create bar chart for counts
        chart_df = df[["group_name", "count"]].copy()
        chart_df.columns = [group_field.title(), "Count"]
        
        widget = WidgetSpec(
            widget_id="group_by_chart",
            widget_type=WidgetType.BAR_CHART,
            title=f"Equipment by {group_field.title()}",
            data=chart_df
        )
        
        total_count = df["count"].sum()
        message = f"✓ Showing {len(data)} {group_field}s with {int(total_count)} total items"
        
        return {
            "widgets": [widget],
            "message": message,
            "success": True
        }
    
    def _create_financial_response(
        self,
        intent_data: Dict[str, Any],
        db_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create scorecard for financial queries."""
        data = db_results.get("data", {})
        value = data.get("value", 0)
        field = data.get("field", "total_depreciation")
        
        if field == "total_depreciation":
            title = "Total Depreciation"
            formatted_value = f"${abs(value):,.2f}"
            message = f"✓ Total Depreciation: ${abs(value):,.2f}"
        else:
            title = "Financial Result"
            formatted_value = f"${value:,.2f}"
            message = f"✓ Result: ${value:,.2f}"
        
        widget = WidgetSpec(
            widget_id="financial_metric",
            widget_type=WidgetType.SCORECARD,
            title=title,
            data={"value": abs(value)}
        )
        
        return {
            "widgets": [widget],
            "message": message,
            "success": True
        }


# Global response generator instance
response_generator = ResponseGenerator()
