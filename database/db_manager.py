"""
Database manager for equipment inventory system.

Handles database connections, initialization, and common operations.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class DatabaseManager:
    """Manages SQLite database connections and operations."""
    
    def __init__(self, db_path: str = "database/equipment.db"):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def initialize_database(self) -> None:
        """Initialize database with schema from schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema_sql)
        
        print(f"✓ Database initialized at {self.db_path}")
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of dictionaries representing rows
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params or ())
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def execute_update(
        self, 
        query: str, 
        params: Optional[tuple] = None
    ) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params or ())
            return cursor.rowcount
    
    def execute_many(
        self, 
        query: str, 
        params_list: List[tuple]
    ) -> int:
        """Execute a query multiple times with different parameters.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.executemany(query, params_list)
            return cursor.rowcount
    
    def get_equipment_count(self) -> int:
        """Get total count of equipment items."""
        result = self.execute_query("SELECT COUNT(*) as count FROM equipment")
        return result[0]['count'] if result else 0
    
    def get_equipment_by_department(self) -> List[Dict[str, Any]]:
        """Get equipment count by department."""
        query = """
            SELECT department, COUNT(*) as count
            FROM equipment
            GROUP BY department
            ORDER BY count DESC
        """
        return self.execute_query(query)
    
    def get_total_equipment_value(self) -> float:
        """Get total current value of all equipment."""
        result = self.execute_query(
            "SELECT SUM(current_value) as total FROM equipment"
        )
        return result[0]['total'] if result and result[0]['total'] else 0.0
    
    def get_equipment_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get equipment filtered by status.
        
        Args:
            status: Equipment status to filter by
            
        Returns:
            List of equipment records
        """
        query = "SELECT * FROM equipment WHERE status = ? ORDER BY name"
        return self.execute_query(query, (status,))
    
    def log_audit(
        self,
        action: str,
        equipment_id: Optional[int] = None,
        user_query: Optional[str] = None,
        agent_name: Optional[str] = None,
        changes: Optional[str] = None,
        success: bool = True
    ) -> None:
        """Log an action to the audit log.
        
        Args:
            action: Description of the action
            equipment_id: ID of affected equipment
            user_query: Original user query
            agent_name: Name of the agent performing action
            changes: Description of changes made
            success: Whether the action succeeded
        """
        query = """
            INSERT INTO audit_log 
            (action, equipment_id, user_query, agent_name, changes, success)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.execute_update(
            query, 
            (action, equipment_id, user_query, agent_name, changes, success)
        )


# Global database manager instance
db_manager = DatabaseManager()
