import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from src.agent import draft_reply

app = typer.Typer(add_completion=False)
console = Console()

@app.command()
def reply(
    email: str = typer.Option(
        ..., 
        "--email", "-e", 
        help="The email text to reply to"
    )
):
    """Draft a reply to an email"""
    console.print(Panel.fit("Drafting reply...", style="bold green"))
    response = draft_reply(email)
    console.print(Panel(response, title="Your Draft", subtitle="Personal Email Assistant"))

@app.command()
def reply_file(
    file: Path = typer.Argument(
        ...,
        help="Path to a file containing the email text"
    )
):
    """Draft a reply from an email file"""
    email_text = file.read_text()
    console.print(Panel.fit("Drafting reply...", style="bold green"))
    response = draft_reply(email_text)
    console.print(Panel(response, title="Your Draft", subtitle="Personal Email Assistant"))

if __name__ == "__main__":
    app()