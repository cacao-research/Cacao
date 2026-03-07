"""
Agent integration for Cacao — ReAct loop visualization with Prompture Agents.

Provides backend support for agent execution, tool call tracing, multi-agent
coordination (debate, router, pipeline), and real-time cost/budget tracking.

Example:
    import cacao as c

    c.agent(
        provider="openai",
        model="gpt-4o",
        tools=[weather_tool],
        tool_handlers={"get_weather": get_weather_fn},
        system_prompt="You are a helpful assistant with tool access.",
    )
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .llm import (
    ChatConfig,
    LLMProvider,
    StreamChunk,
    ToolCall,
    ToolSpec,
    UsageRecord,
    get_cost_tracker,
    get_provider,
)
from .log import get_logger
from .signal import Signal

if TYPE_CHECKING:
    from .session import Session

logger = get_logger("cacao.agent")


# =============================================================================
# Agent Step Types — the trace/timeline data model
# =============================================================================


@dataclass
class AgentStep:
    """A single step in the agent's ReAct loop."""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: str = ""  # "think", "tool_call", "tool_result", "response", "error"
    timestamp: float = field(default_factory=time.time)
    duration: float = 0.0
    content: str = ""
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    tool_result: str | None = None
    tokens: int = 0
    cost: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "duration": round(self.duration, 3),
            "content": self.content,
        }
        if self.tool_name:
            d["tool_name"] = self.tool_name
        if self.tool_args is not None:
            d["tool_args"] = self.tool_args
        if self.tool_result is not None:
            d["tool_result"] = self.tool_result
        if self.tokens:
            d["tokens"] = self.tokens
        if self.cost:
            d["cost"] = round(self.cost, 6)
        return d


# =============================================================================
# Agent Configuration
# =============================================================================


@dataclass
class AgentConfig:
    """Configuration for an agent instance."""

    provider: str | LLMProvider = "openai"
    model: str = "gpt-4o"
    system_prompt: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: list[ToolSpec] | None = None
    tool_handlers: dict[str, Callable[..., Any]] = field(default_factory=dict)
    max_iterations: int = 10  # ReAct loop limit
    max_cost: float | None = None
    max_budget_tokens: int | None = None
    fallback_model: str | None = None


# Registry of agent configs keyed by agent_id
_agent_configs: dict[str, AgentConfig] = {}


def register_agent(agent_id: str, config: AgentConfig) -> None:
    """Register an agent configuration."""
    _agent_configs[agent_id] = config


# =============================================================================
# Agent Execution — ReAct Loop
# =============================================================================


async def handle_agent_run(
    session: Session,
    agent_id: str,
    text: str,
) -> None:
    """
    Run the agent's ReAct loop: Think → Act → Observe → repeat.

    Sends real-time step updates to the client via WebSocket.
    """
    config = _agent_configs.get(agent_id)
    if not config:
        logger.warning("No agent config for id '%s'", agent_id)
        await session.send({"type": "agent:error", "agent_id": agent_id, "error": "Agent not configured"})
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
        await session.send({
            "type": "agent:error",
            "agent_id": agent_id,
            "error": f"Budget exceeded (${tracker.total_cost:.4f} spent)",
        })
        return

    # Determine model
    model = config.model
    if tracker.should_degrade() and tracker.fallback_model:
        model = tracker.fallback_model

    provider = get_provider(config.provider, api_key=config.api_key, base_url=config.base_url)

    # Build initial messages
    messages: list[dict[str, Any]] = []
    if config.system_prompt:
        messages.append({"role": "system", "content": config.system_prompt})
    messages.append({"role": "user", "content": text})

    steps: list[dict[str, Any]] = []
    iteration = 0

    # Notify start
    await session.send({
        "type": "agent:started",
        "agent_id": agent_id,
        "text": text,
    })

    try:
        while iteration < config.max_iterations:
            iteration += 1
            step_start = time.time()

            # Think step — send to LLM
            think_step = AgentStep(type="think", content="Reasoning...")
            await session.send({
                "type": "agent:step",
                "agent_id": agent_id,
                "step": think_step.to_dict(),
                "status": "running",
            })

            full_response = ""
            tool_calls: list[ToolCall] = []

            async for chunk in provider.stream(
                messages,
                model=model,
                system_prompt=None,  # already in messages
                tools=config.tools,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            ):
                if chunk.delta:
                    full_response += chunk.delta
                    # Stream thinking text
                    await session.send({
                        "type": "agent:delta",
                        "agent_id": agent_id,
                        "delta": chunk.delta,
                    })
                if chunk.tool_calls:
                    tool_calls.extend(chunk.tool_calls)

            step_duration = time.time() - step_start

            # Record cost
            meta = getattr(provider, "_last_meta", None)
            step_tokens = 0
            step_cost = 0.0
            if meta:
                step_tokens = meta.get("total_tokens", 0)
                step_cost = meta.get("cost", 0.0)
                provider_name = config.provider if isinstance(config.provider, str) else type(config.provider).__name__
                tracker.record(UsageRecord(
                    provider=provider_name,
                    model=model,
                    prompt_tokens=meta.get("prompt_tokens", 0),
                    completion_tokens=meta.get("completion_tokens", 0),
                    total_tokens=step_tokens,
                    cost=step_cost,
                ))

            # Update think step as complete
            think_step.content = full_response
            think_step.duration = step_duration
            think_step.tokens = step_tokens
            think_step.cost = step_cost
            steps.append(think_step.to_dict())

            await session.send({
                "type": "agent:step",
                "agent_id": agent_id,
                "step": think_step.to_dict(),
                "status": "done",
            })

            if not tool_calls:
                # No tools to call — agent is done, emit final response
                response_step = AgentStep(
                    type="response",
                    content=full_response,
                    tokens=step_tokens,
                    cost=step_cost,
                )
                steps.append(response_step.to_dict())

                await session.send({
                    "type": "agent:step",
                    "agent_id": agent_id,
                    "step": response_step.to_dict(),
                    "status": "done",
                })
                break

            # Act step — execute tool calls
            messages.append({
                "role": "assistant",
                "content": full_response,
                "tool_calls": [tc.to_dict() for tc in tool_calls],
            })

            for tc in tool_calls:
                tc_start = time.time()

                # Notify tool call start
                tool_step = AgentStep(
                    type="tool_call",
                    tool_name=tc.name,
                    tool_args=tc.parsed_arguments,
                    content=f"Calling {tc.name}...",
                )
                await session.send({
                    "type": "agent:step",
                    "agent_id": agent_id,
                    "step": tool_step.to_dict(),
                    "status": "running",
                })

                # Execute handler
                handler = config.tool_handlers.get(tc.name)
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

                tc_duration = time.time() - tc_start

                # Update tool step
                tool_step.tool_result = tool_result
                tool_step.duration = tc_duration
                tool_step.content = f"{tc.name} completed"
                steps.append(tool_step.to_dict())

                await session.send({
                    "type": "agent:step",
                    "agent_id": agent_id,
                    "step": tool_step.to_dict(),
                    "status": "done",
                })

                # Add tool result to messages for next iteration
                messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tc.id,
                    "name": tc.name,
                })

            # Budget check between iterations
            if tracker.is_over_budget():
                await session.send({
                    "type": "agent:error",
                    "agent_id": agent_id,
                    "error": f"Budget exceeded during execution (${tracker.total_cost:.4f})",
                })
                break

            # Degrade model if needed
            if tracker.should_degrade() and tracker.fallback_model:
                model = tracker.fallback_model

        # Send final summary
        await session.send({
            "type": "agent:done",
            "agent_id": agent_id,
            "steps": steps,
            "iterations": iteration,
            "total_cost": round(tracker.total_cost, 6),
            "total_tokens": tracker.total_tokens,
        })

        # Send budget update for budget gauge
        await session.send({
            "type": "agent:budget_update",
            "agent_id": agent_id,
            "summary": tracker.summary(),
        })

    except Exception as e:
        logger.exception("Agent error for id '%s'", agent_id)
        error_step = AgentStep(type="error", content=str(e))
        steps.append(error_step.to_dict())
        await session.send({
            "type": "agent:error",
            "agent_id": agent_id,
            "error": str(e),
            "steps": steps,
        })


# =============================================================================
# Multi-Agent Execution
# =============================================================================


@dataclass
class MultiAgentConfig:
    """Configuration for a multi-agent setup."""

    mode: str = "debate"  # "debate", "router", "pipeline"
    agents: list[AgentConfig] = field(default_factory=list)
    agent_names: list[str] = field(default_factory=list)
    rounds: int = 3  # for debate mode
    router_prompt: str | None = None  # for router mode


_multi_agent_configs: dict[str, MultiAgentConfig] = {}


def register_multi_agent(multi_id: str, config: MultiAgentConfig) -> None:
    """Register a multi-agent configuration."""
    _multi_agent_configs[multi_id] = config


async def handle_multi_agent_run(
    session: Session,
    multi_id: str,
    text: str,
) -> None:
    """Run a multi-agent session based on mode."""
    config = _multi_agent_configs.get(multi_id)
    if not config:
        await session.send({
            "type": "multi_agent:error",
            "multi_id": multi_id,
            "error": "Multi-agent config not found",
        })
        return

    await session.send({
        "type": "multi_agent:started",
        "multi_id": multi_id,
        "mode": config.mode,
        "text": text,
    })

    try:
        if config.mode == "debate":
            await _run_debate(session, multi_id, config, text)
        elif config.mode == "router":
            await _run_router(session, multi_id, config, text)
        elif config.mode == "pipeline":
            await _run_pipeline(session, multi_id, config, text)
        else:
            await session.send({
                "type": "multi_agent:error",
                "multi_id": multi_id,
                "error": f"Unknown mode: {config.mode}",
            })
    except Exception as e:
        logger.exception("Multi-agent error for '%s'", multi_id)
        await session.send({
            "type": "multi_agent:error",
            "multi_id": multi_id,
            "error": str(e),
        })


async def _run_debate(
    session: Session,
    multi_id: str,
    config: MultiAgentConfig,
    text: str,
) -> None:
    """Run agents in debate mode — each takes turns responding."""
    responses: list[dict[str, Any]] = []
    context = f"Topic: {text}\n\n"

    for round_num in range(config.rounds):
        for i, agent_config in enumerate(config.agents):
            agent_name = config.agent_names[i] if i < len(config.agent_names) else f"Agent {i + 1}"
            provider = get_provider(agent_config.provider, api_key=agent_config.api_key, base_url=agent_config.base_url)
            model = agent_config.model

            # Build messages with debate context
            debate_prompt = (
                f"{context}"
                f"You are {agent_name}. This is round {round_num + 1} of a debate. "
                f"Respond with your perspective."
            )
            messages: list[dict[str, Any]] = []
            if agent_config.system_prompt:
                messages.append({"role": "system", "content": agent_config.system_prompt})
            messages.append({"role": "user", "content": debate_prompt})

            await session.send({
                "type": "multi_agent:turn",
                "multi_id": multi_id,
                "agent_name": agent_name,
                "agent_index": i,
                "round": round_num + 1,
                "status": "running",
            })

            full_response = ""
            async for chunk in provider.stream(
                messages, model=model,
                temperature=agent_config.temperature,
                max_tokens=agent_config.max_tokens,
            ):
                if chunk.delta:
                    full_response += chunk.delta
                    await session.send({
                        "type": "multi_agent:delta",
                        "multi_id": multi_id,
                        "agent_index": i,
                        "delta": chunk.delta,
                    })

            entry = {
                "agent_name": agent_name,
                "agent_index": i,
                "round": round_num + 1,
                "content": full_response,
            }
            responses.append(entry)
            context += f"\n{agent_name} (Round {round_num + 1}): {full_response}\n"

            await session.send({
                "type": "multi_agent:turn",
                "multi_id": multi_id,
                "agent_name": agent_name,
                "agent_index": i,
                "round": round_num + 1,
                "content": full_response,
                "status": "done",
            })

    await session.send({
        "type": "multi_agent:done",
        "multi_id": multi_id,
        "mode": "debate",
        "responses": responses,
    })


async def _run_router(
    session: Session,
    multi_id: str,
    config: MultiAgentConfig,
    text: str,
) -> None:
    """Run router mode — a router decides which agent handles the request."""
    # Use first agent's provider for routing decision
    if not config.agents:
        await session.send({
            "type": "multi_agent:error", "multi_id": multi_id, "error": "No agents configured",
        })
        return

    router_config = config.agents[0]
    provider = get_provider(router_config.provider, api_key=router_config.api_key, base_url=router_config.base_url)

    agent_descriptions = "\n".join(
        f"- {config.agent_names[i] if i < len(config.agent_names) else f'Agent {i + 1}'}: "
        f"{a.system_prompt or 'General purpose agent'}"
        for i, a in enumerate(config.agents)
    )

    router_prompt = config.router_prompt or (
        f"Given these agents:\n{agent_descriptions}\n\n"
        f"Which agent should handle this request? Reply with ONLY the agent name.\n\n"
        f"Request: {text}"
    )

    messages: list[dict[str, Any]] = [{"role": "user", "content": router_prompt}]

    await session.send({
        "type": "multi_agent:routing",
        "multi_id": multi_id,
        "status": "running",
    })

    # Get routing decision
    full_response = ""
    async for chunk in provider.stream(messages, model=router_config.model):
        if chunk.delta:
            full_response += chunk.delta

    # Find matching agent
    chosen_idx = 0
    for i, name in enumerate(config.agent_names):
        if name.lower() in full_response.lower():
            chosen_idx = i
            break

    chosen_name = config.agent_names[chosen_idx] if chosen_idx < len(config.agent_names) else f"Agent {chosen_idx + 1}"
    chosen_config = config.agents[chosen_idx]

    await session.send({
        "type": "multi_agent:routing",
        "multi_id": multi_id,
        "chosen_agent": chosen_name,
        "chosen_index": chosen_idx,
        "reason": full_response.strip(),
        "status": "done",
    })

    # Run the chosen agent
    chosen_provider = get_provider(chosen_config.provider, api_key=chosen_config.api_key, base_url=chosen_config.base_url)
    agent_messages: list[dict[str, Any]] = []
    if chosen_config.system_prompt:
        agent_messages.append({"role": "system", "content": chosen_config.system_prompt})
    agent_messages.append({"role": "user", "content": text})

    await session.send({
        "type": "multi_agent:turn",
        "multi_id": multi_id,
        "agent_name": chosen_name,
        "agent_index": chosen_idx,
        "status": "running",
    })

    agent_response = ""
    async for chunk in chosen_provider.stream(
        agent_messages, model=chosen_config.model,
        temperature=chosen_config.temperature,
        max_tokens=chosen_config.max_tokens,
    ):
        if chunk.delta:
            agent_response += chunk.delta
            await session.send({
                "type": "multi_agent:delta",
                "multi_id": multi_id,
                "agent_index": chosen_idx,
                "delta": chunk.delta,
            })

    await session.send({
        "type": "multi_agent:turn",
        "multi_id": multi_id,
        "agent_name": chosen_name,
        "agent_index": chosen_idx,
        "content": agent_response,
        "status": "done",
    })

    await session.send({
        "type": "multi_agent:done",
        "multi_id": multi_id,
        "mode": "router",
        "chosen_agent": chosen_name,
        "response": agent_response,
    })


async def _run_pipeline(
    session: Session,
    multi_id: str,
    config: MultiAgentConfig,
    text: str,
) -> None:
    """Run pipeline mode — agents process sequentially, each getting the previous output."""
    current_input = text
    pipeline_results: list[dict[str, Any]] = []

    for i, agent_config in enumerate(config.agents):
        agent_name = config.agent_names[i] if i < len(config.agent_names) else f"Agent {i + 1}"
        provider = get_provider(agent_config.provider, api_key=agent_config.api_key, base_url=agent_config.base_url)

        messages: list[dict[str, Any]] = []
        if agent_config.system_prompt:
            messages.append({"role": "system", "content": agent_config.system_prompt})
        messages.append({"role": "user", "content": current_input})

        await session.send({
            "type": "multi_agent:turn",
            "multi_id": multi_id,
            "agent_name": agent_name,
            "agent_index": i,
            "pipeline_step": i + 1,
            "pipeline_total": len(config.agents),
            "status": "running",
        })

        full_response = ""
        async for chunk in provider.stream(
            messages, model=agent_config.model,
            temperature=agent_config.temperature,
            max_tokens=agent_config.max_tokens,
        ):
            if chunk.delta:
                full_response += chunk.delta
                await session.send({
                    "type": "multi_agent:delta",
                    "multi_id": multi_id,
                    "agent_index": i,
                    "delta": chunk.delta,
                })

        entry = {
            "agent_name": agent_name,
            "agent_index": i,
            "input": current_input,
            "output": full_response,
        }
        pipeline_results.append(entry)
        current_input = full_response  # pass output to next agent

        await session.send({
            "type": "multi_agent:turn",
            "multi_id": multi_id,
            "agent_name": agent_name,
            "agent_index": i,
            "content": full_response,
            "status": "done",
        })

    await session.send({
        "type": "multi_agent:done",
        "multi_id": multi_id,
        "mode": "pipeline",
        "results": pipeline_results,
        "final_output": current_input,
    })
