import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from src.agent import draft_reply
from src.integrations.gmail import list_unread_emails, get_message_details, send_reply

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

@app.command()
def gmail_inbox():
    """List unread Gmail messages"""
    emails = list_unread_emails()
    if not emails:
        console.print(Panel.fit("No unread emails found.", style="bold yellow"))
        return
    for e in emails:
        console.print(Panel(e["snippet"], title=f"Email ID: {e['id']}"))

@app.command()
def gmail_reply(
    to: str = typer.Option(..., "--to", "-t", help="Recipient email"),
    subject: str = typer.Option(..., "--subject", "-s", help="Email subject"),
    file: Path = typer.Argument(..., help="File containing reply text")
):
    """Send a reply via Gmail"""
    body = file.read_text()
    send_reply(to, subject, body)
    console.print(Panel.fit("Reply sent!", style="bold green"))

@app.command()
def gmail_auto_reply(limit: int = typer.Option(2, help="Number of unread emails to reply to")):
    """Automatically draft and send replies to unread Gmail messages"""
    console.print(Panel.fit("Fetching unread emails...", style="bold green"))
    emails = list_unread_emails()[:limit]

    if not emails:
        console.print(Panel.fit("No unread emails found.", style="bold yellow"))
        return

    for e in emails:
        details = get_message_details(e["id"])
        console.print(Panel.fit(f"Drafting reply to: {details['sender']}", style="bold cyan"))
        reply_text = draft_reply(details["snippet"])
        send_reply(details["sender"], f"Re: {details['subject']}", reply_text)
        console.print(Panel(reply_text, title=f"Reply sent to {details['sender']}", subtitle=details["subject"]))



if __name__ == "__main__":
    app()