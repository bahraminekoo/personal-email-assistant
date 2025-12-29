# Your personal style examples (start simple; refine over time)
MY_STYLE_EXAMPLES = [
    "Hi there, thanks for reaching out — happy to help.",
    "Hey, appreciate the update. Quick note on timing: let's aim for tomorrow afternoon.",
    "Hello, thanks for the details. I’ve reviewed them and here’s my suggestion..."
]

def format_style_block() -> str:
    return "\n".join(f"- {ex}" for ex in MY_STYLE_EXAMPLES)
