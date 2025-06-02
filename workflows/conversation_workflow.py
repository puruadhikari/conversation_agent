from langgraph.graph import StateGraph, END
from typing import Any
from schemas.schemas import ConversationAnalysisState
from classification.journey_classifier import classify_journey_and_subjourney
from retrieval.document_retriever import retrieve_documents
from cross_sell.cross_sell_suggester import suggest_cross_sell
from utils.graph_utils import save_workflow_graph_png


# from conversation_agent.utils.graph_utils import save_workflow_graph_png # If you need to save graph

def build_conversation_workflow() -> Any:  # Using Any for compiled graph type
    """
    Builds and returns the compiled LangGraph workflow for conversation analysis.
    """
    workflow = StateGraph(ConversationAnalysisState)

    # Define the nodes
    workflow.add_node("classify_journey", classify_journey_and_subjourney)
    workflow.add_node("retrieve_documents", retrieve_documents)
    workflow.add_node("suggest_cross_sell", suggest_cross_sell)

    # Build graph
    workflow.set_entry_point("classify_journey")
    workflow.add_edge("classify_journey", "retrieve_documents")
    workflow.add_edge("retrieve_documents", "suggest_cross_sell")
    workflow.add_edge("suggest_cross_sell", END)

    # Compile
    app = workflow.compile()

    #Optional: Save graph visualization
    # from pathlib import Path
    # graph_path = Path(__file__).parent.parent.parent / "workflow_graph.png"
    # save_workflow_graph_png(app, graph_path)
    # print(f"Workflow graph saved to {graph_path}")

    return app


# Example usage (for testing this module directly)
if __name__ == "__main__":
    app = build_conversation_workflow()
    print("Workflow compiled successfully.")

    sample_input: ConversationAnalysisState = {
        "conversation": "Customer: My card was declined when I tried to make a payment for my phone bill.",
        "journey": "",
        "sub_journey": "",
        "retrieved_documents": [],
        "cross_sell_opportunities": [],
    }

    print(f"\nRunning workflow with input: {sample_input['conversation']}")
    try:
        final_state = app.invoke(sample_input)
        print("\nWorkflow final state:")
        for key, value in final_state.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"An error occurred during workflow execution: {e}")
        print("Please ensure your OPENAI_API_KEY is set for the classification step.")