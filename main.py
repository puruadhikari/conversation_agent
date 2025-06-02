import json
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from workflows.conversation_workflow import build_conversation_workflow
from utils.conversation_utils import extract_recent_exchanges
from schemas.schemas import ConversationAnalysisState

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def main():
    """
    Main function to run the conversation analysis agent.
    """
    print("Building conversation analysis workflow...")
    app = build_conversation_workflow()
    print("Workflow built successfully.")

    conversation_data = {
          "dialogue": [
            {"speaker": "customer", "text": "Hi, I want to ask about my bill."},
            {"speaker": "agent", "text": "Sure, I can help you with that. What is your question?"},
            {"speaker": "customer", "text": "I am not receiving my bills to my address and I think you may have your old address."},
            {"speaker": "agent", "text": "Okay, let me check that for you."}
          ]
        }
    # Extract recent exchanges
    recent_dialogue_str = extract_recent_exchanges(conversation_data["dialogue"], max_pairs=3)
    print(f"\nExtracted recent dialogue:\n{recent_dialogue_str}\n")

    # Prepare initial state for the workflow
    initial_state: ConversationAnalysisState = {
        "conversation": recent_dialogue_str,
        "journey": "",
        "sub_journey": "",
        "retrieved_documents": [],
        "cross_sell_opportunities": [],
    }

    print("Invoking workflow...")
    try:
        final_state = app.invoke(initial_state)
        print("\n--- Conversation Analysis Complete ---")
        print(f"Initial Conversation Snippet: {initial_state['conversation']}")
        print(f"  Classified Journey: {final_state.get('journey', 'N/A')}")
        print(f"  Classified Sub-journey: {final_state.get('sub_journey', 'N/A')}")
        print(f"  Retrieved Documents: {final_state.get('retrieved_documents', [])}")
        print(f"  Cross-Sell Opportunities: {final_state.get('cross_sell_opportunities', [])}")
        print("------------------------------------")
    except Exception as e:
        print(f"An error occurred while running the workflow: {e}")
        print("If this is related to OpenAI, ensure your API key is correctly configured.")


if __name__ == "__main__":
    main()
