from typing import List, Dict


def extract_recent_exchanges(dialogue: List[Dict[str, str]], max_pairs: int = 5) -> str:
    """Concatenate the last *max_pairs* customer/agent exchanges.

    The *dialogue* parameter is expected to be a list of dicts with keys
    ``speaker`` (either "customer" or "agent") and ``text``.
    """

    # Keep the last *max_pairs* * 2 utterances (pair = customer + agent)
    recent_turns = dialogue[-max_pairs * 2 :]

    # Simple formatting: "Speaker: text" per line
    return "\n".join(f"{turn['speaker'].title()}: {turn['text']}" for turn in recent_turns)