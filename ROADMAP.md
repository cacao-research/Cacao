# Cacao v2 Development Roadmap

> **Target competitor: Gradio** — Cacao should be what Gradio wishes it was: function-wrapping simplicity with real app-building power.

---

## Completed Phases

### Phase 1: Core Server ✅
- [x] Signal — Reactive state with session scoping
- [x] Computed — Derived state from signals
- [x] Session / SessionManager — Per-client isolation
- [x] EventRegistry — Event handling with auto-binding
- [x] App — Main class with decorators (@app.on, @app.route)
- [x] WebSocket server (Starlette + Uvicorn)
- [x] State sync protocol (init, update, batch)

### Phase 2: Component Library ✅
- [x] Layout — Row, Col, Grid, Container, Stack, Split, Hero, AppShell, NavSidebar, Panel
- [x] Form — Button, Input, Select, Checkbox, Switch, Slider, DatePicker, FileUpload, Textarea, SearchInput
- [x] Display — Card, Metric, Table, Alert, Badge, Progress, Accordion, Modal, Tooltip, Timeline, Diff, JsonView, Steps, FileTree
- [x] Typography — Title, Text, Code, Divider, Markdown, Html, Spacer
- [x] Navigation — Tabs, Breadcrumb, Sidebar, SubNav

### Phase 3: Charts & Data ✅
- [x] 11 chart types — Line, Bar, Pie, Scatter, Area, Gauge, Heatmap, Funnel, Radar, Treemap, Donut
- [x] DataFrame — Custom lightweight DataFrame with filter, sort, group_by, aggregate
- [x] Data loaders — CSV, JSON, Parquet with auto-type conversion
- [x] Sample data generators

### Phase 4: Advanced Server ✅
- [x] Effect / Watch — Side effects on signal changes
- [x] Batch — Batch multiple signal updates
- [x] Middleware chain — Rate limit, auth, validation, transform, timeout, logging
- [x] Plugin registry — Lifecycle hooks, UI slots, event bus
- [x] Auth system — SimpleAuthProvider, permissions, token-based
- [x] Notifications — Toasts, persistent notifications, broadcast

### Phase 5: Fluent API & Static Builds ✅
- [x] Simple API — `import cacao as c` with lazy app creation
- [x] Context managers — `with c.row():`, `with c.card():`
- [x] Multi-page routing — Hash-based SPA routing
- [x] Static export — `cacao build` for serverless deployment
- [x] Built-in handlers — Encoders, generators, converters, text, crypto
- [x] CLI — `cacao run`, `cacao build`, `cacao create`
- [x] Hot reload — File watching with auto-restart
- [x] Themes — Dark, light, tukuy, tukuy-light

### Phase 6: cacao_tools Port ✅
- [x] Encoders — Base64, URL, HTML, JWT, hex, CSV
- [x] Generators — UUID, passwords, Lorem Ipsum, random data
- [x] Converters — YAML, case conversion, number bases
- [x] Text — Stats, regex, reverse, word wrap
- [x] Crypto — SHA-256, MD5, HMAC

---

## Competitive Analysis

### Why Gradio is the target

Gradio owns the "wrap a function, get a UI" space. Its `gr.Interface(fn, inputs, outputs)` pattern is the fastest way to go from Python function to shareable demo. But it hits a wall fast:

- **Layout prison** — Stuck in input/output box model. Anything beyond a demo fights the framework.
- **Not for real apps** — No state management, no multi-page, no middleware. It's a demo tool.
- **No static builds** — Always needs a server running.
- **No session isolation** — Shared state across users.

Cacao already beats Gradio on: layout flexibility, real reactivity, component richness, session isolation, static builds, plugin architecture. The roadmap closes the gaps where Gradio wins.

### What we take from each competitor

| Competitor | Steal this | Avoid this |
|------------|-----------|------------|
| **Gradio** | Function wrapping, auto-UI generation, HF Spaces integration | Input/output box prison, no real state |
| **Streamlit** | One-file simplicity, instant gratification | Full-rerun model, session_state bolted on |
| **Reflex** | Full-stack ambition, production-grade goal | Compilation complexity, breaking changes |
| **Marimo** | Reactive notebook, export-as-app | Tiny ecosystem, breaks common Python patterns |
| **NiceGUI** | Real-time sync, desktop-style feel | Scaling issues, laggy with complex state |
| **Flet** | Cross-platform output (web + desktop) | Flutter bloat, massive runtime |
| **Panel** | Plays well with data ecosystem | Steep learning curve, overwhelming API |

---

## Phase 7: Function Wrapping (The Gradio Killer Feature) ✅

> **Goal:** Match Gradio's `gr.Interface()` simplicity, then surpass it with Cacao's layout system.

### 7.1 Auto-Interface ✅
- [x] `c.interface(fn, inputs, outputs)` — Wrap any function into a full UI
- [x] Auto-detect input types from type hints (str -> input, int -> slider, bool -> checkbox, list -> select)
- [x] Auto-detect output types (str -> text, dict -> json_view, list -> table, plt.Figure -> image)
- [x] Support for `Annotated[str, c.TextArea()]` to override defaults
- [x] Loading states while function runs
- [x] Error display when function raises

### 7.2 Composable Interfaces ✅
- [x] `c.parallel(fn1, fn2)` — Side-by-side interfaces (Gradio's Parallel)
- [x] `c.series(fn1, fn2)` — Chain function outputs to inputs (Gradio's Series)
- [x] `c.compare(fn1, fn2)` — Run same inputs through multiple functions, compare outputs
- [x] Mix interfaces with manual layout: `with c.row(): c.interface(fn); c.metric(...)`

### 7.3 Advanced Input/Output Types ✅
- [x] Image input/output with preview
- [x] Audio input/output with waveform
- [x] Video input/output with player
- [x] File input/output with drag-and-drop
- [x] DataFrame input (editable table) / output (rendered table)
- [x] Plot output (matplotlib, plotly figures auto-rendered)
- [x] Chatbot output type (streaming conversation)

### 7.4 Examples & Flagging ✅
- [x] `c.interface(fn, examples=[[...], [...]])` — Clickable example inputs
- [x] Flagging system — Users can flag bad outputs for review
- [x] Output caching — Cache results for identical inputs

---

## Phase 8: AI-Powered Apps (Tukuy + Prompture Integration)

> **Goal:** Make Cacao the best framework for AI-powered apps by integrating [Prompture](https://github.com/jhd3197/prompture) (multi-provider LLM engine) and [Tukuy](https://github.com/jhd3197/Tukuy) (skills & transformation toolkit) as first-class backends.

### 8.1 Streaming & LLM Integration ✅
- [x] `c.chat()` with real streaming backend (SSE + WebSocket)
- [x] `c.stream(fn)` — Stream function output token-by-token
- [x] Built-in adapters: OpenAI, Anthropic, local models (ollama)
- [x] Conversation memory with session-scoped history
- [x] System prompt configuration
- [x] Tool/function calling UI (show tool calls inline)

### 8.2 Prompture Backend ✅
- [x] Replace `llm.py` provider internals with Prompture drivers (15+ providers)
- [x] Structured extraction UI — `c.extract(schema, text)` powered by Prompture
- [x] Cost tracking dashboard — per-session token counts, USD costs, model comparison
- [x] Budget enforcement — `max_cost`, `max_tokens`, auto-degrade to cheaper models
- [x] Document ingestion — upload PDF/DOCX/CSV, extract structured data via Prompture
- [x] Model discovery — auto-detect available providers/models, expose in UI

### 8.3 Tukuy Skills UI ✅
- [x] `c.skill(fn)` — Wrap a Tukuy `@skill` into an interactive component
- [x] Skill browser — discovery widget showing all registered skills with search
- [x] Chain visual builder — drag-and-drop Tukuy Chain/Branch/Parallel composition
- [x] Replace Phase 6 JS handlers with Tukuy JS transformers (broader coverage, zero-dep)
- [x] Safety policy UI — configure allowed imports, network, filesystem per session

### 8.4 Agent Components ✅
- [x] `c.agent()` — Wrap Prompture Agent with ReAct loop visualization
- [x] Multi-agent UIs — debate view, router dashboard, sequential pipeline monitor
- [x] Tool call timeline — visual trace of agent reasoning steps and tool invocations
- [x] Budget gauge — real-time cost/token usage widget with threshold alerts

---

## Phase 9: Sharing & Deployment

> **Goal:** Go from `cacao run` to "anyone can use this" in one command.

### 9.1 One-Command Sharing ✅
- [x] review CachiBot QR sharing implementation for inspiration for windows support as is a bit more mature maybe we can leverage some of that code or ideas from it or maybe is over complicating it and we can do something simpler
- [x] `cacao share` — Expose local app via tunnel (like Gradio's share=True)
- [x] Generate shareable URL with optional password protection
- [x] Auto-expire after configurable time (default 72h)
- [x] QR code for mobile access

### 9.2 Deployment Targets ✅
- [x] `cacao deploy` — Deploy to cloud with guided setup
- [x] Hugging Face Spaces support (Dockerfile + app.py template)
- [x] Docker export — `cacao docker app.py` generates Dockerfile
- [x] Railway / Render / Fly.io one-click templates
- [x] GitHub Pages (already works via `cacao build`)

### 9.3 App Gallery ✅
- [x] Public app registry / gallery for discovering Cacao apps
- [x] `cacao publish` — Publish app to gallery
- [x] Embed support — `<iframe>` snippet for embedding in docs/blogs

---

## Phase 10: Developer Experience & Polish

> **Goal:** Make the 0-to-working-app experience flawless.

### 10.1 Error Experience ✅
- [x] Friendly error messages with suggestions (not raw tracebacks)
- [x] Component-level error boundaries with visual indicators
- [x] "Did you mean?" for typos in component names/props
- [x] Server-side errors rendered in browser overlay (dev mode)

### 10.2 DevTools
- [ ] Browser DevTools panel — Signal inspector, event log, session viewer
- [ ] `cacao --debug` mode with verbose WebSocket logging
- [ ] Component tree visualizer
- [ ] Performance profiler (signal update timings, render counts)

### 10.3 Testing
- [ ] `c.test()` — Test runner for Cacao apps
- [ ] Mock session/signals for unit testing event handlers
- [ ] Snapshot testing for UI definitions
- [ ] `cacao test app.py` CLI command

### 10.4 Documentation
- [ ] Interactive API reference (self-hosted Cacao app)
- [ ] Component playground — Edit props live, see result
- [ ] Cookbook with 20+ recipes (auth flow, CRUD app, dashboard, chat, etc.)
- [ ] Video tutorials / getting started guide

---

## Phase 11: Ecosystem & Integrations

> **Goal:** Play well with the Python data stack, don't be an island.

### 11.1 Data Ecosystem
- [ ] Native pandas DataFrame support (auto-detect and render)
- [ ] Polars DataFrame support
- [ ] Plotly figure rendering (pass plotly fig, render natively)
- [ ] Matplotlib figure rendering (auto-convert to image/SVG)
- [ ] SQL query component with connection management

### 11.2 Notebook Integration
- [ ] `c.display()` for rendering Cacao components in Jupyter
- [ ] Notebook-to-app export (`cacao convert notebook.ipynb`)
- [ ] Marimo-style reactive mode in notebooks

### 11.3 Extension System
- [ ] Custom component SDK — Build React components, use from Python
- [ ] `cacao install <extension>` — Install community components
- [ ] Theme marketplace
- [ ] Handler plugins for static builds

---

## Phase 12: Production Hardening

> **Goal:** Make Cacao trustworthy for real deployments.

### 12.1 Performance
- [ ] Component-level lazy loading
- [ ] Virtual scrolling for large datasets (improve existing VirtualList)
- [ ] Signal batching optimization (coalesce rapid updates)
- [ ] WebSocket compression
- [ ] CDN-ready asset fingerprinting

### 12.2 Security
- [ ] CSRF protection
- [ ] Input sanitization framework
- [ ] OAuth2 / OIDC provider support
- [ ] Role-based access control (RBAC)
- [ ] Audit logging

### 12.3 Reliability
- [ ] Configurable WebSocket reconnection strategy
- [ ] Session persistence across server restarts
- [ ] Health check endpoint
- [ ] Graceful shutdown with session draining
- [ ] Background task queue (not blocking the event loop)

### 12.4 Observability
- [ ] Structured logging with correlation IDs
- [ ] Prometheus metrics export
- [ ] OpenTelemetry tracing
- [ ] Signal update rate monitoring

---

## Release Strategy

| Version | Milestone | Key Feature |
|---------|-----------|-------------|
| **0.1.0** | Current | Fluent API + static builds + 67 components |
| **0.2.0** | Phase 7 | Function wrapping (`c.interface()`) |
| **0.3.0** | Phase 8 | AI-powered apps (Prompture + Tukuy integration) |
| **0.4.0** | Phase 9 | Sharing & deployment (`cacao share`, HF Spaces) |
| **0.5.0** | Phase 10 | DevTools, testing, documentation |
| **0.6.0** | Phase 11 | Ecosystem integrations (pandas, plotly, jupyter) |
| **1.0.0** | Phase 12 | Production-ready with security, performance, reliability |

---

## The Pitch (Post-Roadmap)

```python
# Gradio: demo a function
import gradio as gr
gr.Interface(fn=classify, inputs="image", outputs="label").launch()

# Cacao: demo a function AND build the real app around it
import cacao as c

c.config(title="Image Classifier", theme="dark")

with c.sidebar():
    c.text("Model Settings")
    model = c.select("Model", ["ResNet50", "ViT", "CLIP"])

with c.row():
    with c.col(span=6):
        c.interface(classify, inputs="image", outputs="label")
    with c.col(span=6):
        c.metric("Accuracy", "94.2%", trend="+1.2%")
        c.line(history, x="date", y="accuracy")

# Same function wrapping. Real app layout. Real state. Real deployment.
```

**Cacao isn't a demo tool that wishes it was an app framework. It's an app framework that makes demos trivial.**
