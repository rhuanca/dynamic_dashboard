"""
Orchestrator Agent - LangGraph Workflow

Coordinates the multi-agent workflow using LangGraph.
Routes user queries through NLU → Database → Response Generator.
"""

from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

from agents.nlu_agent import nlu_agent
from agents.database_agent import database_agent
from agents.response_generator import response_generator
from core.specs import WidgetSpec


class AgentState(TypedDict):
    """State passed between agents in the workflow."""
    user_input: str
    intent_data: Dict[str, Any]
    db_results: Dict[str, Any]
    response: Dict[str, Any]
    widgets: List[WidgetSpec]
    message: str
    error: str | None


class Orchestrator:
    """Orchestrates the multi-agent workflow using LangGraph."""
    
    def __init__(self):
        """Initialize orchestrator with LangGraph workflow."""
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Define the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("nlu", self._nlu_node)
        workflow.add_node("database", self._database_node)
        workflow.add_node("response", self._response_node)
        
        # Define the flow
        workflow.set_entry_point("nlu")
        workflow.add_edge("nlu", "database")
        workflow.add_edge("database", "response")
        workflow.add_edge("response", END)
        
        # Compile the workflow
        return workflow.compile()
    
    def _nlu_node(self, state: AgentState) -> AgentState:
        """NLU agent node - classify intent and extract entities."""
        user_input = state["user_input"]
        
        try:
            intent_data = nlu_agent.process_query(user_input)
            state["intent_data"] = intent_data
            state["error"] = None
        except Exception as e:
            state["error"] = f"NLU Error: {str(e)}"
            state["intent_data"] = {}
        
        return state
    
    def _database_node(self, state: AgentState) -> AgentState:
        """Database agent node - execute queries."""
        if state.get("error"):
            return state
        
        intent_data = state["intent_data"]
        
        try:
            db_results = database_agent.execute_query(intent_data)
            state["db_results"] = db_results
        except Exception as e:
            state["error"] = f"Database Error: {str(e)}"
            state["db_results"] = {"success": False, "error": str(e)}
        
        return state
    
    def _response_node(self, state: AgentState) -> AgentState:
        """Response generator node - create widgets and messages."""
        if state.get("error"):
            state["widgets"] = []
            state["message"] = f"❌ {state['error']}"
            return state
        
        intent_data = state["intent_data"]
        db_results = state["db_results"]
        
        try:
            response = response_generator.generate_response(intent_data, db_results)
            state["response"] = response
            state["widgets"] = response.get("widgets", [])
            state["message"] = response.get("message", "✓ Query completed")
        except Exception as e:
            state["error"] = f"Response Error: {str(e)}"
            state["widgets"] = []
            state["message"] = f"❌ {state['error']}"
        
        return state
    
    def process_query(self, user_input: str) -> Dict[str, Any]:
        """Process user query through the multi-agent workflow.
        
        Args:
            user_input: User's natural language query
            
        Returns:
            Dictionary with widgets and response message
        """
        # Initialize state
        initial_state = {
            "user_input": user_input,
            "intent_data": {},
            "db_results": {},
            "response": {},
            "widgets": [],
            "message": "",
            "error": None
        }
        
        # Execute workflow
        final_state = self.workflow.invoke(initial_state)
        
        return {
            "widgets": final_state.get("widgets", []),
            "message": final_state.get("message", ""),
            "intent": final_state.get("intent_data", {}).get("intent", "unknown"),
            "success": final_state.get("error") is None
        }


# Global orchestrator instance
orchestrator = Orchestrator()
