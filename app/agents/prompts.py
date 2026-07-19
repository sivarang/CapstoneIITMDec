from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_DIR = BASE_DIR / "prompts"


def load_prompt(filename: str) -> str:
    """
    Load a prompt file from app/prompts.
    """

    prompt_file = PROMPT_DIR / filename

    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_file}"
        )

    return prompt_file.read_text(encoding="utf-8")