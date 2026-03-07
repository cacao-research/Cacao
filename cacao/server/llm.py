"""
LLM integration for Cacao — streaming chat with Prompture-powered providers.

Uses Prompture's driver system for 15+ LLM providers (OpenAI, Anthropic,
Google, Groq, Grok, Ollama, LM Studio, Azure, OpenRouter, and more).
Provides session-scoped conversation memory, system prompt configuration,
tool/function calling support, cost tracking, and budget enforcement.

Example:
    import cacao as c

    chat = c.chat(
        provider="openai",
        model="gpt-4o",
        system_prompt="You are a helpful assistant.",
    )
"""

from __future__ import annotations

import asyncio
import json
import uuid
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .log import get_logger
from .signal import Signal

if TYPE_CHECKING:
    from .session import Session

logger = get_logger("cacao.llm")


# =============================================================================
# Message Types
# =============================================================================


@dataclass
class Message:
    """A chat message."""

    role: str  # "user", "assistant", "system", "tool"
    content: str
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
    name: str | None = None  # tool name for tool messages

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for signal serialization."""
        d: dict[str, Any] = {"role": self.role, "content": self.content}
        if self.tool_calls:
            d["tool_calls"] = [tc.to_dict() for tc in self.tool_calls]
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.name:
            d["name"] = self.name
        return d


@dataclass
class ToolCall:
    """A tool/function call from the LLM."""

    id: str
    name: str
    arguments: str  # JSON string

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "arguments": self.arguments}

    @property
    def parsed_arguments(self) -> dict[str, Any]:
        """Parse the JSON arguments string."""
        try:
            result: dict[str, Any] = json.loads(self.arguments)
            return result
        except (json.JSONDecodeError, TypeError):
            return {}


@dataclass
class StreamChunk:
    """A chunk from a streaming LLM response."""

    delta: str = ""
    tool_calls: list[ToolCall] | None = None
    finish_reason: str | None = None


@dataclass
class ToolSpec:
    """Specification for a tool the LLM can call."""

    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema

    def to_openai(self) -> dict[str, Any]:
        """Convert to OpenAI tool format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def to_anthropic(self) -> dict[str, Any]:
        """Convert to Anthropic tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters,
        }

    def to_prompture(self) -> dict[str, Any]:
        """Convert to Prompture tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


# =============================================================================
# Cost Tracking
# =============================================================================


@dataclass
class UsageRecord:
    """Token usage and cost for a single LLM call."""

    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0


class SessionCostTracker:
    """Track LLM usage costs per session."""

    def __init__(self) -> None:
        self._records: list[UsageRecord] = []
        self._total_cost: float = 0.0
        self._total_tokens: int = 0
        self._budget_max_cost: float | None = None
        self._budget_max_tokens: int | None = None
        self._fallback_model: str | None = None

    def record(self, usage: UsageRecord) -> None:
        """Record a usage event."""
        self._records.append(usage)
        self._total_cost += usage.cost
        self._total_tokens += usage.total_tokens

    @property
    def total_cost(self) -> float:
        return self._total_cost

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    @property
    def records(self) -> list[UsageRecord]:
        return list(self._records)

    def set_budget(
        self,
        max_cost: float | None = None,
        max_tokens: int | None = None,
        fallback_model: str | None = None,
    ) -> None:
        """Set budget limits for this session."""
        self._budget_max_cost = max_cost
        self._budget_max_tokens = max_tokens
        self._fallback_model = fallback_model

    def is_over_budget(self) -> bool:
        """Check if the session has exceeded its budget."""
        if self._budget_max_cost is not None and self._total_cost >= self._budget_max_cost:
            return True
        if self._budget_max_tokens is not None and self._total_tokens >= self._budget_max_tokens:
            return True
        return False

    def should_degrade(self) -> bool:
        """Check if we should degrade to a cheaper model (80% of budget)."""
        if self._fallback_model is None:
            return False
        if self._budget_max_cost is not None and self._total_cost >= self._budget_max_cost * 0.8:
            return True
        if self._budget_max_tokens is not None and self._total_tokens >= int(
            self._budget_max_tokens * 0.8
        ):
            return True
        return False

    @property
    def fallback_model(self) -> str | None:
        return self._fallback_model

    def summary(self) -> dict[str, Any]:
        """Return a cost summary dict for the UI."""
        by_model: dict[str, dict[str, Any]] = {}
        for rec in self._records:
            key = f"{rec.provider}/{rec.model}"
            entry = by_model.setdefault(
                key,
                {
                    "provider": rec.provider,
                    "model": rec.model,
                    "calls": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "cost": 0.0,
                },
            )
            entry["calls"] += 1
            entry["prompt_tokens"] += rec.prompt_tokens
            entry["completion_tokens"] += rec.completion_tokens
            entry["total_tokens"] += rec.total_tokens
            entry["cost"] += rec.cost

        return {
            "total_cost": round(self._total_cost, 6),
            "total_tokens": self._total_tokens,
            "call_count": len(self._records),
            "by_model": list(by_model.values()),
            "budget": {
                "max_cost": self._budget_max_cost,
                "max_tokens": self._budget_max_tokens,
                "over_budget": self.is_over_budget(),
                "degraded": self.should_degrade(),
            },
        }


# Global per-session cost trackers
_session_trackers: dict[str, SessionCostTracker] = {}


def get_cost_tracker(session_id: str) -> SessionCostTracker:
    """Get or create a cost tracker for a session."""
    if session_id not in _session_trackers:
        _session_trackers[session_id] = SessionCostTracker()
    return _session_trackers[session_id]


# =============================================================================
# Provider Adapters — Prompture-backed
# =============================================================================


class LLMProvider(ABC):
    """Base class for LLM provider adapters."""

    @abstractmethod
    def stream(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str,
        system_prompt: str | None = None,
        tools: list[ToolSpec] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> AsyncIterator[StreamChunk]:
        """Stream a chat completion response."""
        ...

    @abstractmethod
    async def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str,
        system_prompt: str | None = None,
        tools: list[ToolSpec] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> Message:
        """Get a complete (non-streaming) chat response."""
        ...


class PromptureProvider(LLMProvider):
    """Unified LLM provider backed by Prompture's driver system.

    Supports 15+ providers via Prompture: OpenAI, Anthropic, Google, Groq,
    Grok, Ollama, LM Studio, Azure, OpenRouter, Moonshot, Z.ai, ModelScope,
    HuggingFace, AirLLM, CachiBot, and any custom-registered driver.
    """

    def __init__(
        self,
        *,
        provider: str = "openai",
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url
        self._async_driver: Any | None = None

    def _get_async_driver(self, model: str) -> Any:
        """Get or create the async Prompture driver."""
        try:
            from prompture.drivers import get_async_driver_for_model
        except ImportError:
            raise ImportError(
                "prompture package is required for LLM providers. "
                "Install it with: pip install prompture"
            )

        model_str = f"{self.provider}/{model}"
        kwargs: dict[str, Any] = {}
        if self.api_key:
            kwargs["api_key"] = self.api_key
        if self.base_url:
            kwargs["base_url"] = self.base_url

        return get_async_driver_for_model(model_str, **kwargs)

    def _build_messages(
        self, messages: list[dict[str, Any]], system_prompt: str | None
    ) -> list[dict[str, Any]]:
        """Build Prompture-format message list."""
        result: list[dict[str, Any]] = []
        if system_prompt:
            result.append({"role": "system", "content": system_prompt})
        for msg in messages:
            role = msg["role"]
            if role == "error":
                continue  # skip error messages
            entry: dict[str, Any] = {"role": role, "content": msg.get("content", "")}
            if msg.get("tool_calls"):
                entry["tool_calls"] = msg["tool_calls"]
            if msg.get("tool_call_id"):
                entry["tool_call_id"] = msg["tool_call_id"]
            if msg.get("name"):
                entry["name"] = msg["name"]
            result.append(entry)
        return result

    async def stream(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str,
        system_prompt: str | None = None,
        tools: list[ToolSpec] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> AsyncIterator[StreamChunk]:
        driver = self._get_async_driver(model)
        api_messages = self._build_messages(messages, system_prompt)

        options: dict[str, Any] = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }

        if tools and hasattr(driver, "generate_messages_with_tools") and driver.supports_tool_use:
            # Use non-streaming tool call path, then yield as single chunk
            prompture_tools = [t.to_prompture() for t in tools]
            response = await driver.generate_messages_with_tools(
                api_messages, prompture_tools, options
            )
            text = response.get("text", "")
            meta = response.get("meta", {})

            tool_calls = None
            if response.get("tool_calls"):
                tool_calls = [
                    ToolCall(
                        id=tc.get("id", str(uuid.uuid4())),
                        name=tc["name"],
                        arguments=json.dumps(tc["arguments"])
                        if isinstance(tc["arguments"], dict)
                        else tc["arguments"],
                    )
                    for tc in response["tool_calls"]
                ]

            yield StreamChunk(delta=text, tool_calls=tool_calls, finish_reason="stop")
            # Store meta for cost tracking
            self._last_meta = meta
            return

        # Streaming path
        if hasattr(driver, "generate_messages_stream") and driver.supports_streaming:
            async for chunk in driver.generate_messages_stream(api_messages, options):
                chunk_type = chunk.get("type", "")
                if chunk_type == "delta":
                    yield StreamChunk(delta=chunk.get("text", ""))
                elif chunk_type == "done":
                    self._last_meta = chunk.get("meta", {})
                    yield StreamChunk(
                        delta="",
                        finish_reason="stop",
                    )
        else:
            # Fallback: non-streaming complete call
            response = await driver.generate_messages(api_messages, options)
            text = response.get("text", "")
            self._last_meta = response.get("meta", {})
            yield StreamChunk(delta=text, finish_reason="stop")

    async def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str,
        system_prompt: str | None = None,
        tools: list[ToolSpec] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> Message:
        driver = self._get_async_driver(model)
        api_messages = self._build_messages(messages, system_prompt)

        options: dict[str, Any] = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }

        if tools and hasattr(driver, "generate_messages_with_tools") and driver.supports_tool_use:
            prompture_tools = [t.to_prompture() for t in tools]
            response = await driver.generate_messages_with_tools(
                api_messages, prompture_tools, options
            )
        else:
            response = await driver.generate_messages(api_messages, options)

        text = response.get("text", "")
        meta = response.get("meta", {})
        self._last_meta = meta

        tool_calls = None
        if response.get("tool_calls"):
            tool_calls = [
                ToolCall(
                    id=tc.get("id", str(uuid.uuid4())),
                    name=tc["name"],
                    arguments=json.dumps(tc["arguments"])
                    if isinstance(tc["arguments"], dict)
                    else tc["arguments"],
                )
                for tc in response["tool_calls"]
            ]

        return Message(
            role="assistant",
            content=text,
            tool_calls=tool_calls,
        )


# Legacy provider classes — thin wrappers around PromptureProvider for backward compat
class OpenAIProvider(PromptureProvider):
    """OpenAI provider (backed by Prompture)."""

    def __init__(self, *, api_key: str | None = None, base_url: str | None = None) -> None:
        super().__init__(provider="openai", api_key=api_key, base_url=base_url)


class AnthropicProvider(PromptureProvider):
    """Anthropic Claude provider (backed by Prompture)."""

    def __init__(self, *, api_key: str | None = None) -> None:
        super().__init__(provider="claude", api_key=api_key)


class OllamaProvider(PromptureProvider):
    """Ollama local model provider (backed by Prompture)."""

    def __init__(self, *, base_url: str = "http://localhost:11434") -> None:
        super().__init__(provider="ollama", base_url=base_url)


# Provider name aliases — maps user-facing names to Prompture provider names
_PROVIDER_ALIASES: dict[str, str] = {
    "openai": "openai",
    "gpt": "openai",
    "chatgpt": "openai",
    "anthropic": "claude",
    "claude": "claude",
    "ollama": "ollama",
    "local": "ollama",
    "google": "google",
    "gemini": "google",
    "groq": "groq",
    "grok": "grok",
    "xai": "grok",
    "azure": "azure",
    "openrouter": "openrouter",
    "lmstudio": "lmstudio",
    "lm_studio": "lmstudio",
    "moonshot": "moonshot",
    "zai": "zai",
    "zhipu": "zai",
    "modelscope": "modelscope",
    "huggingface": "huggingface",
    "hf": "huggingface",
    "airllm": "airllm",
    "cachibot": "cachibot",
    "local_http": "local_http",
}


def get_provider(
    provider: str | LLMProvider,
    *,
    api_key: str | None = None,
    base_url: str | None = None,
) -> LLMProvider:
    """Get a provider instance by name or pass through an existing one.

    Supports all Prompture providers: openai, anthropic/claude, google/gemini,
    groq, grok/xai, ollama, lmstudio, azure, openrouter, moonshot, zai/zhipu,
    modelscope, huggingface, airllm, cachibot, local_http.
    """
    if isinstance(provider, LLMProvider):
        return provider

    name = provider.lower().strip()
    prompture_name = _PROVIDER_ALIASES.get(name, name)

    return PromptureProvider(
        provider=prompture_name,
        api_key=api_key,
        base_url=base_url,
    )


# =============================================================================
# Chat Engine — ties provider + memory + tools + streaming + cost tracking
# =============================================================================


@dataclass
class ChatConfig:
    """Configuration for a chat instance."""

    provider: str | LLMProvider = "openai"
    model: str = "gpt-4o"
    system_prompt: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: list[ToolSpec] | None = None
    tool_handlers: dict[str, Callable[..., Any]] = field(default_factory=dict)
    max_history: int = 100  # max messages to keep in memory
    # Budget enforcement
    max_cost: float | None = None  # max USD cost per session
    max_budget_tokens: int | None = None  # max total tokens per session
    fallback_model: str | None = None  # cheaper model to degrade to


# Registry of chat configs keyed by signal name
_chat_configs: dict[str, ChatConfig] = {}

# Tool handler registry: signal_name -> {tool_name: handler_fn}
_tool_handlers: dict[str, dict[str, Callable[..., Any]]] = {}


def register_chat(
    signal_name: str,
    config: ChatConfig,
) -> None:
    """Register a chat configuration for a signal."""
    _chat_configs[signal_name] = config
    if config.tool_handlers:
        _tool_handlers[signal_name] = config.tool_handlers


async def handle_chat_message(
    session: Session,
    signal: Signal[list[Any]],
    text: str,
) -> None:
    """
    Handle a user message: add to history, stream LLM response, update signal.

    This is the main entry point called by the chat event handler.
    """
    signal_name = signal.name
    config = _chat_configs.get(signal_name)
    if not config:
        logger.warning("No chat config for signal '%s'", signal_name)
        return

    # Budget check
    tracker = get_cost_tracker(session.id)
    if config.max_cost is not None or config.max_budget_tokens is not None:
        tracker.set_budget(
            max_cost=config.max_cost,
            max_tokens=config.max_budget_tokens,
            fallback_model=config.fallback_model,
        )

    if tracker.is_over_budget():
        # Send budget exceeded error
        history: list[dict[str, Any]] = list(signal.get(session))
        history.append({"role": "user", "content": text})
        history.append(
            {
                "role": "error",
                "content": f"Budget exceeded (${tracker.total_cost:.4f} spent"
                + (f", limit ${config.max_cost:.4f}" if config.max_cost else "")
                + f"). {tracker.total_tokens} tokens used"
                + (f", limit {config.max_budget_tokens}" if config.max_budget_tokens else "")
                + ".",
            }
        )
        signal.set(session, history)
        await session.send_chat_done(signal_name)
        return

    # Determine model (auto-degrade if near budget)
    model = config.model
    if tracker.should_degrade() and tracker.fallback_model:
        model = tracker.fallback_model
        logger.info(
            "Budget threshold reached for session '%s', degrading to '%s'",
            session.id,
            model,
        )

    # Get current history
    history = list(signal.get(session))

    # Add user message
    user_msg = {"role": "user", "content": text}
    history.append(user_msg)
    signal.set(session, history)

    # Get provider
    provider = get_provider(config.provider, api_key=config.api_key, base_url=config.base_url)

    try:
        # Stream the response
        full_response = ""
        tool_calls: list[ToolCall] = []

        async for chunk in provider.stream(
            history,
            model=model,
            system_prompt=config.system_prompt,
            tools=config.tools,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        ):
            if chunk.delta:
                full_response += chunk.delta
                await session.send_chat_delta(signal_name, chunk.delta)
            if chunk.tool_calls:
                tool_calls.extend(chunk.tool_calls)

        # Signal streaming is done
        await session.send_chat_done(signal_name)

        # Record cost from provider meta
        _record_cost(session.id, config, model, provider)

        # Handle tool calls if any
        if tool_calls:
            # Add assistant message with tool calls
            assistant_msg: dict[str, Any] = {
                "role": "assistant",
                "content": full_response,
                "tool_calls": [tc.to_dict() for tc in tool_calls],
            }
            history.append(assistant_msg)
            signal.set(session, history)

            # Execute tool handlers and collect results
            handlers = _tool_handlers.get(signal_name, config.tool_handlers)
            for tc in tool_calls:
                handler = handlers.get(tc.name)
                if handler:
                    try:
                        args = tc.parsed_arguments
                        result = handler(**args)
                        if asyncio.iscoroutine(result):
                            result = await result
                        tool_result = str(result)
                    except Exception as e:
                        tool_result = f"Error: {e}"
                else:
                    tool_result = f"No handler for tool '{tc.name}'"

                # Add tool result to history
                tool_msg: dict[str, Any] = {
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tc.id,
                    "name": tc.name,
                }
                history.append(tool_msg)

            signal.set(session, history)

            # Continue the conversation with tool results — recurse
            await _continue_after_tools(session, signal, config, provider, history, model)
        else:
            # Regular text response — add to history
            assistant_msg = {"role": "assistant", "content": full_response}
            history.append(assistant_msg)

            # Trim history if needed
            if config.max_history and len(history) > config.max_history:
                history = history[-config.max_history :]

            signal.set(session, history)

    except Exception as e:
        logger.exception("Chat error for signal '%s'", signal_name)
        await session.send_chat_done(signal_name)

        # Add error to history
        error_msg = {"role": "error", "content": str(e)}
        history.append(error_msg)
        signal.set(session, history)


def _record_cost(
    session_id: str,
    config: ChatConfig,
    model: str,
    provider: LLMProvider,
) -> None:
    """Record cost from the last provider call."""
    meta = getattr(provider, "_last_meta", None)
    if not meta:
        return

    provider_name = (
        config.provider if isinstance(config.provider, str) else type(config.provider).__name__
    )
    tracker = get_cost_tracker(session_id)
    tracker.record(
        UsageRecord(
            provider=provider_name,
            model=model,
            prompt_tokens=meta.get("prompt_tokens", 0),
            completion_tokens=meta.get("completion_tokens", 0),
            total_tokens=meta.get("total_tokens", 0),
            cost=meta.get("cost", 0.0),
        )
    )


async def _continue_after_tools(
    session: Session,
    signal: Signal[list[Any]],
    config: ChatConfig,
    provider: LLMProvider,
    history: list[dict[str, Any]],
    model: str | None = None,
) -> None:
    """Continue streaming after tool call results are added."""
    signal_name = signal.name
    model = model or config.model

    try:
        full_response = ""
        tool_calls: list[ToolCall] = []

        async for chunk in provider.stream(
            history,
            model=model,
            system_prompt=config.system_prompt,
            tools=config.tools,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        ):
            if chunk.delta:
                full_response += chunk.delta
                await session.send_chat_delta(signal_name, chunk.delta)
            if chunk.tool_calls:
                tool_calls.extend(chunk.tool_calls)

        await session.send_chat_done(signal_name)

        # Record cost
        _record_cost(session.id, config, model, provider)

        if tool_calls:
            assistant_msg: dict[str, Any] = {
                "role": "assistant",
                "content": full_response,
                "tool_calls": [tc.to_dict() for tc in tool_calls],
            }
            history.append(assistant_msg)
            signal.set(session, history)

            handlers = _tool_handlers.get(signal_name, config.tool_handlers)
            for tc in tool_calls:
                handler = handlers.get(tc.name)
                if handler:
                    try:
                        args = tc.parsed_arguments
                        result = handler(**args)
                        if asyncio.iscoroutine(result):
                            result = await result
                        tool_result = str(result)
                    except Exception as e:
                        tool_result = f"Error: {e}"
                else:
                    tool_result = f"No handler for tool '{tc.name}'"

                tool_msg: dict[str, Any] = {
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tc.id,
                    "name": tc.name,
                }
                history.append(tool_msg)

            signal.set(session, history)
            await _continue_after_tools(session, signal, config, provider, history, model)
        else:
            assistant_msg = {"role": "assistant", "content": full_response}
            history.append(assistant_msg)

            if config.max_history and len(history) > config.max_history:
                history = history[-config.max_history :]

            signal.set(session, history)

    except Exception as e:
        logger.exception("Chat continuation error for signal '%s'", signal_name)
        await session.send_chat_done(signal_name)
        error_msg = {"role": "error", "content": str(e)}
        history.append(error_msg)
        signal.set(session, history)


# =============================================================================
# Stream wrapper — c.stream(fn) for streaming any async generator
# =============================================================================


async def stream_to_chat(
    session: Session,
    signal: Signal[list[Any]],
    fn: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    Stream a function's output token-by-token to a chat signal.

    The function should be an async generator yielding string chunks,
    or a sync generator (run in a thread).

    Example:
        async def my_stream(prompt: str):
            async for token in some_api(prompt):
                yield token

        await c.stream_to_chat(session, messages_signal, my_stream, "Hello")
    """
    import inspect

    signal_name = signal.name
    history: list[dict[str, Any]] = list(signal.get(session))
    full_response = ""

    try:
        if inspect.isasyncgenfunction(fn):
            async for token in fn(*args, **kwargs):
                text = str(token)
                full_response += text
                await session.send_chat_delta(signal_name, text)
        elif inspect.isgeneratorfunction(fn):
            loop = asyncio.get_running_loop()
            queue: asyncio.Queue[str | None] = asyncio.Queue()

            def _run() -> None:
                try:
                    for token in fn(*args, **kwargs):
                        asyncio.run_coroutine_threadsafe(queue.put(str(token)), loop).result()
                finally:
                    asyncio.run_coroutine_threadsafe(queue.put(None), loop).result()

            future = loop.run_in_executor(None, _run)
            while True:
                token = await queue.get()
                if token is None:
                    break
                full_response += token
                await session.send_chat_delta(signal_name, token)
            await future
        else:
            # Regular function — call it and treat result as single response
            result = fn(*args, **kwargs)
            if asyncio.iscoroutine(result):
                result = await result
            full_response = str(result)
            await session.send_chat_delta(signal_name, full_response)

        await session.send_chat_done(signal_name)

        # Add response to history
        assistant_msg = {"role": "assistant", "content": full_response}
        history.append(assistant_msg)
        signal.set(session, history)

    except Exception as e:
        logger.exception("Stream error for signal '%s'", signal_name)
        await session.send_chat_done(signal_name)
        error_msg = {"role": "error", "content": str(e)}
        history.append(error_msg)
        signal.set(session, history)


# =============================================================================
# Structured Extraction — c.extract(schema, text) via Prompture
# =============================================================================


async def extract_structured(
    text: str,
    *,
    schema: dict[str, Any] | None = None,
    pydantic_model: Any = None,
    model: str = "openai/gpt-4o",
    api_key: str | None = None,
) -> dict[str, Any]:
    """Extract structured data from text using Prompture.

    Args:
        text: The text to extract from.
        schema: JSON Schema for the desired output.
        pydantic_model: A Pydantic BaseModel class (alternative to schema).
        model: Model string in "provider/model" format.
        api_key: Optional API key override.

    Returns:
        Dict with 'result' (extracted data) and 'usage' (token/cost info).
    """
    try:
        from prompture import ask_for_json, extract_with_model
    except ImportError:
        raise ImportError(
            "prompture package is required for structured extraction. "
            "Install it with: pip install prompture"
        )

    kwargs: dict[str, Any] = {}
    if api_key:
        kwargs["api_key"] = api_key

    if pydantic_model is not None:
        result = extract_with_model(
            pydantic_model,
            text,
            model_name=model,
            **kwargs,
        )
        return {
            "result": result.model_dump() if hasattr(result, "model_dump") else result,
            "usage": {},
        }

    if schema is not None:
        response = ask_for_json(
            content_prompt=f"Extract the following information from this text:\n\n{text}",
            json_schema=schema,
            model_name=model,
            **kwargs,
        )
        return {
            "result": response.get("json_object", {}),
            "usage": response.get("usage", {}),
        }

    raise ValueError("Either 'schema' or 'pydantic_model' must be provided")


# =============================================================================
# Document Ingestion — parse uploaded files via Prompture
# =============================================================================


async def ingest_document(
    file_path: str,
    *,
    file_type: str | None = None,
    schema: dict[str, Any] | None = None,
    model: str = "openai/gpt-4o",
    api_key: str | None = None,
) -> dict[str, Any]:
    """Ingest a document and optionally extract structured data.

    Args:
        file_path: Path to the document (PDF, DOCX, CSV, etc.).
        file_type: Override auto-detection of file type.
        schema: If provided, extract structured data matching this JSON Schema.
        model: Model to use for extraction (if schema provided).
        api_key: Optional API key override.

    Returns:
        Dict with 'text' (parsed content), and optionally 'extracted' data.
    """
    try:
        from prompture.ingestion import ingest
    except ImportError:
        raise ImportError(
            "prompture package is required for document ingestion. "
            "Install it with: pip install prompture"
        )

    doc = await asyncio.to_thread(ingest, file_path, file_type=file_type)
    result: dict[str, Any] = {
        "text": doc.text,
        "metadata": {
            "source": str(file_path),
            "file_type": file_type or "auto",
            "length": len(doc.text),
        },
    }

    if schema is not None:
        extraction = await extract_structured(
            doc.text,
            schema=schema,
            model=model,
            api_key=api_key,
        )
        result["extracted"] = extraction.get("result", {})
        result["extraction_usage"] = extraction.get("usage", {})

    return result


# =============================================================================
# Model Discovery — list available providers/models via Prompture
# =============================================================================


def discover_models(
    *,
    grouped: bool = False,
    include_capabilities: bool = False,
) -> Any:
    """Discover available LLM models across all configured providers.

    Args:
        grouped: If True, group models by provider.
        include_capabilities: Include model capabilities metadata.

    Returns:
        List of model strings, or grouped dict if grouped=True.
    """
    try:
        from prompture import get_available_models
    except ImportError:
        raise ImportError(
            "prompture package is required for model discovery. "
            "Install it with: pip install prompture"
        )

    return get_available_models(
        grouped=grouped,
        include_capabilities=include_capabilities,
    )
