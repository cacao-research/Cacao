# Cacao UI/UX — Final Action Plan
## Compiled by Viktor Solis from 10 specialist reports

All paths are relative to `cacao/frontend/src/styles/`. Absolute root: `/mnt/c/Users/Juan/documents/github/cacao/cacao/frontend/src/styles/`.

---

### Top 10 Quick Wins (< 30 min each)

#### 1. Fix hardcoded focus ring in form.less

**File:** `components/form.less` lines 39 and 88

The `.c-input:focus` and `.c-textarea:focus` rules use a hardcoded indigo rgba instead of the theme variable.

```less
// BEFORE (line 39)
box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);

// AFTER
box-shadow: 0 0 0 3px var(--accent-glow);
```

Same fix at line 88 (`.c-textarea:focus`):
```less
// BEFORE (line 88)
box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);

// AFTER
box-shadow: 0 0 0 3px var(--accent-glow);
```

#### 2. Fix hardcoded active nav background in admin.less

**File:** `components/admin.less` line 129

The `.nav-item.active` rule uses hardcoded indigo rgba.

```less
// BEFORE (line 129)
background: rgba(99, 102, 241, 0.1);

// AFTER
background: var(--accent-glow);
```

#### 3. Add missing Light theme status colors

**File:** `themes/light.less`

The light theme only defines bg/text/border/accent. It inherits dark theme status colors from `:root`, which are mismatched for a light background.

```less
// BEFORE — full file:
[data-theme="light"] {
  --bg-primary: #faf6f1;
  --bg-secondary: #f5ebe0;
  --bg-tertiary: #ede0d4;
  --bg-card: #ffffff;
  --bg-card-hover: #fdfbf8;
  --text-primary: #3d2c1e;
  --text-secondary: #6b5344;
  --text-muted: #9c8675;
  --border-color: rgba(109, 83, 68, 0.2);
  --border-subtle: rgba(109, 83, 68, 0.1);
  --accent-primary: #8b5a3c;
  --accent-secondary: #a0674a;
  --accent-glow: rgba(139, 90, 60, 0.15);
  --primary: #8b5a3c;
}

// AFTER — add status colors + gradients + charts:
[data-theme="light"] {
  --bg-primary: #faf6f1;
  --bg-secondary: #f5ebe0;
  --bg-tertiary: #ede0d4;
  --bg-card: #ffffff;
  --bg-card-hover: #fdfbf8;
  --text-primary: #3d2c1e;
  --text-secondary: #6b5344;
  --text-muted: #9c8675;
  --border-color: rgba(109, 83, 68, 0.2);
  --border-subtle: rgba(109, 83, 68, 0.1);
  --accent-primary: #8b5a3c;
  --accent-secondary: #a0674a;
  --accent-glow: rgba(139, 90, 60, 0.15);
  --primary: #8b5a3c;

  // Status colors (tuned for light backgrounds)
  --success: #2d8a4e;
  --success-bg: rgba(45, 138, 78, 0.15);
  --warning: #c4820a;
  --warning-bg: rgba(196, 130, 10, 0.15);
  --danger: #c53030;
  --danger-bg: rgba(197, 48, 48, 0.15);
  --info: #2b6cb0;
  --info-bg: rgba(43, 108, 176, 0.15);

  // Gradients
  --gradient-start: #8b5a3c;
  --gradient-end: #a0674a;

  // Chart colors
  --chart-1: #8b5a3c;
  --chart-2: #2d8a4e;
  --chart-3: #2b6cb0;
  --chart-4: #c4820a;
  --chart-5: #c53030;
  --chart-6: #6b5344;
}
```

#### 4. Fix hardcoded badge backgrounds in display.less

**File:** `components/display.less` lines 94-117

Badge colors use hardcoded rgba that don't respond to theme changes.

```less
// BEFORE (lines 94-117)
.c-badge-primary {
  background: rgba(99, 102, 241, 0.15);
  color: var(--primary);
}
.c-badge-success {
  background: rgba(34, 197, 94, 0.15);
  color: var(--success);
}
.c-badge-warning {
  background: rgba(234, 179, 8, 0.15);
  color: var(--warning);
}
.c-badge-danger {
  background: rgba(239, 68, 68, 0.15);
  color: var(--danger);
}
.c-badge-info {
  background: rgba(14, 165, 233, 0.15);
  color: var(--info);
}

// AFTER
.c-badge-primary {
  background: var(--accent-glow);
  color: var(--primary);
}
.c-badge-success {
  background: var(--success-bg);
  color: var(--success);
}
.c-badge-warning {
  background: var(--warning-bg);
  color: var(--warning);
}
.c-badge-danger {
  background: var(--danger-bg);
  color: var(--danger);
}
.c-badge-info {
  background: var(--info-bg);
  color: var(--info);
}
```

#### 5. Add table row hover transition

**File:** `components/table.less` line 26

Row hover snaps instantly. Add a transition.

```less
// BEFORE (line 26-28)
tbody tr:hover {
  background: var(--bg-card-hover);
}

// AFTER
tbody tr {
  transition: background @transition-fast;
}
tbody tr:hover {
  background: var(--bg-card-hover);
}
```

(Requires `@transition-fast` from Quick Win #9. If doing this first, use `0.15s ease` inline.)

#### 6. Add global focus-visible style and selection color

**File:** `base.less` — append after line 39

```less
// Global focus ring for keyboard navigation
:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

// Theme-aware text selection
::selection {
  background: var(--accent-primary);
  color: var(--bg-primary);
}
```

#### 7. Standardize card padding with token

**File:** `components/card.less` line 7

```less
// BEFORE (line 7)
padding: 1.25rem;

// AFTER
padding: @space-4;
```

This gives consistent 16px. For a roomier card, use `@space-6` (24px).

#### 8. Fix button padding with tokens

**File:** `components/button.less` line 4

```less
// BEFORE (line 4)
padding: 0.625rem 1.25rem;

// AFTER
padding: @space-2 @space-4;
```

Result: 8px top/bottom, 16px left/right.

#### 9. Add transition variables

**File:** `variables.less` — append after line 26

```less
// Transitions
@transition-fast: 0.15s ease;
@transition-base: 0.2s ease;
@transition-slow: 0.3s ease;
```

Then replace hardcoded transitions across the codebase. Key files:
- `components/button.less` line 10: `transition: all @transition-fast;`
- `components/card.less` line 8: `transition: border-color @transition-base;`
- `components/form.less` line 26: `transition: border-color @transition-fast;`
- `components/tabs.less` line 17: `transition: all @transition-fast;`
- `components/admin.less` line 79 (nav-group-chevron): `transition: transform @transition-base;`
- `components/admin.less` line 117 (nav-item): `transition: all @transition-fast;`

#### 10. Fix form input padding with tokens

**File:** `components/form.less` line 20, 65, 112, 235

All form controls use `padding: 0.625rem 0.875rem`. Replace with tokens.

```less
// BEFORE (lines 20, 65, 112, 235)
padding: 0.625rem 0.875rem;

// AFTER
padding: @space-2 @space-3;
```

Result: 8px top/bottom, 12px left/right. Apply to:
- `.c-input` (line 20)
- `.c-textarea` (line 65)
- `.select` (line 112)
- `.c-datepicker` (line 235)

Also update the `.form-control()` mixin in `mixins.less` line 24:
```less
// BEFORE
padding: 0.625rem 0.875rem;

// AFTER
padding: @space-2 @space-3;
```

#### 11. Add scrollbar styling

**File:** `base.less` — append after the focus-visible rules

```less
// Themed scrollbar
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}
::-webkit-scrollbar-thumb {
  background: var(--accent-primary);
  border-radius: 4px;

  &:hover {
    background: var(--accent-secondary);
  }
}
```

---

### Design Tokens

Create **`variables.less`** additions (append to existing file). These tokens already partially exist; this fills the gaps.

**File:** `variables.less` — full target state:

```less
// Cacao Design Tokens
// Core theme variables - DO NOT add component styles here

// Spacing scale (4px base)
@space-1: 4px;
@space-2: 8px;
@space-3: 12px;
@space-4: 16px;
@space-6: 24px;
@space-8: 32px;

// Border radius
@radius-xs: 2px;
@radius-sm: 8px;    // was 6px — round up for soft craft feel
@radius-md: 12px;   // was 8px — brand direction: soft craftsmanship
@radius-lg: 16px;   // was 12px
@radius-full: 50%;

// Typography
@font-family: 'Inter', system-ui, -apple-system, sans-serif;
@font-mono: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
@font-size-xs: 0.7rem;      // 11px
@font-size-sm: 0.75rem;     // 12px
@font-size-base: 0.875rem;  // 14px
@font-size-lg: 1rem;        // 16px
@font-size-xl: 1.125rem;    // 18px
@font-size-2xl: 1.5rem;     // 24px
@font-size-3xl: 1.75rem;    // 28px
@font-size-4xl: 2rem;       // 32px
@font-weight-normal: 400;
@font-weight-medium: 500;
@font-weight-semibold: 600;
@font-weight-bold: 700;

// Transitions
@transition-fast: 0.15s ease;
@transition-base: 0.2s ease;
@transition-slow: 0.3s ease;

// Shadows (use in component upgrades)
@shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
@shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.06);
@shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
@shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.1);
@shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.12);

// Sidebar
@sidebar-width: 260px;
@sidebar-collapsed: 64px;

// Breakpoints (reference only — used in @media queries)
@breakpoint-sm: 480px;
@breakpoint-md: 768px;
@breakpoint-lg: 1024px;
@breakpoint-xl: 1280px;
```

Note: Radius values are intentionally bumped per the Brand Direction. This is a breaking visual change. Existing `@radius-sm: 6px` becomes `8px`, `@radius-md: 8px` becomes `12px`, `@radius-lg: 12px` becomes `16px`. Every component using these tokens inherits the new values automatically.

#### CSS Custom Properties for runtime theming

**Dark theme** (`themes/dark.less`) — add to `:root`:
```less
// Already present: bg, text, border, accent, status, gradient, chart vars.
// No changes needed — dark theme is complete.
```

**Light theme** (`themes/light.less`) — see Quick Win #3 above.

**Tukuy theme** (`themes/tukuy.less`) — already complete with all status/gradient/chart vars.

---

### Component Upgrades

#### Cards — `components/card.less`

Replace the entire file:

```less
// Card component

.card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: @radius-lg;
  padding: @space-4;
  box-shadow: @shadow-xs;
  transition: border-color @transition-base, box-shadow @transition-base, background @transition-base;

  &:hover {
    border-color: var(--accent-primary);
    box-shadow: @shadow-md;
    background: var(--bg-card-hover);
  }
}

.card-title {
  font-size: 0.8rem;
  font-weight: @font-weight-semibold;
  color: var(--text-secondary);
  margin-bottom: @space-4;
  padding-bottom: @space-3;
  border-bottom: 1px solid var(--border-subtle);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

@media (max-width: @breakpoint-md) {
  .card {
    padding: @space-3;
  }
}
```

#### Buttons — `components/button.less`

Replace the entire file:

```less
// Button component

.btn {
  padding: @space-2 @space-4;
  border-radius: @radius-md;
  font-weight: @font-weight-medium;
  font-size: @font-size-base;
  cursor: pointer;
  border: none;
  transition: all @transition-fast;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: @space-2;
  min-height: 36px;

  &:active {
    transform: scale(0.98);
  }

  &:focus-visible {
    outline: 2px solid var(--accent-primary);
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  &-primary {
    background: var(--accent-primary);
    color: var(--bg-primary);
    font-weight: @font-weight-semibold;

    &:hover { background: var(--accent-secondary); }
  }

  &-secondary {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: 1px solid var(--border-color);

    &:hover { background: var(--bg-card-hover); }
  }

  &-ghost {
    background: transparent;
    color: var(--text-secondary);

    &:hover { background: var(--bg-tertiary); }
  }

  &-loading {
    pointer-events: none;
    opacity: 0.7;
  }
}

@media (max-width: @breakpoint-md) {
  .btn {
    min-height: 44px;  // touch target
  }
}
```

#### Inputs — `components/form.less`

Key changes (apply to `.c-input`, `.c-textarea`, `.select`, `.c-datepicker`):

```less
// Replace :focus block on .c-input (lines 36-40)
&:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

// Add error state after :disabled block (after line 45)
&.error {
  border-color: var(--danger);
  &:focus {
    box-shadow: 0 0 0 3px var(--danger-bg);
  }
}
```

Same pattern for `.c-textarea` (lines 85-89) and `.c-datepicker`.

Add to `.c-switch` (after line 200):
```less
&:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
```

Add to `.checkbox` (after line 141):
```less
&:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
```

Increase touch targets on mobile — add at end of `form.less`:
```less
@media (max-width: @breakpoint-md) {
  .c-input, .c-textarea, .select, .c-datepicker {
    padding: @space-3 @space-3;
    min-height: 44px;
  }
  .checkbox {
    width: 22px;
    height: 22px;
  }
  .c-switch {
    width: 48px;
    height: 28px;
  }
}
```

#### Tables — `components/table.less`

Replace the entire file:

```less
// Table component

.table-container { overflow-x: auto; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: @font-size-base;
}

th, td {
  padding: @space-3 @space-4;
  text-align: left;
  border-bottom: 1px solid var(--border-subtle);
}

th {
  font-weight: @font-weight-semibold;
  color: var(--text-muted);
  text-transform: uppercase;
  font-size: @font-size-xs;
  letter-spacing: 0.04em;
  background: var(--bg-tertiary);
  position: sticky;
  top: 0;
  z-index: 1;
}

tbody tr {
  transition: background @transition-fast;
}

tbody tr:hover {
  background: var(--bg-card-hover);
}

// Mobile: card view
@media (max-width: @breakpoint-md) {
  table, thead, tbody, th, td, tr {
    display: block;
  }
  thead {
    display: none;
  }
  tbody tr {
    margin-bottom: @space-3;
    border: 1px solid var(--border-color);
    border-radius: @radius-md;
    padding: @space-2;
    background: var(--bg-card);
  }
  td {
    padding: @space-2 @space-3;
    border-bottom: 1px solid var(--border-subtle);
    text-align: right;

    &::before {
      content: attr(data-label);
      float: left;
      font-weight: @font-weight-semibold;
      color: var(--text-muted);
      text-transform: uppercase;
      font-size: @font-size-xs;
    }

    &:last-child {
      border-bottom: none;
    }
  }
}
```

Note: The mobile card view requires the JS Table component to render `data-label` attributes on `<td>` elements. That change goes in `frontend/src/components/display/Table.js`.

#### Tabs — `components/tabs.less`

Replace the entire file:

```less
// Tabs component

.tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: @space-4;
}

.tab {
  padding: @space-2 @space-4;
  font-size: @font-size-base;
  color: var(--text-muted);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all @transition-fast;
  font-weight: @font-weight-medium;
  background: none;
  border-top: none;
  border-left: none;
  border-right: none;

  &:hover { color: var(--text-primary); }

  &:focus-visible {
    outline: 2px solid var(--accent-primary);
    outline-offset: -2px;
  }

  &.active {
    color: var(--accent-primary);
    border-bottom-color: var(--accent-primary);
  }
}

.tab-content {
  animation: fadeIn @transition-fast;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

#### Nav Groups — `components/admin.less`

Add height animation for expand/collapse. Replace `.nav-group-items` (line 101-103):

```less
// BEFORE
.nav-group-items {
  padding: @space-1 0;
}

// AFTER
.nav-group-items {
  padding: @space-1 0;
  max-height: 500px;
  overflow: hidden;
  transition: max-height @transition-slow, opacity @transition-base;
  opacity: 1;
}

.nav-group:not(.open) .nav-group-items {
  max-height: 0;
  opacity: 0;
  padding: 0;
}
```

#### Alerts — `components/alert.less`

Replace the entire file:

```less
// Alert component

.alert {
  padding: @space-3 @space-4;
  border-radius: @radius-md;
  display: flex;
  align-items: center;
  gap: @space-3;
  margin-bottom: @space-3;
  font-size: @font-size-base;
  animation: alertIn @transition-base;
  position: relative;

  &-info { background: var(--info-bg); border: 1px solid var(--info); color: var(--info); }
  &-success { background: var(--success-bg); border: 1px solid var(--success); color: var(--success); }
  &-warning { background: var(--warning-bg); border: 1px solid var(--warning); color: var(--warning); }
  &-error { background: var(--danger-bg); border: 1px solid var(--danger); color: var(--danger); }
}

.alert-close {
  position: absolute;
  top: @space-2;
  right: @space-3;
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.6;
  font-size: @font-size-lg;
  padding: @space-1;

  &:hover { opacity: 1; }
}

@keyframes alertIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}
```

Note: Close button requires JS component change in `frontend/src/components/display/Alert.js`.

#### Progress — `components/progress.less`

Add shimmer animation. Append after line 24:

```less
.progress-fill.indeterminate {
  width: 30% !important;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
```

#### Code blocks — `components/typography.less`

Add copy button positioning. Modify `.c-code` (lines 30-49):

```less
.c-code {
  font-family: @font-mono;
  font-size: @font-size-sm;
  line-height: 1.6;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: @radius-md;
  padding: @space-4;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--text-primary);
  margin: 0;
  position: relative;

  code {
    font-family: inherit;
    background: none;
    padding: 0;
  }
}

.c-code-copy {
  position: absolute;
  top: @space-2;
  right: @space-2;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: @radius-sm;
  color: var(--text-muted);
  padding: @space-1 @space-2;
  font-size: @font-size-xs;
  cursor: pointer;
  opacity: 0;
  transition: opacity @transition-fast;

  .c-code:hover & {
    opacity: 1;
  }

  &:hover {
    color: var(--text-primary);
    background: var(--bg-tertiary);
  }
}
```

Note: Copy button requires JS component change in `frontend/src/components/typography/Code.js`.

---

### Features to Add

#### P0 — Must-have

**1. Command Palette (Cmd+K)**

New files:
- `frontend/src/components/core/CommandPalette.js` — React component
- `styles/components/command-palette.less` — Styles

Style spec:
```less
// components/command-palette.less

.cmd-palette-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  padding-top: 20vh;
  animation: fadeIn @transition-fast;
}

.cmd-palette {
  width: 560px;
  max-height: 400px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: @radius-lg;
  box-shadow: @shadow-xl;
  overflow: hidden;
}

.cmd-palette-input {
  width: 100%;
  padding: @space-4;
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: @font-size-lg;

  &:focus { outline: none; }
  &::placeholder { color: var(--text-muted); }
}

.cmd-palette-results {
  overflow-y: auto;
  max-height: 320px;
}

.cmd-palette-item {
  padding: @space-3 @space-4;
  display: flex;
  align-items: center;
  gap: @space-3;
  cursor: pointer;
  color: var(--text-secondary);
  transition: background @transition-fast;

  &:hover, &.active {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }
}

.cmd-palette-shortcut {
  margin-left: auto;
  font-size: @font-size-xs;
  color: var(--text-muted);
  padding: 2px @space-2;
  background: var(--bg-tertiary);
  border-radius: @radius-xs;
}
```

Add import to `index.less`:
```less
@import "components/command-palette.less";
```

JS implementation: Listen for `Cmd+K` / `Ctrl+K`, render overlay, fuzzy-match against registered commands.

**2. Toast Notification System**

New files:
- `frontend/src/components/core/Toast.js`
- `styles/components/toast.less`

Style spec:
```less
// components/toast.less

.toast-container {
  position: fixed;
  top: @space-4;
  right: @space-4;
  z-index: 1100;
  display: flex;
  flex-direction: column;
  gap: @space-2;
  pointer-events: none;
}

.toast {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: @radius-md;
  padding: @space-3 @space-4;
  box-shadow: @shadow-lg;
  display: flex;
  align-items: center;
  gap: @space-3;
  min-width: 280px;
  max-width: 420px;
  pointer-events: auto;
  animation: toastIn @transition-base;

  &.exiting {
    animation: toastOut @transition-fast forwards;
  }
}

.toast-success { border-left: 3px solid var(--success); }
.toast-error { border-left: 3px solid var(--danger); }
.toast-warning { border-left: 3px solid var(--warning); }
.toast-info { border-left: 3px solid var(--info); }

.toast-close {
  margin-left: auto;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: @space-1;
  &:hover { color: var(--text-primary); }
}

@keyframes toastIn {
  from { opacity: 0; transform: translateX(100%); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes toastOut {
  from { opacity: 1; transform: translateX(0); }
  to { opacity: 0; transform: translateX(100%); }
}
```

**3. Copy-to-clipboard on code blocks**

Add to Code.js component (see Code blocks upgrade above for CSS). JS logic:

```js
// In frontend/src/components/typography/Code.js
// Add a button element inside the code wrapper:
//   <button class="c-code-copy" onclick="copyCode(this)">Copy</button>
// Handler:
function copyCode(btn) {
  const code = btn.parentElement.querySelector('code') || btn.parentElement;
  navigator.clipboard.writeText(code.textContent);
  btn.textContent = 'Copied!';
  setTimeout(() => btn.textContent = 'Copy', 1500);
}
```

**4. Mobile hamburger menu button**

**File:** `components/admin.less` — add before the `@media` block (before line 171):

```less
.app-shell-hamburger {
  display: none;
  position: fixed;
  top: @space-3;
  left: @space-3;
  z-index: 101;
  width: 44px;
  height: 44px;
  border-radius: @radius-md;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: @font-size-xl;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  box-shadow: @shadow-sm;
}

.app-shell-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

@media (max-width: @breakpoint-md) {
  .app-shell-hamburger {
    display: flex;
  }
  .app-shell-backdrop.open {
    display: block;
  }
}
```

Update the existing `@media (max-width: 768px)` block in admin.less to use the `@breakpoint-md` variable.

JS: In `frontend/src/components/layout/AppShell.js`, render hamburger button + backdrop, toggle `.open` class on `.app-shell-nav`.

**5. Keyboard shortcut system**

**File:** `frontend/src/components/core/shortcuts.js` (new)

```js
// Keyboard shortcut registry
const shortcuts = {};

export function registerShortcut(combo, handler, description) {
  shortcuts[combo] = { handler, description };
}

export function initShortcuts() {
  document.addEventListener('keydown', (e) => {
    const combo = [];
    if (e.metaKey || e.ctrlKey) combo.push('mod');
    if (e.shiftKey) combo.push('shift');
    if (e.altKey) combo.push('alt');
    combo.push(e.key.toLowerCase());
    const key = combo.join('+');
    if (shortcuts[key]) {
      e.preventDefault();
      shortcuts[key].handler();
    }
  });
}

export function getShortcuts() {
  return Object.entries(shortcuts).map(([combo, { description }]) => ({
    combo, description
  }));
}
```

#### P1 — Should-have

**1. Theme toggle with localStorage**

JS component: `frontend/src/components/core/ThemeToggle.js`

```js
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('cacao-theme', theme);
}

function initTheme() {
  const saved = localStorage.getItem('cacao-theme');
  if (saved) setTheme(saved);
}
```

**2. Loading skeleton shimmer**

**File:** `base.less` — append:

```less
.skeleton {
  background: var(--bg-tertiary);
  border-radius: @radius-md;
  position: relative;
  overflow: hidden;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
      90deg,
      transparent,
      var(--accent-glow),
      transparent
    );
    animation: skeletonShimmer 1.5s ease-in-out infinite;
  }
}

@keyframes skeletonShimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
```

**3. Accordion / Collapsible component**

Style spec — new file `styles/components/accordion.less`:

```less
.c-accordion {
  border: 1px solid var(--border-color);
  border-radius: @radius-md;
  overflow: hidden;
}

.c-accordion-item {
  border-bottom: 1px solid var(--border-subtle);
  &:last-child { border-bottom: none; }
}

.c-accordion-header {
  width: 100%;
  padding: @space-3 @space-4;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: @font-size-base;
  font-weight: @font-weight-medium;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background @transition-fast;

  &:hover { background: var(--bg-tertiary); }
}

.c-accordion-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height @transition-slow;
  padding: 0 @space-4;
}

.c-accordion-item.open .c-accordion-body {
  max-height: 500px;
  padding: @space-3 @space-4;
}
```

#### P2 — Nice-to-have

**1. Tooltip component** — CSS-only approach in `styles/components/tooltip.less`:

```less
[data-tooltip] {
  position: relative;

  &::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: calc(100% + @space-2);
    left: 50%;
    transform: translateX(-50%);
    padding: @space-1 @space-2;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: @radius-sm;
    font-size: @font-size-xs;
    color: var(--text-primary);
    white-space: nowrap;
    box-shadow: @shadow-md;
    opacity: 0;
    pointer-events: none;
    transition: opacity @transition-fast;
  }

  &:hover::after {
    opacity: 1;
  }
}
```

**2. prefers-reduced-motion** — add to `base.less`:

```less
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**3. Print media queries** — add to `base.less`:

```less
@media print {
  .app-shell-nav,
  .app-shell-hamburger,
  .toast-container,
  .cmd-palette-overlay {
    display: none !important;
  }
  .app-shell-content {
    width: 100% !important;
  }
  .card {
    box-shadow: none;
    border: 1px solid #ddd;
    break-inside: avoid;
  }
}
```

---

### Mobile Fixes

All changes target `@breakpoint-md: 768px` unless noted.

#### 1. Hamburger menu + mobile drawer

See Features > P0 > #4 above. Full implementation in `admin.less` and `AppShell.js`.

#### 2. Touch targets — 44px minimum

**File:** `components/button.less` — already handled in Component Upgrades section:
```less
@media (max-width: @breakpoint-md) {
  .btn { min-height: 44px; }
}
```

**File:** `components/form.less` — already handled in Component Upgrades section:
```less
@media (max-width: @breakpoint-md) {
  .c-input, .c-textarea, .select, .c-datepicker {
    padding: @space-3 @space-3;
    min-height: 44px;
  }
}
```

**File:** `components/tabs.less` — add:
```less
@media (max-width: @breakpoint-md) {
  .tab {
    padding: @space-3 @space-4;
    min-height: 44px;
  }
}
```

#### 3. Responsive typography

**File:** `components/typography.less` — replace the existing `@media` block (line 51-53):

```less
@media (max-width: @breakpoint-md) {
  .title-1 { font-size: @font-size-3xl; }
  .title-2 { font-size: 1.25rem; }
  .title-3 { font-size: @font-size-lg; }
}
```

#### 4. Table mobile card view

See Component Upgrades > Tables above. Requires JS change to add `data-label` on `<td>`.

#### 5. Reduce chart height at phone breakpoint

**File:** `components/charts.less` — append:

```less
@media (max-width: @breakpoint-sm) {
  .chart-container {
    height: 180px;
  }
}
```

#### 6. Add 480px breakpoint

Already defined in tokens as `@breakpoint-sm: 480px;`. Used above for chart height.

#### 7. Reduce card padding on mobile

See Component Upgrades > Cards above. Already handled with:
```less
@media (max-width: @breakpoint-md) {
  .card { padding: @space-3; }
}
```

#### 8. prefers-reduced-motion

See Features > P2 > #2 above. One rule in `base.less` kills all animations/transitions globally.

---

### Brand Direction

**THE ONE THING: "Cacao Accent Glow"**

Every interactive element gets the warm accent glow. This is Cacao's signature.

Implementation touchpoints:
| Element | File | Property |
|---------|------|----------|
| Input focus | `form.less` | `box-shadow: 0 0 0 3px var(--accent-glow)` |
| Button focus | `button.less` | `outline: 2px solid var(--accent-primary)` |
| Card hover | `card.less` | `box-shadow: @shadow-md` + `border-color: var(--accent-primary)` |
| Nav active | `admin.less` | `background: var(--accent-glow)` |
| Tab active | `tabs.less` | `border-bottom-color: var(--accent-primary)` |
| Badge primary | `display.less` | `background: var(--accent-glow)` |
| Scrollbar thumb | `base.less` | `background: var(--accent-primary)` |
| Text selection | `base.less` | `background: var(--accent-primary)` |

**Border-radius: Soft Craftsmanship**

Updated in `variables.less`:
- `@radius-xs: 2px` — pills within components
- `@radius-sm: 8px` — badges, small elements (was 6px)
- `@radius-md: 12px` — buttons, inputs, alerts (was 8px)
- `@radius-lg: 16px` — cards, modals (was 12px)
- `@radius-full: 50%` — avatars, round indicators

**Shadow elevation system**

Defined in tokens. Usage map:
- `@shadow-xs` — default cards, inputs
- `@shadow-sm` — hamburger button, dropdowns
- `@shadow-md` — card hover, active elements
- `@shadow-lg` — toasts, popovers
- `@shadow-xl` — command palette, modals

**Color: Brighten caramel accent in dark mode**

**File:** `themes/dark.less` line 21 — optional accent brighten:

```less
// Current
--accent-primary: #d4a574;

// Proposed (warmer, more vibrant)
--accent-primary: #e8b86a;
// If changed, also update:
--accent-glow: rgba(232, 184, 106, 0.2);
--gradient-start: #e8b86a;
--primary: #e8b86a;
--chart-1: #e8b86a;
```

This is a judgment call. Test both and pick. The `#e8b86a` is more golden, `#d4a574` is more caramel. Either works.

---

### Implementation Order

#### Phase 1 — Foundation (Day 1)

| # | Task | File(s) | Time |
|---|------|---------|------|
| 1 | Add transition variables | `variables.less` | 5 min |
| 2 | Add shadow variables | `variables.less` | 5 min |
| 3 | Update border-radius values | `variables.less` | 5 min |
| 4 | Add font-weight, @font-mono variables | `variables.less` | 5 min |
| 5 | Add breakpoint variables | `variables.less` | 5 min |
| 6 | Fix hardcoded focus ring | `form.less` L39, L88 | 5 min |
| 7 | Fix hardcoded nav active bg | `admin.less` L129 | 2 min |
| 8 | Add light theme status colors | `light.less` | 10 min |
| 9 | Fix hardcoded badge colors | `display.less` L94-117 | 5 min |
| 10 | Add table hover transition | `table.less` L26 | 2 min |
| 11 | Add focus-visible + selection | `base.less` | 5 min |
| 12 | Standardize card padding | `card.less` L7 | 2 min |
| 13 | Fix button padding | `button.less` L4 | 2 min |
| 14 | Fix form input padding | `form.less` L20,65,112,235 + `mixins.less` L24 | 5 min |
| 15 | Add scrollbar styling | `base.less` | 5 min |
| 16 | Build and verify | `npm run build` in `frontend/` | 5 min |

**Day 1 total: ~70 min**

#### Phase 2 — Brand Polish (Day 2)

| # | Task | File(s) | Time |
|---|------|---------|------|
| 1 | (Optional) Brighten dark mode accent | `dark.less` | 10 min |
| 2 | Add box-shadow to cards | `card.less` | 10 min |
| 3 | Update mixins.less .form-control() | `mixins.less` | 5 min |
| 4 | Replace hardcoded transitions with tokens | All component LESS files | 20 min |
| 5 | Add prefers-reduced-motion | `base.less` | 5 min |
| 6 | Add skeleton shimmer animation | `base.less` | 10 min |
| 7 | Build and visual QA all themes | `npm run build`, check dark/light/tukuy | 20 min |

**Day 2 total: ~80 min**

#### Phase 3 — Component Upgrades (Days 3-4)

| # | Task | File(s) | Time |
|---|------|---------|------|
| 1 | Button upgrade (active, focus, disabled, loading) | `button.less` | 30 min |
| 2 | Input error states + focus ring | `form.less` | 30 min |
| 3 | Switch/checkbox focus rings | `form.less` | 15 min |
| 4 | Table sticky header | `table.less` | 10 min |
| 5 | Table mobile card view (CSS) | `table.less` | 20 min |
| 6 | Table mobile card view (JS: data-label) | `components/display/Table.js` | 30 min |
| 7 | Tabs keyboard nav + focus ring | `tabs.less` + `components/form/Tabs.js` | 30 min |
| 8 | Nav group expand/collapse animation | `admin.less` | 15 min |
| 9 | Alert close button + animation (CSS) | `alert.less` | 15 min |
| 10 | Alert close button (JS) | `components/display/Alert.js` | 20 min |
| 11 | Progress shimmer / indeterminate | `progress.less` | 10 min |
| 12 | Code block copy button (CSS + JS) | `typography.less` + `components/typography/Code.js` | 30 min |
| 13 | Build and test all components | Full QA | 30 min |

**Days 3-4 total: ~285 min (~4.75 hours)**

#### Phase 4 — Mobile (Day 5)

| # | Task | File(s) | Time |
|---|------|---------|------|
| 1 | Hamburger button (CSS) | `admin.less` | 15 min |
| 2 | Hamburger button (JS) | `components/layout/AppShell.js` | 30 min |
| 3 | Backdrop overlay | `admin.less` | 10 min |
| 4 | Touch targets (buttons, inputs, tabs) | `button.less`, `form.less`, `tabs.less` | 20 min |
| 5 | Responsive typography | `typography.less` | 10 min |
| 6 | Chart height at 480px | `charts.less` | 5 min |
| 7 | Mobile QA on 375px, 768px, 1024px viewports | Browser DevTools | 30 min |

**Day 5 total: ~120 min (2 hours)**

#### Phase 5 — Features (Days 6-7)

| # | Task | File(s) | Time |
|---|------|---------|------|
| 1 | Command palette CSS | `styles/components/command-palette.less` | 20 min |
| 2 | Command palette JS | `components/core/CommandPalette.js` | 90 min |
| 3 | Toast system CSS | `styles/components/toast.less` | 20 min |
| 4 | Toast system JS | `components/core/Toast.js` | 60 min |
| 5 | Keyboard shortcut registry | `components/core/shortcuts.js` | 30 min |
| 6 | Wire Cmd+K to command palette | `shortcuts.js` + `CommandPalette.js` | 15 min |
| 7 | Theme toggle with localStorage | `components/core/ThemeToggle.js` | 30 min |
| 8 | Wire toast to Python server events | `server/ui.py` + `components/core/websocket.js` | 30 min |
| 9 | Integration test | Full app test | 30 min |

**Days 6-7 total: ~325 min (~5.4 hours)**

#### Phase 6 — Accessibility (Day 8)

| # | Task | File(s) | Time |
|---|------|---------|------|
| 1 | Add ARIA roles to nav items | `components/layout/NavItem.js`, `NavGroup.js` | 20 min |
| 2 | Tab keyboard arrow navigation | `components/form/Tabs.js` | 30 min |
| 3 | Alert ARIA role="alert" | `components/display/Alert.js` | 5 min |
| 4 | Modal/palette focus trap | `CommandPalette.js` | 20 min |
| 5 | Ensure all interactive elements have focus-visible | Global audit | 30 min |
| 6 | Print media queries | `base.less` | 10 min |
| 7 | Final QA: keyboard-only navigation test | Manual test | 30 min |

**Day 8 total: ~145 min (~2.4 hours)**

---

**Total estimated effort: 8 working days (~17 hours of focused work)**

Files touched (LESS — existing):
- `variables.less`
- `base.less`
- `mixins.less`
- `themes/light.less`
- `themes/dark.less` (optional accent change)
- `components/card.less`
- `components/button.less`
- `components/form.less`
- `components/table.less`
- `components/tabs.less`
- `components/alert.less`
- `components/progress.less`
- `components/display.less`
- `components/admin.less`
- `components/typography.less`
- `components/charts.less`
- `index.less` (add new imports)

Files created (LESS — new):
- `components/command-palette.less`
- `components/toast.less`
- `components/accordion.less`
- `components/tooltip.less`

Files touched (JS — existing):
- `components/display/Table.js` (data-label for mobile)
- `components/display/Alert.js` (close button)
- `components/typography/Code.js` (copy button)
- `components/form/Tabs.js` (keyboard nav)
- `components/layout/AppShell.js` (hamburger menu)

Files created (JS — new):
- `components/core/CommandPalette.js`
- `components/core/Toast.js`
- `components/core/shortcuts.js`
- `components/core/ThemeToggle.js`
