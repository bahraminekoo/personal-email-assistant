from src.agent import draft_reply

def test_draft_reply_basic():
    email = "Hi Hossein, can we meet tomorrow at 3pm?"
    reply = draft_reply(email)
    assert isinstance(reply, str)
    assert len(reply) > 0
