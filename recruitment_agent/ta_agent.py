from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# ---------- 1. Set-up ----------
load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)


class State(TypedDict):
    application: str
    experience_level: str
    skill_match: str
    response: str


workflow = StateGraph(State)

# ---------- 2. Pydantic schema for experience ----------
class ExperienceLevelOutput(BaseModel):
    """Structured response expected from the LLM."""
    experience_level: str = Field(
        description="One of 'Entry-level', 'Mid-level', or 'Senior-level'."
    )

exp_parser = PydanticOutputParser(pydantic_object=ExperienceLevelOutput)

# ---------- 3. Nodes ----------
def categorize_experience(state: State) -> State:
    """Ask the LLM to classify experience and parse the JSON into a Pydantic object."""
    prompt = ChatPromptTemplate.from_template(
        "You are classifying a candidate's seniority.\n\n"
        "Return **ONLY** JSON that matches this schema:\n"
        "{format_instructions}\n\n"
        "Application: {application}"
    ).partial(format_instructions=exp_parser.get_format_instructions())

    # Combine prompt → model → parser
    chain = prompt | llm | exp_parser

    result: ExperienceLevelOutput = chain.invoke(
        {"application": state["application"]}
    )
    experience_level = result.experience_level
    print(f"Experience level → {experience_level}")
    return {"experience_level": experience_level}


def assess_skillset(state: State) -> State:
    print("\nAssessing skill-set …")
    prompt = ChatPromptTemplate.from_template(
        "Based on the job application for a Python Developer, assess the candidate's skill-set.\n"
        "Respond with either 'Match' or 'No Match'.\n"
        "Application: {application}"
    )
    skill_match = (prompt | llm).invoke({"application": state["application"]}).content
    print(f"Skill match → {skill_match}")
    return {"skill_match": skill_match}


def schedule_hr_interview(_: State) -> State:
    print("\nScheduling HR interview …")
    return {"response": "Candidate has been shortlisted for an HR interview."}


def escalate_to_recruiter(_: State) -> State:
    print("\nEscalating to recruiter …")
    return {"response": "Candidate has senior-level experience but doesn't match job skills."}


def reject_application(_: State) -> State:
    print("\nSending rejection email …")
    return {"response": "Candidate doesn't meet the JD and has been rejected."}


# ---------- 4. Router ----------
def route_app(state: State) -> str:
    if state["skill_match"] == "Match":
        return "schedule_hr_interview"
    elif "Senior-level" in state["experience_level"]:
        return "escalate_to_recruiter"
    else:
        return "reject_application"


# ---------- 5. Build graph ----------
workflow.add_node("categorize_experience", categorize_experience)
workflow.add_node("assess_skillset", assess_skillset)
workflow.add_node("schedule_hr_interview", schedule_hr_interview)
workflow.add_node("escalate_to_recruiter", escalate_to_recruiter)
workflow.add_node("reject_application", reject_application)

workflow.add_edge("categorize_experience", "assess_skillset")
workflow.add_conditional_edges("assess_skillset", route_app)
workflow.add_edge(START, "categorize_experience")
workflow.add_edge("assess_skillset", END)
workflow.add_edge("schedule_hr_interview", END)
workflow.add_edge("escalate_to_recruiter", END)
workflow.add_edge("reject_application", END)

app = workflow.compile()

# ---------- 6. Test run & save graph ----------
if __name__ == "__main__":
    test_state: State = {
        "application": "I have 10 years of Java and AWS experience, built scalable APIs …",
        "experience_level": "",
        "skill_match": "",
        "response": ""
    }
    final_state = app.invoke(test_state)
    print("\nFinal state:", final_state)

    png_bytes: bytes = app.get_graph().draw_mermaid_png()
    out_path = Path(__file__).with_name("workflow_graph.png")
    out_path.write_bytes(png_bytes)
    print(f"\nGraph saved → {out_path.resolve()}")
