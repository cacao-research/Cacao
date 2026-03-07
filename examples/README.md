# Cacao Examples

## Simple (single file)

Small apps that fit in one file. Run any with `cacao run <file>`.

| Example | Description |
|---|---|
| `simple/hello.py` | 4-line hello world |
| `simple/counter.py` | Signals + event handling |
| `simple/metrics.py` | KPI dashboard in 10 lines |
| `simple/dashboard.py` | Charts + data tables |

## Standard (single file, more features)

Larger single-file apps with multiple pages, handlers, etc.

| Example | Description |
|---|---|
| `counter/app.py` | Counter with increment/decrement/reset |
| `todo/app.py` | Todo list with CRUD + filtering |
| `dashboard/app.py` | Sales dashboard with sidebar filters |
| `chat/app.py` | AI chat with Prompture streaming |

## Structured (multi-file)

Apps split into `pages/`, `components/`, `handlers/`, `data/`. See [docs/STRUCTURE.md](../docs/STRUCTURE.md) for the pattern.

| Example | Description |
|---|---|
| `analytics_dashboard/` | Full dashboard with 3 pages, sidebar, charts |

```
analytics_dashboard/
├── app.py              # Entry point
├── pages/
│   ├── overview.py     # KPIs + charts
│   ├── analytics.py    # Tabs + detailed breakdowns
│   └── monitor.py      # Real-time gauges
├── components/
│   └── sidebar.py      # Shared filter sidebar
├── handlers/
│   └── filters.py      # Filter event handlers
└── data/
    └── __init__.py     # Data generation
```

Run with: `cacao run examples/analytics_dashboard/app.py`
