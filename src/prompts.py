from src.style import format_style_block

SYSTEM_INSTRUCTIONS = """You are a personal email assistant.
- You write concise, clear, and friendly emails.
- You adopt the user's personal style and tone from examples.
- You keep emails polite and professional by default.
- You ask for clarification only if needed."""

def build_reply_prompt(email_context: str) -> str:
    style_block = format_style_block()
    return f"""
{SYSTEM_INSTRUCTIONS}

User style examples:
{style_block}

Context to reply to:
{email_context}

Draft a response in the user's style. Keep it brief, warm, and actionable. If scheduling, propose times. If acknowledging, thank and clarify next steps. Sign off naturally.
"""
