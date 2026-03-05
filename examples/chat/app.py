"""
Chat Example — AI Chat powered by Prompture + Cacao

A chat app where the user provides their API key,
picks a model, and chats with an LLM in real time with streaming.

Usage:
    cacao run examples/chat/app.py

Requires:
    pip install prompture
"""

from __future__ import annotations

import cacao as c
from cacao.server.session import Session

c.config(title="AI Chat", theme="dark")

# --- Versions ---
_cacao_version = c.__version__.split("+")[0].split(".dev")[0]
try:
    import prompture
    _pv = getattr(prompture, "__version__", "installed")
    _prompture_version = _pv.split("+")[0].split(".dev")[0]
except ImportError:
    _prompture_version = "not installed"

# --- State ---
api_key = c.signal("", name="api_key")
model_name = c.signal("openai/gpt-4o-mini", name="model_name")
system_prompt = c.signal("You are a helpful assistant.", name="system_prompt")
messages = c.signal([], name="messages")

# Bindings (sync input values back to signals)
c.bind("update_api_key", api_key)
c.bind("update_model", model_name)
c.bind("update_system_prompt", system_prompt)

# Per-session conversation instances
_conversations: dict[str, object] = {}


# --- Layout: sidebar (settings) + main (chat) ---
with c.layout("sidebar", sidebar_width="300px") as l:

    # Left sidebar — settings
    with l.side():
        with c.card(title="Provider"):
            c.input("API Key", signal=api_key, type="password",
                    placeholder="sk-...", on_change="update_api_key")
            c.select("Model", options=[
                "openai/gpt-4o-mini",
                "openai/gpt-4o",
                "claude/claude-sonnet-4-20250514",
                "groq/llama-3.1-8b-instant",
            ], signal=model_name, on_change="update_model")

        with c.card(title="System Prompt"):
            c.textarea(signal=system_prompt, placeholder="You are a helpful assistant.",
                       rows=5, on_change="update_system_prompt")

        with c.card(title="Powered by"):
            c.button(f"Cacao v{_cacao_version}", variant="ghost", size="sm",
                     on_click="link:https://github.com/cacao-research/Cacao")
            c.button(f"Prompture v{_prompture_version}", variant="ghost", size="sm",
                     on_click="link:https://github.com/jhd3197/prompture")

    # Right main — chat
    with l.main():
        c.chat(
            signal=messages,
            on_send="chat_send",
            on_clear="chat_clear",
            title="Chat",
            height="100%",
            show_clear=True,
            placeholder="Ask me anything...",
        )


# --- Event Handlers ---

@c.on("chat_send")
async def handle_send(session: Session, event: dict) -> None:
    """Handle user message: stream response from LLM via Prompture."""
    text = event.get("text", "").strip()
    if not text:
        return

    key = api_key.get(session)
    if not key:
        msgs = messages.get(session)
        messages.set(session, msgs + [{"role": "error", "content": "Please enter an API key first."}])
        return

    # Append user message immediately
    msgs = messages.get(session)
    messages.set(session, msgs + [{"role": "user", "content": text}])

    signal_name = "messages"

    try:
        from prompture import AsyncConversation
        from prompture.drivers.async_registry import get_async_driver_for_model

        # Get or create conversation for this session
        conv = _conversations.get(session.id)
        model = model_name.get(session)
        sys_prompt = system_prompt.get(session)

        if conv is None or conv._model_name != model:
            driver = get_async_driver_for_model(model, api_key=key)
            conv = AsyncConversation(
                driver=driver,
                model_name=model,
                system_prompt=sys_prompt,
            )
            _conversations[session.id] = conv
        elif conv._system_prompt != sys_prompt:
            conv._system_prompt = sys_prompt

        # Stream the response
        full_response = ""
        async for chunk in conv.ask_stream(text):
            full_response += chunk
            await session.send_chat_delta(signal_name, chunk)

        await session.send_chat_done(signal_name)

        # Append final assistant message to signal
        msgs = messages.get(session)
        messages.set(session, msgs + [{"role": "assistant", "content": full_response}])

    except ImportError:
        await session.send_chat_done(signal_name)
        msgs = messages.get(session)
        messages.set(session, msgs + [{
            "role": "error",
            "content": "Prompture is not installed. Run: pip install prompture",
        }])
    except Exception as e:
        await session.send_chat_done(signal_name)
        msgs = messages.get(session)
        messages.set(session, msgs + [{"role": "error", "content": str(e)}])


@c.on("chat_clear")
async def handle_clear(session: Session, event: dict) -> None:
    """Clear conversation history."""
    messages.set(session, [])
    _conversations.pop(session.id, None)
