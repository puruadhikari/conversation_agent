from pathlib import Path
from typing import Any


def save_workflow_graph_png(workflow: Any, output_path: Path) -> None:
    """
    Generate and save the workflow graph as a PNG file.

    :param workflow: Compiled LangGraph application (return of compile()).
    :param output_path: Path where the PNG should be saved.
    """
    # Draw graph as Mermaid PNG bytes
    png_bytes: bytes = workflow.get_graph().draw_mermaid_png()

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write bytes to file
    with output_path.open("wb") as f:
        f.write(png_bytes)