from __future__ import annotations
from typing import Dict, List

# Corrected import path
from schemas.schemas import CrossSellOutput, ConversationAnalysisState


def suggest_cross_sell(state: ConversationAnalysisState) -> Dict[str, List[str]]:
    """
    Node function for LangGraph – suggests cross-sell items.
    This is a placeholder implementation.
    """
    journey = state["journey"]
    sub_journey = state["sub_journey"]

    print(f"Suggesting cross-sell for journey: '{journey}' and sub-journey: '{sub_journey}'")

    # Placeholder logic:
    suggested = []
    if journey == "Payment" and "credit card" in state["conversation"].lower():
        suggested.append("premium_credit_card_rewards")
    if sub_journey == "New Account":
        suggested.append("overdraft_protection_service")

    output = CrossSellOutput(suggested_items=suggested)

    return {"cross_sell_opportunities": output.suggested_items}


# Example usage (for testing this module directly)
if __name__ == "__main__":
    sample_state: ConversationAnalysisState = {
        "conversation": "Customer: I'd like to open a new checking account. I also use my credit card a lot.",
        "journey": "Account Management",  # This might be classified by a previous step
        "sub_journey": "New Account",  # This might be classified by a previous step
        "retrieved_documents": [],
        "cross_sell_opportunities": [],
    }
    result = suggest_cross_sell(sample_state)
    print("Cross-Sell Suggestions:")
    print(result["cross_sell_opportunities"])