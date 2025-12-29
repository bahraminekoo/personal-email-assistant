import typer
from rich.console import Console
from rich.panel import Panel
from src.agent import draft_reply

app = typer.Typer(add_completion=False)
console = Console()

@app.command()
def reply(email: str):
    """
    Draft a reply in your personal style.
    Example:
        python -m src.cli reply "Hi Hossein, can we meet tomorrow at 3pm?"
    """
    console.print(Panel.fit("Drafting reply...", style="bold green"))
    response = draft_reply(email)
    console.print(Panel(response, title="Your Draft", subtitle="Personal Email Assistant"))

if __name__ == "__main__":
    app()
