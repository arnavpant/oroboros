"""
Antidote system instruction injected when a semantic loop is detected.
This is the single source of truth for loop termination behavior.
"""

ANTIDOTE_INSTRUCTION = """
You are in a detected reasoning loop.

Rules you must follow immediately:
1. Stop all iterative reasoning.
2. Do NOT re-plan, re-check, or self-verify.
3. Produce a single, final response only.
4. If you are uncertain or cannot safely conclude, output exactly:

TERMINATE_LOOP

Do not continue the conversation after this response.
"""

from .config import ANTIDOTE_INSTRUCTION
