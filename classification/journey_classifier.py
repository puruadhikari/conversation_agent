from typing import Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

# Corrected import path
from schemas.schemas import JourneyClassificationOutput, ConversationAnalysisState

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Instantiate LLM client and output parser with descriptive names
llm_client = ChatOpenAI(model="gpt-4o", temperature=0)
output_parser = PydanticOutputParser(pydantic_object=JourneyClassificationOutput)

# Prompt template for classifying journey and sub-journey
JOURNEY_PROMPT = ChatPromptTemplate.from_template(
    """
You are an expert customer-journey classifier.
We have a predefined hierarchy of journeys and sub-journeys.
Return **ONLY** JSON matching this schema:
{format_instructions}

Conversation:
{conversation_snippet}
"""
).partial(format_instructions=output_parser.get_format_instructions())


def classify_journey_and_subjourney(state: ConversationAnalysisState) -> Dict[str, str]:
    """Node function for LangGraph – single LLM call for both labels."""

    conversation_snippet = state["conversation"]

    # Create the chain
    classification_chain = JOURNEY_PROMPT | llm_client | output_parser

    # Invoke the chain
    classification_result: JourneyClassificationOutput = classification_chain.invoke(
        {"conversation_snippet": conversation_snippet}
    )

    return {
        "journey": classification_result.journey,
        "sub_journey": classification_result.sub_journey,
    }


# Example usage (for testing this module directly)
if __name__ == "__main__":
    sample_state: ConversationAnalysisState = {
        "conversation": "Customer: I want to check my last bill.\nAgent: Sure, I can help with that.",
        "journey": "",
        "sub_journey": "",
        "retrieved_documents": [],
        "cross_sell_opportunities": [],
    }
    try:
        result = classify_journey_and_subjourney(sample_state)
        print("Classification Result:")
        print(f"  Journey: {result['journey']}")
        print(f"  Sub-journey: {result['sub_journey']}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your OPENAI_API_KEY is set in a .env file or environment variables.")