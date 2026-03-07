"""
Tukuy Skills integration for Cacao.

Provides server-side handlers for:
- Skill invocation (c.skill)
- Skill discovery/browsing (c.skill_browser)
- Chain execution (c.chain_builder)
- Tukuy transformer bridge (replaces Phase 6 JS handlers)
- Safety policy management (c.safety_policy)
"""

from __future__ import annotations

import asyncio
import traceback
from typing import Any

from .log import get_logger
from .session import Session

logger = get_logger("cacao.tukuy")


# =============================================================================
# Lazy Tukuy imports (graceful fallback if not installed)
# =============================================================================


def _get_tukuy() -> Any:
    """Import tukuy lazily. Raises ImportError if not installed."""
    try:
        import tukuy

        return tukuy
    except ImportError:
        raise ImportError(
            "Tukuy is required for skill components. Install it with: pip install tukuy"
        )


# =============================================================================
# Skill Invocation
# =============================================================================


async def handle_skill_invoke(
    session: Session,
    skill_name: str,
    inputs: dict[str, Any],
    invoke_id: str,
) -> None:
    """Invoke a Tukuy skill and send the result back to the client."""
    try:
        _get_tukuy()
        from tukuy import get_tool_details

        # Find the skill
        details = get_tool_details(skill_name)
        if not details:
            await session.send(
                {
                    "type": "skill:error",
                    "id": invoke_id,
                    "error": f"Skill '{skill_name}' not found",
                }
            )
            return

        details[0]

        # Get the actual skill object from the plugin system
        from tukuy.availability import get_available_skills
        from tukuy.plugin import discover_plugins

        plugins = discover_plugins()
        availability = get_available_skills(plugins=plugins)

        skill_obj = None
        for avail in availability:
            if avail.skill.descriptor.name == skill_name:
                skill_obj = avail.skill
                break

        if skill_obj is None:
            await session.send(
                {
                    "type": "skill:error",
                    "id": invoke_id,
                    "error": f"Skill '{skill_name}' could not be loaded",
                }
            )
            return

        # Invoke the skill
        result = await asyncio.to_thread(skill_obj.invoke, **inputs)

        await session.send(
            {
                "type": "skill:result",
                "id": invoke_id,
                "value": result.value if result.success else None,
                "error": str(result.error) if result.error else None,
                "success": result.success,
                "duration_ms": result.duration_ms,
                "metadata": result.metadata if hasattr(result, "metadata") else {},
            }
        )

    except Exception as e:
        logger.warning("Skill invoke error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "skill:error",
                "id": invoke_id,
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
        )


# =============================================================================
# Skill Discovery
# =============================================================================


async def handle_skill_browse(session: Session) -> None:
    """Browse all available Tukuy skills."""
    try:
        _get_tukuy()
        from tukuy import browse_tools

        index = await asyncio.to_thread(browse_tools)

        await session.send(
            {
                "type": "skill:browse_result",
                "index": index,
            }
        )

    except Exception as e:
        logger.warning("Skill browse error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "skill:browse_error",
                "error": str(e),
            }
        )


async def handle_skill_search(
    session: Session,
    query: str,
    limit: int = 20,
) -> None:
    """Search Tukuy skills by keyword."""
    try:
        _get_tukuy()
        from tukuy import search_tools

        results = await asyncio.to_thread(search_tools, query, limit=limit)

        await session.send(
            {
                "type": "skill:search_result",
                "query": query,
                "results": results,
            }
        )

    except Exception as e:
        logger.warning("Skill search error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "skill:search_error",
                "error": str(e),
            }
        )


async def handle_skill_details(
    session: Session,
    skill_names: list[str],
) -> None:
    """Get detailed info for specific skills."""
    try:
        _get_tukuy()
        from tukuy import get_tool_details

        details = await asyncio.to_thread(get_tool_details, *skill_names)

        await session.send(
            {
                "type": "skill:details_result",
                "details": details,
            }
        )

    except Exception as e:
        logger.warning("Skill details error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "skill:details_error",
                "error": str(e),
            }
        )


# =============================================================================
# Chain Execution
# =============================================================================


async def handle_chain_run(
    session: Session,
    chain_id: str,
    steps: list[dict[str, Any]],
    input_value: Any,
) -> None:
    """Execute a Tukuy chain and stream step-by-step results."""
    try:
        _get_tukuy()
        from tukuy import Chain

        # Build steps from serialized definitions
        resolved_steps = _resolve_chain_steps(steps)

        Chain(resolved_steps)

        # Send start notification
        await session.send(
            {
                "type": "chain:started",
                "id": chain_id,
                "step_count": len(resolved_steps),
            }
        )

        # Run the chain (we can't easily intercept per-step in Chain,
        # so we run sequentially and report each step)
        current_value = input_value
        for i, step_def in enumerate(steps):
            step_name = step_def.get("name", f"step_{i}")
            step_chain = Chain([resolved_steps[i]])

            try:
                result = await asyncio.to_thread(step_chain.run, current_value)
                current_value = result

                await session.send(
                    {
                        "type": "chain:step_result",
                        "id": chain_id,
                        "step_index": i,
                        "step_name": step_name,
                        "value": _serialize_value(result),
                        "success": True,
                    }
                )
            except Exception as step_error:
                await session.send(
                    {
                        "type": "chain:step_result",
                        "id": chain_id,
                        "step_index": i,
                        "step_name": step_name,
                        "error": str(step_error),
                        "success": False,
                    }
                )
                # Stop the chain on error
                await session.send(
                    {
                        "type": "chain:error",
                        "id": chain_id,
                        "error": f"Step '{step_name}' failed: {step_error}",
                    }
                )
                return

        await session.send(
            {
                "type": "chain:result",
                "id": chain_id,
                "value": _serialize_value(current_value),
            }
        )

    except Exception as e:
        logger.warning("Chain run error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "chain:error",
                "id": chain_id,
                "error": str(e),
            }
        )


def _resolve_chain_steps(steps: list[dict[str, Any]]) -> list[Any]:
    """Resolve serialized step definitions into Tukuy chain steps."""
    resolved = []
    for step in steps:
        step_type = step.get("type", "transformer")
        name = step.get("name", "")

        if step_type == "transformer":
            # Simple transformer by name (e.g., "strip", "lowercase")
            if step.get("params"):
                resolved.append({"function": name, **step["params"]})
            else:
                resolved.append(name)
        elif step_type == "skill":
            resolved.append(name)
        elif step_type == "branch":
            from tukuy import Branch

            true_path = _resolve_chain_steps(step.get("true_path", []))
            false_path = _resolve_chain_steps(step.get("false_path", []))
            resolved.append(
                Branch(
                    on_match=lambda v, cond=step.get("condition", ""): (
                        bool(v) if not cond else eval(cond, {"v": v})
                    ),
                    true_path=true_path,
                    false_path=false_path if false_path else None,
                )
            )
        elif step_type == "parallel":
            from tukuy import Parallel

            sub_steps = _resolve_chain_steps(step.get("steps", []))
            resolved.append(
                Parallel(
                    steps=sub_steps,
                    merge=step.get("merge", "dict"),
                )
            )

    return resolved


def _serialize_value(value: Any) -> Any:
    """Serialize a value for JSON transport."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_serialize_value(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _serialize_value(v) for k, v in value.items()}
    return str(value)


# =============================================================================
# Tukuy Transformer Bridge (replaces Phase 6 JS handlers)
# =============================================================================


async def handle_transform(
    session: Session,
    transform_id: str,
    transformer_name: str,
    input_value: Any,
    params: dict[str, Any] | None = None,
) -> None:
    """Run a Tukuy transformer server-side (replaces client-side JS handlers)."""
    try:
        _get_tukuy()
        from tukuy import Chain

        step: Any
        if params:
            step = {"function": transformer_name, **params}
        else:
            step = transformer_name

        chain = Chain([step])
        result = await asyncio.to_thread(chain.run, input_value)

        await session.send(
            {
                "type": "transform:result",
                "id": transform_id,
                "value": _serialize_value(result),
            }
        )

    except Exception as e:
        logger.warning("Transform error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "transform:error",
                "id": transform_id,
                "error": str(e),
            }
        )


async def handle_transform_list(session: Session) -> None:
    """List all available Tukuy transformers (for the transformer bridge)."""
    try:
        _get_tukuy()
        from tukuy import browse_tools

        index = await asyncio.to_thread(browse_tools)

        # Extract just transformer names grouped by plugin
        transformers: dict[str, list[str]] = {}
        for plugin_name, plugin_info in index.get("plugins", {}).items():
            tools = list(plugin_info.get("tools", {}).keys())
            if tools:
                transformers[plugin_name] = tools

        await session.send(
            {
                "type": "transform:list_result",
                "transformers": transformers,
                "total_count": index.get("total_count", 0),
            }
        )

    except Exception as e:
        logger.warning("Transform list error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "transform:list_error",
                "error": str(e),
            }
        )


# =============================================================================
# Safety Policy Management
# =============================================================================

# Per-session safety policies
_session_policies: dict[str, Any] = {}


async def handle_safety_set(
    session: Session,
    policy_config: dict[str, Any],
) -> None:
    """Set the Tukuy safety policy for the current session."""
    try:
        _get_tukuy()
        from tukuy import SafetyPolicy

        preset = policy_config.get("preset")
        if preset == "restrictive":
            policy = SafetyPolicy.restrictive()
        elif preset == "permissive":
            policy = SafetyPolicy.permissive()
        elif preset == "network_only":
            policy = SafetyPolicy.network_only()
        elif preset == "filesystem_only":
            policy = SafetyPolicy.filesystem_only()
        else:
            # Custom policy
            policy = SafetyPolicy(
                allowed_imports=set(policy_config.get("allowed_imports", [])) or None,
                blocked_imports=set(policy_config.get("blocked_imports", [])) or None,
                allow_network=policy_config.get("allow_network", True),
                allow_filesystem=policy_config.get("allow_filesystem", True),
            )

        _session_policies[session.id] = policy

        await session.send(
            {
                "type": "safety:set_result",
                "success": True,
                "policy": {
                    "preset": preset,
                    "allowed_imports": list(policy.allowed_imports)
                    if policy.allowed_imports
                    else None,
                    "blocked_imports": list(policy.blocked_imports)
                    if policy.blocked_imports
                    else None,
                    "allow_network": policy.allow_network,
                    "allow_filesystem": policy.allow_filesystem,
                },
            }
        )

    except Exception as e:
        logger.warning("Safety policy error: %s", e, extra={"label": "tukuy"})
        await session.send(
            {
                "type": "safety:set_error",
                "error": str(e),
            }
        )


async def handle_safety_get(session: Session) -> None:
    """Get the current safety policy for this session."""
    try:
        policy = _session_policies.get(session.id)

        if policy is None:
            await session.send(
                {
                    "type": "safety:get_result",
                    "policy": None,
                    "message": "No policy set (unrestricted)",
                }
            )
            return

        await session.send(
            {
                "type": "safety:get_result",
                "policy": {
                    "allowed_imports": list(policy.allowed_imports)
                    if policy.allowed_imports
                    else None,
                    "blocked_imports": list(policy.blocked_imports)
                    if policy.blocked_imports
                    else None,
                    "allow_network": policy.allow_network,
                    "allow_filesystem": policy.allow_filesystem,
                },
            }
        )

    except Exception as e:
        await session.send(
            {
                "type": "safety:get_error",
                "error": str(e),
            }
        )


def get_session_policy(session_id: str) -> Any | None:
    """Get the safety policy for a session (used by skill invocation)."""
    return _session_policies.get(session_id)


def cleanup_session_policy(session_id: str) -> None:
    """Remove safety policy when session ends."""
    _session_policies.pop(session_id, None)
