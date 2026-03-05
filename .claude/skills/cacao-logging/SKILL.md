---
name: cacao-logging
description: Add logs to Cacao server code. Use when adding debug messages, error logging, info output, or replacing print() calls in any server module. Covers the unified logging system, labels, log levels, and how uvicorn output is formatted.
---

# Cacao Logging Guide

All server-side logging goes through a unified system in `cacao/server/log.py`. Never use bare `print()` for operational messages — use the logger so output stays aligned and respects `--verbose`.

## Output Format

```
  HH:MM:SS  label   message
```

- 2-space indent
- Dim timestamp
- Brown fixed-width label (8 chars)
- Message

Examples:
```
  12:34:56  ready   Listening on http://127.0.0.1:1502
  12:34:57  GET     / 200
  12:34:57  ws      Connection opened
  12:34:57  event   Event: increment {'value': 1}
  12:34:58  persist Save error for count: IOError
```

## Quick Start

```python
from .log import get_logger

logger = get_logger("cacao.mymodule")

# INFO — always visible
logger.info("Something happened", extra={"label": "ready"})

# DEBUG — only visible with --verbose
logger.debug("Session %s connected", sid, extra={"label": "ws"})

# WARNING — always visible
logger.warning("Invalid JSON: %s", data, extra={"label": "ws"})

# ERROR — always visible
logger.error("Save failed: %s", e, extra={"label": "persist"})
```

## Rules

### 1. Always pass `extra={"label": "..."}`

The label is the category tag that appears in the log line. Keep it short (max 8 chars). Common labels:

| Label | Use |
|-------|-----|
| `ready` | Server startup/ready messages |
| `ws` | WebSocket connect/disconnect/errors |
| `event` | Event dispatch and handling |
| `effect` | Effect execution errors |
| `watch` | Watch callback errors |
| `persist` | Persistence save/restore/delete errors |
| `log` | Default fallback (avoid using explicitly) |

### 2. Use the right log level

| Level | When | Visible by default? |
|-------|------|---------------------|
| `DEBUG` | Session connect/disconnect, event details, internal state | No (only with `--verbose`) |
| `INFO` | Server ready, important state changes | Yes |
| `WARNING` | Recoverable issues (bad JSON, unexpected state) | Yes |
| `ERROR` | Failures that need attention (effect crash, persistence failure) | Yes |

### 3. Use %-formatting, not f-strings

```python
# Right — lazy evaluation, no work if level is filtered
logger.debug("Session %s connected", session.id, extra={"label": "ws"})

# Wrong — f-string always evaluates
logger.debug(f"Session {session.id} connected", extra={"label": "ws"})
```

### 4. No `if app.debug:` guards

The log level handles filtering. Just log at the right level:

```python
# Wrong
if app.debug:
    print(f"[Cacao] Session {session.id} connected")

# Right
logger.debug("Session %s connected", session.id, extra={"label": "ws"})
```

### 5. No `print()` for operational messages

```python
# Wrong
print(f"Effect '{name}' error: {e}")

# Right
logger.error("Effect '%s': %s", name, e, extra={"label": "effect"})
```

`print()` is still fine for:
- CLI banner output (`commands.py`) — that's UI, not logging
- Fatal pre-server errors in `runner.py`

## Adding Logging to a New Module

### Step 1: Import and create logger

```python
from .log import get_logger

_logger = get_logger("cacao.mymodule")
```

Use a module-level `_logger` (underscore = private). The name must start with `cacao.` to inherit the unified config.

### Step 2: Replace print() calls

```python
# Before
print(f"Something failed for {name}: {e}")

# After
_logger.error("Something failed for %s: %s", name, e, extra={"label": "mymod"})
```

### Step 3: Choose a label

Pick an existing label from the table above, or create a new one if the module is a distinct category. Keep it <= 8 chars.

## Architecture

### Files

| File | Role |
|------|------|
| `cacao/server/log.py` | Formatters, filters, config, `get_logger()` |
| `cacao/server/server.py` | Uses `logger` for ws/event/ready messages |
| `cacao/server/effects.py` | Uses `_logger` for effect/watch errors |
| `cacao/server/persist.py` | Uses `_logger` for persistence errors |
| `cacao/server/middleware.py` | `logging_middleware()` defaults to logger |

### How It Works

```
get_logger("cacao.xxx")          →  logging.getLogger("cacao.xxx")
                                       ↓
_ensure_cacao_handler()          →  Bootstraps a CacaoFormatter handler
                                    on the "cacao" root logger (if none exists)
                                       ↓
get_uvicorn_log_config(debug)    →  dictConfig passed to uvicorn.run()
                                    - CacaoFormatter for uvicorn.error
                                    - CacaoAccessFormatter for uvicorn.access
                                    - UvicornStartupFilter suppresses noisy msgs
                                    - Sets cacao logger to DEBUG if debug=True
```

### UvicornStartupFilter

Suppresses these messages (the banner already shows them):
- "Started server process [pid]"
- "Waiting for application startup"
- "Uvicorn running on http://..."
- "Application startup complete."

### CacaoAccessFormatter

Parses uvicorn's access log tuple `(client, method, path, http_ver, status)` and formats it as:
```
  12:34:57  GET     /path 200
```

## Verbose Mode

`--verbose` (or `app.debug = True`) sets the `cacao` logger to DEBUG level. This surfaces:
- WebSocket session connect/disconnect
- Event names and payloads
- Any other `logger.debug()` calls

Without `--verbose`, only INFO+ is shown.

## Checklist

When adding logging to Cacao server code:

- [ ] Import `get_logger` from `.log`
- [ ] Create module-level logger: `_logger = get_logger("cacao.xxx")`
- [ ] Use `extra={"label": "..."}` on every log call
- [ ] Use %-style formatting, not f-strings
- [ ] Use DEBUG for detailed/noisy info, INFO for important state, ERROR for failures
- [ ] No `if app.debug:` guards — log level handles it
- [ ] No bare `print()` for operational messages
