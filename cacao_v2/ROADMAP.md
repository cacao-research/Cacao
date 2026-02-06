# Cacao v2 Development Roadmap

## Current State (Phase 2 In Progress)

### Server (Python) ✅ Complete
- [x] `Signal` - Reactive state with session scoping
- [x] `Computed` - Derived state from signals
- [x] `Session` - Per-client session management
- [x] `SessionManager` - Session lifecycle
- [x] `EventRegistry` - Event handling with auto-binding
- [x] `App` - Main class with decorators (@app.on, @app.route)
- [x] WebSocket server (Starlette + Uvicorn) - **Port 1634**
- [x] State sync protocol (init, update, batch)

### Client (React + TypeScript) ✅ Core Complete
- [x] `CacaoProvider` - Context provider with WebSocket
- [x] `useSignal` - Subscribe to signal values
- [x] `useEvent` - Dispatch events to server
- [x] `useConnectionStatus` - Connection state
- [x] `useSessionId` - Session identifier
- [x] `useSignalInput` - Form input binding
- [x] `useSignalSelect` - Select binding
- [x] `useSignalCheckbox` - Checkbox binding
- [x] `useSignalSwitch` - Switch binding
- [x] `useSignalForm` - Multi-field form binding
- [x] WebSocket client with auto-reconnect
- [x] State store with subscriptions

---

## Phase 2: Component Library Foundation ✅ Complete

### 2.1 Layout Components (React) ✅
- [x] `Box` - Flexible container with spacing/flex props
- [x] `Stack` / `HStack` / `VStack` - Vertical/horizontal stack with gap
- [x] `Grid` / `GridItem` - CSS Grid wrapper
- [x] `Container` - Max-width centered container
- [x] `Divider` - Horizontal/vertical divider

### 2.2 Basic UI Components (React) ✅
- [x] `Button` - Primary, secondary, danger, success, warning, ghost, outline variants
- [x] `Text` - Typography component (h1-h6, body, small, caption, code)
- [x] `Badge` - Status indicators with dot option
- [x] `Card` / `CardSection` - Content container with header/footer
- [x] `Alert` - Info, success, warning, error messages

### 2.3 Form Components (React + Python bindings) ✅
- [x] `Input` - Text input with validation states
- [x] `Textarea` - Multi-line text with resize options
- [x] `Select` - Dropdown selection with options
- [x] `Checkbox` - Boolean toggle with label/description
- [x] `Switch` - Toggle switch

### Examples
- [x] Counter - Basic increment/decrement
- [x] Todo - Form binding, list management (created)

---

## Phase 3: Data Components ✅ Complete

### 3.1 Data Display
- [x] `Table` - Data table with sorting, pagination, selection
- [x] `List` - Vertical list with items
- [x] `Descriptions` - Key-value pairs display
- [x] `Tree` - Hierarchical data display
- [x] `Avatar` / `AvatarGroup` - User profile images
- [x] `Tag` / `TagGroup` - Labels and categories

### 3.2 Data Visualization
- [ ] `Plot` - Chart integration (Chart.js or similar)
- [x] `Progress` - Progress bars (line and circle)
- [x] `Statistic` / `StatisticGroup` - Number display with label/trend

---

## Phase 4: Navigation ✅ Complete

- [x] `Navbar` / `NavbarSection` / `NavbarItem` - Top navigation bar
- [x] `Sidebar` / `SidebarGroup` / `SidebarItem` - Collapsible side navigation
- [x] `Menu` / `MenuItem` / `MenuDivider` / `MenuLabel` - Vertical/horizontal menu
- [x] `Tabs` / `Tab` - Tab navigation (line, card, pill variants)
- [x] `Breadcrumb` - Navigation trail with max items

---

## Phase 5: Advanced Features ✅ Complete

### 5.1 Server Enhancements
- [x] `Effect` / `Watch` - Side effects on signal changes
- [x] `Batch` / `batch()` - Batch multiple signal updates
- [x] `Persist` / `PersistManager` - Persist signals to storage (Memory, File)
- [x] `MiddlewareChain` - Middleware system for events
- [x] `rate_limit_middleware` - Rate limiting
- [x] `auth_middleware` - Authentication middleware
- [x] `validation_middleware` - Input validation
- [x] `timeout_middleware` - Request timeout

### 5.2 Client Enhancements
- [x] `useComputed` - Client-side computed values
- [x] `useLocalStorage` - Persist to localStorage
- [x] `useDebounce` / `useDebouncedCallback` - Debounced values/callbacks
- [x] `useThrottle` - Throttled values
- [x] `useSignalDebounced` - Debounced signal updates
- [x] `ErrorBoundary` / `ConnectionError` - Error boundaries
- [x] `Spinner` / `DotsLoader` / `Skeleton` / `LoadingOverlay` - Loading states
- [x] `EmptyState` - Empty state placeholder
- [x] `usePrevious` / `useUpdateEffect` / `useTimeout` / `useInterval` - Utility hooks

### 5.3 Developer Experience
- [ ] CLI tool (`cacao create`, `cacao dev`)
- [ ] TypeScript codegen from Python signals
- [ ] Hot reload for both Python and React
- [ ] DevTools extension

---

## Phase 6: Fluent UI Builder (Streamlit Killer) ✅ In Progress

### 6.1 Python Fluent API
- [x] `ui.App` - Application container with page routing
- [x] `ui.row()`, `ui.col()`, `ui.grid()` - Layout context managers
- [x] `ui.card()`, `ui.sidebar()`, `ui.tabs()` - Container components
- [x] `ui.title()`, `ui.text()`, `ui.code()` - Typography
- [x] `ui.metric()`, `ui.table()`, `ui.progress()` - Data display
- [x] `ui.button()`, `ui.input_field()`, `ui.select()` - Form elements
- [x] `ui.checkbox()`, `ui.switch()`, `ui.slider()` - Form controls
- [x] `ui.badge()`, `ui.alert()` - Feedback components

### 6.2 Chart Components
- [x] `chart.line()` - Line charts
- [x] `chart.bar()` - Bar charts
- [x] `chart.pie()` / `chart.donut()` - Pie/donut charts
- [x] `chart.scatter()` - Scatter plots
- [x] `chart.area()` - Area charts
- [x] `chart.gauge()` - Gauge/radial charts
- [x] `chart.heatmap()` - Heatmaps
- [x] `chart.funnel()` - Funnel charts
- [x] `chart.radar()` - Radar/spider charts
- [x] `chart.treemap()` - Treemaps

### 6.3 Data Utilities
- [x] `data.DataFrame` - Lightweight DataFrame
- [x] `data.load_csv()` - CSV loading
- [x] `data.load_json()` - JSON loading
- [x] `data.load_parquet()` - Parquet loading
- [x] `data.sample_sales_data()` - Demo data generators
- [x] DataFrame methods: filter, select, sort, group_by, aggregate

### 6.4 Examples
- [x] Dashboard example with charts and metrics

### 6.5 TODO: React Chart Components
- [ ] LineChart React component
- [ ] BarChart React component
- [ ] PieChart React component
- [ ] ScatterChart React component
- [ ] Integration with Recharts or Chart.js

---

## Phase 7: Port cacao_tools

- [ ] Encoders tool
- [ ] Converters tool
- [ ] Crypto tools
- [ ] Generators tool
- [ ] Text tools

---

## Strategic Goal: Streamlit Killer

See `STREAMLIT_KILLER_STUDY.md` for full analysis.

### Key Differentiators
1. **10x faster** - Signal-based reactivity vs full re-runs
2. **Professional UI** - Modern component library out of the box
3. **Multi-user ready** - Session-scoped state from day one
4. **Python simplicity** - Streamlit-like API with context managers
5. **React escape hatch** - Full React ecosystem when needed

### Target API (Achieved)
```python
from cacao.ui import App, row, card, metric
from cacao.chart import line, pie
from cacao.data import load_csv

app = App(title="Dashboard")

with app.page("/"):
    with row():
        metric("Revenue", "$45K", trend="+20%")
        metric("Users", "2.3K", trend="+15%")

    with card("Trends"):
        line(load_csv("sales.csv"), x="date", y="revenue")

app.run()
```

---

## Architecture Decisions

### Component Philosophy
Unlike v1 which rendered components server-side as JSON, v2 uses:
- **React components** for all UI rendering
- **Python signals** only for state management
- **Events** for all client-to-server communication

### Why This Approach?
1. **Leverage React ecosystem** - Use existing React component libraries
2. **Better DX** - TypeScript types, React DevTools
3. **Simpler mental model** - State in Python, UI in React
4. **Performance** - React handles efficient DOM updates

### Signal-Component Binding Pattern
```python
# Python - Define state
name = Signal("", name="name")
app.bind("name:input", name)  # Auto-update on input events
```

```tsx
// React - Bind to state (simple)
const nameProps = useSignalInput('name', '')
<Input {...nameProps} />

// React - Bind to state (manual)
const name = useSignal('name', '')
const updateName = useEvent('name:input')
<Input value={name} onChange={e => updateName({ value: e.target.value })} />
```

---

## File Organization

```
cacao_v2/
├── server/                    # Python package
│   ├── signal.py              # ✓ Signal, Computed
│   ├── session.py             # ✓ Session management
│   ├── events.py              # ✓ Event system
│   ├── app.py                 # ✓ App class
│   ├── server.py              # ✓ WebSocket server (port 1634)
│   ├── effects.py             # TODO: Side effects
│   └── middleware.py          # TODO: Event middleware
│
├── client/
│   └── src/
│       ├── cacao/             # Core library
│       │   ├── hooks.tsx      # ✓ React hooks
│       │   ├── useForm.ts     # ✓ Form binding hooks
│       │   ├── store.ts       # ✓ State store
│       │   ├── websocket.ts   # ✓ WS client
│       │   └── types.ts       # ✓ TypeScript types
│       │
│       └── components/        # Component library
│           ├── layout/        # ✓ Box, Stack, Grid, Container, Divider
│           ├── ui/            # ✓ Button, Text, Badge, Card, Alert
│           ├── forms/         # ✓ Input, Textarea, Select, Checkbox, Switch
│           ├── data/          # TODO: Table, List
│           └── navigation/    # TODO: Navbar, Tabs
│
└── examples/
    ├── counter/               # ✓ Basic counter
    ├── todo/                  # ✓ Todo list with forms
    └── dashboard/             # TODO: Full dashboard
```

---

## Next Steps (Immediate)

1. **Test Todo example** - Verify form binding works end-to-end
2. **Create Table component** - Most requested data component
3. **Create Navbar component** - Navigation foundation
4. **Create Tabs component** - Common navigation pattern
5. **Build Dashboard example** - Showcase all components
