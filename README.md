# 📧 Personal Email Assistant

An AI‑powered assistant that reads emails, decides whether they need a reply, drafts polite responses, and integrates directly with Gmail for automated sending. Built with **LangGraph**, **LangChain**, and **Hugging Face models**, this project is designed to be beginner‑friendly, maintainable, and easy to extend.

---

## ✨ Features

- **Email Understanding**
  - Reads incoming email text or files.
  - Decides automatically if a reply is needed (e.g., skips newsletters).

- **AI‑Generated Replies**
  - Drafts polite, context‑aware responses using Hugging Face models.
  - Customizable signature (name, email, company) via `.env`.

- **CLI Interface**
  - `reply` → Draft a reply from inline text.
  - `reply-file` → Draft a reply from a file.
  - `gmail-inbox` → List unread Gmail messages.
  - `gmail-reply` → Send a reply via Gmail.
  - `gmail-auto-reply` → Fetch unread Gmail, draft replies, and send automatically.

- **Gmail Integration**
  - OAuth2 authentication with Gmail API.
  - Fetch unread emails, extract sender + subject.
  - Send replies directly from the assistant.
  - ✅ **Mark messages as read after replying** (prevents duplicate replies).
  - ✅ **Configurable filters**:
     - Skip newsletters, no‑reply addresses, or promotional emails.
     - Restrict replies to specific senders via `.env`.

---

## 🛠️ Technical Details

- **Core Frameworks**
  - [LangGraph](https://github.com/langchain-ai/langgraph) for agent workflow orchestration.
  - [LangChain](https://www.langchain.com/) for LLM integration.
  - [Hugging Face Transformers](https://huggingface.co/docs/transformers) for local model pipelines.

- **Model Flexibility**
  - Model ID is configurable via `.env` (`DEFAULT_MODEL`).
  - Supports causal models (`text-generation`) like `TinyLlama/TinyLlama-1.1B-Chat-v1.0`.
  - Supports seq2seq models (`text2text-generation`) like `google/flan-t5-large`.

- **CLI**
  - Built with [Typer](https://typer.tiangolo.com/) for a clean command‑line interface.
  - Rich output formatting with [Rich](https://github.com/Textualize/rich).

- **Gmail API**
  - Uses `google-api-python-client`, `google-auth-oauthlib`.
  - Stores OAuth tokens in `token.json` for reuse.
  - Scopes: `https://www.googleapis.com/auth/gmail.modify`.

---

## ⚙️ Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/bahraminekoo/personal-email-assistant.git
   cd personal-email-assistant

2. **Install dependencies**
   pip install -r requirements.txt

3. **Configure environment**
   ```
   Create a .env file:
   DEFAULT_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0
   SIGNATURE_NAME=Hossein
   SIGNATURE_EMAIL=hossein@example.com
   SIGNATURE_COMPANY=Personal Email Assistant
   # Comma-separated list of allowed senders
   ALLOWED_SENDERS=boss@example.com,friend@example.com

   # Comma-separated list of keywords to skip
   SKIP_KEYWORDS=newsletter,no-reply,promotion
   ```
    
4. **Set up Gmail API**
   - Enable Gmail API in Google Cloud Console
   - Download credentials.json into project root.
   - First run will prompt OAuth login and create token.json.

🚀 Usage

Draft a reply from inline text:

   python -m src.cli reply --email "Hi Hossein, can we meet tomorrow at 3pm?"

Draft a reply from a file:

   python -m src.cli reply-file email.txt

List unread Gmail messages:
   
   python -m src.cli gmail-inbox

Send a reply via Gmail:

   python -m src.cli gmail-reply -t someone@example.com -s "Re: Meeting" reply.txt

Auto‑reply to unread Gmail:

   python -m src.cli gmail-auto-reply --limit 2

📐 Project Structure
```
src/
   agent.py              # LangGraph agent logic
   cli.py                # Typer CLI commands
   config.py             # Environment variable loader
   integrations/
      gmail.py          # Gmail API helpers
```      

🔮 Roadmap

   - [x] Mark Gmail messages as read after replying

   - [x] Configurable filters via .env (skip keywords, allowed senders)

   - [ ] Support multiple signatures / personas.

   - [ ] Add logging and monitoring.

   - [ ] Store skipped emails for later review

🤝 Contributing

Pull requests are welcome! Please ensure code is clean, documented, and beginner‑friendly.   

📜 License

MIT License.