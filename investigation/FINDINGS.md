# Cacao UI/UX Investigation Report

**Date:** 2026-02-17
**Framework:** Cacao - Reactive Web Framework for Python
**Scope:** Complete UI/UX audit across spatial design, color, motion, typography, iconography, interaction, dashboard architecture, mobile/responsive, brand identity, and developer experience.

---

## Table of Contents

1. [Marco - Spatial Design & Layout](#1-marco---spatial-design--layout)
2. [Luna - Color System & Theming](#2-luna---color-system--theming)
3. [Kai - Motion & Animation](#3-kai---motion--animation)
4. [Sana - Typography & Readability](#4-sana---typography--readability)
5. [Tomas - Iconography & Visual Assets](#5-tomas---iconography--visual-assets)
6. [Priya - Interaction Design & Accessibility](#6-priya---interaction-design--accessibility)
7. [Diego - Dashboard Architecture & Information Design](#7-diego---dashboard-architecture--information-design)
8. [Mei - Mobile & Responsive Design](#8-mei---mobile--responsive-design)
9. [Ren - Brand Identity & Visual Personality](#9-ren---brand-identity--visual-personality)
10. [Zara - Developer Experience & Component Inventory](#10-zara---developer-experience--component-inventory)

---

## 1. Marco - Spatial Design & Layout

### Overview

Marco evaluated the spatial system across both the legacy frontend (LESS/JS) and the modern client (TypeScript/CSS). The framework defines a 4px base spacing scale but fails to use it consistently across components.

### Spacing Scale Definition

**File:** `cacao/frontend/src/styles/variables.less`

The framework defines an 8-step spacing scale based on a 4px unit:

| Variable     | Value | Pixels |
|-------------|-------|--------|
| `@space-1`  | 4px   | 4      |
| `@space-2`  | 8px   | 8      |
| `@space-3`  | 12px  | 12     |
| `@space-4`  | 16px  | 16     |
| `@space-5`  | 20px  | 20     |
| `@space-6`  | 24px  | 24     |
| `@space-7`  | 28px  | 28     |
| `@space-8`  | 32px  | 32     |

### Consistency Audit by Area

| Area | Score | Notes |
|------|-------|-------|
| Admin layout (`admin.less`) | 9/10 | Uses LESS variables throughout, most consistent area |
| Client TypeScript components | 9/10 | Clean 4px multiplication system, disciplined |
| Layouts (`layouts.less`) | 5/10 | Hardcoded REM values instead of LESS spacing variables |
| Form elements (`form.less`) | 4/10 | Inconsistent values: 14px, 10px, 6px oddities |

### Specific Issues

**Card padding is off-scale:**
- **File:** `cacao/frontend/src/styles/components/card.less`
- Card uses `padding: 1.25rem` which is 20px. This matches `@space-5` numerically, but is expressed in REM rather than using the variable. More importantly, it falls between the more natural rhythm points of 16px (`@space-4`) and 24px (`@space-6`).

**Button padding is off-scale:**
- **File:** `cacao/frontend/src/styles/components/button.less`
- Button uses `padding: 0.625rem 1.25rem` which resolves to 10px vertical / 20px horizontal. The 10px vertical padding does not fall on the 4px scale (nearest values: 8px or 12px).

**Column spans have inconsistent gap offsets:**
- **File:** `cacao/frontend/src/styles/layouts.less`
- Column gap calculations reference values of 8px, 10px, and 12px. The 10px value is off the 4px scale.

**Sidebar has no collapsed state:**
- **File:** `cacao/frontend/src/styles/components/admin.less`
- Sidebar width is hardcoded at 260px with no collapsed/minimized state defined. No CSS class or variable exists for a narrow sidebar mode.

### Container Sizes

Container breakpoints follow Tailwind conventions:

| Size | Width  |
|------|--------|
| `sm` | 640px  |
| `md` | 768px  |
| `lg` | 1024px |
| `xl` | 1280px |

### Overall Spatial Consistency Score: 6.8 / 10

### Recommendations

1. Replace all hardcoded REM padding/margin values with LESS spacing variables (`@space-*`).
2. Align button vertical padding to `@space-2` (8px) or `@space-3` (12px).
3. Align card padding to `@space-4` (16px) or `@space-6` (24px).
4. Normalize column gap offsets to values on the 4px scale.
5. Define a collapsed sidebar state (e.g., 64px icon-only mode).

---

## 2. Luna - Color System & Theming

### Overview

Luna audited the three-theme color system (Dark, Light, Tukuy) and found an excellent CSS custom properties foundation undermined by hardcoded color values scattered across component styles.

### Theme Architecture

All three themes use CSS custom properties, enabling runtime switching via the `data-theme` attribute. This is an excellent architectural decision.

| Theme  | Identity   | Primary Accent |
|--------|-----------|----------------|
| Dark   | Chocolate  | Warm brown/caramel tones |
| Light  | Cream      | Warm light palette |
| Tukuy  | Blue       | Technical blue palette |

**Files:**
- `cacao/frontend/src/styles/themes/dark.less`
- `cacao/frontend/src/styles/themes/light.less`
- `cacao/frontend/src/styles/themes/tukuy.less`

### Surface Hierarchy

The surface system is well-defined across themes:

```
bg-primary --> bg-secondary --> bg-tertiary --> bg-card
```

This four-level depth provides sufficient layering for complex layouts.

### CRITICAL: Light Theme Missing Status Colors

**File:** `cacao/frontend/src/styles/themes/light.less`

The light theme is MISSING all status color definitions:
- `--color-success` (green)
- `--color-warning` (yellow/amber)
- `--color-danger` (red)
- `--color-info` (blue)

This means any component using status colors (Alert, Badge, Progress) will fall back to inherited or undefined values in light mode. This is a **P0 bug**.

### Hardcoded Color Values (Theme-Breaking)

Three locations use hardcoded `rgba(99, 102, 241, ...)` (Indigo) which bypasses the theme system entirely:

1. **Badge backgrounds** in `cacao/frontend/src/styles/components/display.less`:
   - `rgba(99, 102, 241, 0.15)` -- Indigo at 15% opacity
   - Does not respond to theme changes

2. **Focus ring shadow** in `cacao/frontend/src/styles/components/form.less`:
   - `rgba(99, 102, 241, 0.1)` -- Indigo at 10% opacity
   - Visually disconnected from all three theme palettes

3. **Active nav background** in `cacao/frontend/src/styles/components/admin.less`:
   - `rgba(99, 102, 241, 0.1)` -- Indigo at 10% opacity
   - Should use accent color from active theme

### Contrast Ratios

All themes achieve **AAA** rating for primary text contrast. This is excellent and should be maintained.

### Tukuy Blue Palette

| Role       | Hex       |
|-----------|-----------|
| Primary    | `#3b82f6` |
| Secondary  | `#60a5fa` |
| Deep       | `#1d4ed8` |

### Chart Colors

Each theme defines a 6-color chart palette with good distribution across the hue wheel.

### Client Boilerplate Contamination

**File:** `cacao/client/src/index.css`

Contains Vite scaffold boilerplate colors including `#646cff` (a purple/indigo) that do not match any Cacao theme. These should be removed or replaced with framework-appropriate values.

### Recommendations

1. **P0:** Add all status colors to `light.less` (success, warning, danger, info).
2. **P0:** Replace all hardcoded `rgba(99, 102, 241, ...)` with theme-aware CSS custom properties.
3. **P1:** Remove or replace Vite boilerplate colors in `cacao/client/src/index.css`.
4. **P2:** Consider defining a `--color-focus-ring` custom property per theme.

---

## 3. Kai - Motion & Animation

### Overview

Kai audited all transitions and animations across the codebase. The framework has a functional but minimal motion system -- transitions exist but are uniform, predictable, and lack personality. There are zero `@keyframes` animations in the entire codebase.

### Existing Transition Inventory

| Component        | Duration | Easing | File |
|-----------------|----------|--------|------|
| Buttons          | 150ms    | ease   | `button.less` |
| Inputs           | 150ms    | ease   | `form.less` |
| Cards            | 200ms    | ease   | `card.less` |
| Switches         | 200ms    | ease   | `form.less` |
| Progress bars    | 300ms    | ease   | `progress.less` |
| Nav items        | 150ms    | ease   | `admin.less` |
| Mobile sidebar   | 300ms    | ease   | `admin.less` |
| Nav group chevron| 200ms    | ease   | `admin.less` |

**All transitions in `cacao/frontend/src/styles/components/`**

### Timing Pattern

The timing follows a reasonable three-tier pattern:
- **Fast (150ms):** Micro-interactions (buttons, inputs, nav items)
- **Medium (200ms):** Component-level (cards, switches, chevrons)
- **Slow (300ms):** Layout-level (progress, sidebar slide)

### Problems

**Uniform easing -- no variety:**
Every transition uses `ease`. Best practice calls for:
- `ease-out` for entrances (element arriving)
- `ease-in` for exits (element leaving)
- `ease-in-out` for state changes (element transforming in place)

**Client outlier:**
- **File:** `cacao/client/src/index.css`
- Button transition uses 250ms, inconsistent with the 150ms used in the legacy frontend.

**Nav group content appears/disappears instantly:**
- **File:** `cacao/frontend/src/components/layout/NavGroup.js`
- The chevron icon rotates with a 200ms transition, but the expandable content below it shows/hides with no transition at all. This creates a jarring disconnect.

### Zero @keyframes Animations

There are no `@keyframes` definitions anywhere in the codebase. This means:
- No loading spinners (CSS-based)
- No shimmer/skeleton effects
- No entrance animations
- No pulse/heartbeat indicators
- No toast slide-in/out

### Missing Motion Patterns

| Pattern | Impact | Priority |
|---------|--------|----------|
| Page/route transitions | High -- navigation feels instant/jumpy | P1 |
| Accordion expand/collapse | Medium -- nav groups snap open | P1 |
| Dropdown open/close | Medium -- menus appear instantly | P1 |
| Loading shimmer | High -- no skeleton loading state | P1 |
| Toast entrance/exit | High -- no notification animation | P1 |
| Card hover elevation (shadow lift) | Low -- subtle polish | P2 |
| Button hover scale | Low -- micro-feedback | P2 |
| Gauge needle animation | Medium -- gauge appears static | P2 |
| Form validation shake | Low -- error feedback | P2 |
| Table row hover transition | Low -- data browsing feedback | P2 |

### Positive Notes

- No animation libraries are imported. The CSS-first approach is appropriate for a framework that values bundle size.
- The existing timing tiers (150/200/300ms) are reasonable and should be formalized as LESS variables.

### Recommendations

1. Define LESS variables for transition durations: `@duration-fast`, `@duration-normal`, `@duration-slow`.
2. Define LESS variables for easing curves: `@ease-in`, `@ease-out`, `@ease-in-out`.
3. Add `@keyframes` for: `spin` (loading), `shimmer` (skeleton), `fade-in`, `slide-up`, `slide-down`.
4. Add `max-height` or `grid-template-rows` transition to nav group content.
5. Add `prefers-reduced-motion` media query support (see Mei's findings).

---

## 4. Sana - Typography & Readability

### Overview

Sana audited the typographic system across both frontend stacks. The framework has a comprehensive type scale but applies it inconsistently, and the two stacks (legacy JS and modern TypeScript) define conflicting systems.

### Font Families

**Primary font:** Inter (loaded from Google Fonts CDN) with `system-ui` fallback.

**Code font stack:** Monaco, Menlo, Ubuntu Mono, Consolas, monospace.
- **Notable absence:** JetBrains Mono, which has become the standard developer font for code display.

### Type Scale (Legacy Frontend)

**File:** `cacao/frontend/src/styles/variables.less`

| Variable           | Value     | Approx px |
|-------------------|-----------|-----------|
| `@font-size-xs`    | 0.7rem    | 11px      |
| `@font-size-sm`    | 0.75rem   | 12px      |
| `@font-size-base`  | 0.875rem  | 14px      |
| `@font-size-lg`    | 1rem      | 16px      |
| `@font-size-xl`    | 1.125rem  | 18px      |
| `@font-size-2xl`   | 1.5rem    | 24px      |
| `@font-size-3xl`   | 1.75rem   | 28px      |
| `@font-size-4xl`   | 2rem      | 32px      |

Note: The base size is 14px (`0.875rem`), which is smaller than the modern default of 16px. This is intentional for data-dense dashboard interfaces but worth documenting as a conscious choice.

### Type Scale (Modern Client -- CONFLICTING)

**File:** `cacao/client/src/components/ui/Text.tsx`

The TypeScript client defines its own variant system that does NOT align with the LESS variables:

| Variant   | Size    | Weight | Line Height |
|----------|---------|--------|-------------|
| `h1`      | 2rem    | 700    | 1.2         |
| `h2`      | 1.5rem  | 700    | 1.3         |
| `h3`      | 1.25rem | 600    | 1.3         |
| `body`    | 1rem    | 400    | 1.6         |
| `small`   | 0.875rem| --     | --          |
| `caption` | 0.75rem | --     | 0.7 opacity |

The `h3` value of `1.25rem` (20px) does not appear in the LESS scale at all. The `body` variant uses `1rem` (16px) which maps to `@font-size-lg` in the LESS system -- a confusing name collision.

### Off-Scale Values

**Metric component:**
- **File:** `cacao/frontend/src/styles/components/metric.less`
- Metric values use `1.75rem` (28px) which maps to `@font-size-3xl`. On mobile, this scales down to `1.5rem` (24px).

### Specialized Typography Patterns

**Table headers:**
- Transform: `uppercase`
- Size: `@font-size-xs`
- Letter spacing: `0.04em`
- Weight: 600
- **File:** `cacao/frontend/src/styles/components/table.less`

**Labels:**
- Transform: `uppercase`
- Size: `@font-size-sm`
- Letter spacing: `0.03em` to `0.05em` (inconsistent range)
- Weight: 500

**Code blocks:**
- Size: `@font-size-sm`
- Line height: 1.6
- Background: `bg-tertiary`
- **File:** `cacao/frontend/src/components/typography/Code.js`
- No syntax highlighting whatsoever -- plain text only.

### Responsive Typography

**Only Title 1 has responsive scaling:**
- Desktop: `2rem` (32px)
- Below 768px: `1.75rem` (28px)

Titles 2 through 4, body text, and all other typography remain at fixed sizes regardless of viewport. This means text that looks good on desktop may be too large or too small on mobile.

### Missing Features

1. **Tabular figures:** No `font-variant-numeric: tabular-nums` configuration for data display. This means numbers in tables and metrics may not align vertically.
2. **Syntax highlighting:** Code blocks render as plain monospace text.
3. **Responsive scaling for Title 2-4:** Only Title 1 adapts to viewport.

### Recommendations

1. Reconcile the LESS and TypeScript type scales into a single source of truth.
2. Add `font-variant-numeric: tabular-nums` to metric, table, and statistic components.
3. Add JetBrains Mono to the code font stack.
4. Add responsive scaling for Title 2, 3, and 4.
5. Normalize label letter-spacing to a single value (recommend `0.04em`).
6. Consider integrating a syntax highlighting library (e.g., Prism.js) for code blocks.

---

## 5. Tomas - Iconography & Visual Assets

### Overview

Tomas audited the icon system defined in the framework. Cacao uses inline SVGs with a consistent stroke-based style, but the icon set is minimal and lacks critical icons for common UI patterns.

### Icon Implementation

**File:** `cacao/frontend/src/components/core/icons.js`

Icons are defined as SVG elements in an `iconMap` lookup object. Components reference icons by name string, and the renderer returns the corresponding SVG element.

### Icon Style Consistency

All 18 icons share identical attributes -- this is excellent consistency:

| Attribute      | Value           |
|---------------|-----------------|
| `viewBox`      | `0 0 24 24`    |
| `stroke`       | `currentColor` |
| `strokeWidth`  | `2`            |
| `fill`         | `none`         |
| Rendered size  | 16x16 px       |

The use of `currentColor` for stroke means all icons correctly inherit their parent's text color. This is the right approach.

### Current Icon Set (18 icons)

```
home, box, database, globe, code, file-text, image, cloud,
message-square, layers, folder, wrench, cog, chevron-down,
chevron-right, hash, check, x
```

### Icon Sizing

All icons render at a fixed 16x16 pixel size. There are no size variants. A mature icon system should support at least three sizes:

| Size | Use Case |
|------|----------|
| 16px | Inline with text, nav items, badges |
| 20px | Buttons, form elements |
| 24px | Headers, empty states, feature highlights |

### Missing Critical Icons

The following icons are needed for common UI patterns but are not defined:

**Navigation & Actions:**
`search`, `plus`, `minus`, `arrow-left`, `arrow-right`, `arrow-up`, `arrow-down`, `menu` (hamburger), `refresh`, `external-link`

**Data Operations:**
`copy`, `clipboard`, `download`, `upload`, `filter`, `sort`, `edit`, `trash`, `link`

**Visibility & State:**
`eye`, `eye-off`, `lock`, `unlock`, `bell`, `star`, `heart`

**Status & Feedback:**
`warning` / `alert-triangle`, `info` / `info-circle`, `error` / `x-circle`, `check-circle`

**Time & Identity:**
`calendar`, `clock`, `user`, `users`, `settings`

### Icon + Label Spacing

**File:** `cacao/frontend/src/styles/components/admin.less`

Navigation items use `gap: @space-2` (8px) between icon and label. This is appropriate for 16px icons with standard text sizes.

### No Icon Component Wrapper

Icons are injected as raw SVG elements via the `iconMap` lookup. There is no reusable `<Icon>` component that would provide:
- Size variants (sm, md, lg)
- Color overrides
- Accessibility attributes (`aria-hidden`, `role="img"`, `aria-label`)
- Spin/animation states (for loading icons)

### Recommendations

1. Add at minimum 20-25 high-priority missing icons (search, plus, minus, arrows, copy, filter, sort, edit, trash, eye, lock, bell, user, calendar, warning, info).
2. Create an `<Icon>` wrapper component with size prop (`sm`=16, `md`=20, `lg`=24).
3. Add `aria-hidden="true"` to decorative icons and `role="img"` + `aria-label` to semantic icons.
4. Consider adopting Lucide icons (which match the current stroke style) for a complete set.

---

## 6. Priya - Interaction Design & Accessibility

### Overview

Priya conducted an accessibility and interaction audit across all 28 components. The results reveal **critical gaps** in keyboard navigation, focus management, ARIA labeling, and interaction states. The framework currently fails to meet WCAG AA compliance by a significant margin.

### Interaction State Coverage

| State | Components with Support | Total Components | Coverage |
|-------|------------------------|-----------------|----------|
| Hover feedback | 18 | 28 | 64% -- acceptable |
| Disabled state | 22 | 28 | 79% -- good but inconsistent |
| Focus ring (visible) | 2 | 28 | **7% -- CRITICAL** |
| Active state (`:active`) | 2 | 28 | **7% -- CRITICAL** |
| Loading state | 2 | 28 | **7% -- CRITICAL** |
| Keyboard support | 0 | 28 | **0% -- CRITICAL** |
| ARIA labels | 1 | 28 | **4% -- CRITICAL** |

### Focus Ring Issues

**File:** `cacao/frontend/src/styles/components/form.less`

The focus ring uses a hardcoded Indigo shadow:
```css
box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
```

This value:
- Does not reference any theme variable
- Uses Indigo, which is disconnected from all three theme palettes (Dark=chocolate, Light=cream, Tukuy=blue)
- Has very low opacity (0.1), making it nearly invisible on most backgrounds
- Is only applied to 2 of 28 components

### Disabled State Inconsistencies

While 22 components define a disabled visual state, implementation varies:
- Some set `opacity: 0.5` without `pointer-events: none`, meaning disabled elements can still receive clicks.
- Some set `pointer-events: none` without visual dimming, meaning elements appear enabled but are not.

### Keyboard Navigation -- Zero Support

No component implements keyboard event handlers:
- **Checkbox / Switch:** Uses a hidden `<input>` approach that prevents keyboard navigation. The visual element is a styled `<div>` that only responds to click.
- **Tabs:** No arrow key navigation between tabs.
- **Menu / Dropdown:** No Escape key to close, no arrow keys to navigate items.
- **Modal / Dialog:** No focus trapping.

### TypeScript vs JavaScript Component Gap

| Feature | TypeScript Client | Legacy JS Frontend |
|---------|------------------|-------------------|
| Button loading spinner | Yes (`cacao/client/src/components/ui/Button.tsx`) | No |
| Table sorting | Yes (`cacao/client/src/components/data/Table.tsx`) | No |
| Table pagination | Yes | No |
| Table row selection | Yes | No |

The TypeScript client is significantly more feature-complete for interaction states, but both stacks share the same accessibility gaps.

### Missing Interaction Patterns

| Pattern | Status | Impact |
|---------|--------|--------|
| Command palette (Cmd+K) | Not implemented | High -- standard for dev tools |
| Toast / notification system | Not implemented | High -- no user feedback mechanism |
| Tooltip system | Not implemented | Medium -- no hover information |
| Copy-to-clipboard | Not implemented | High -- expected on code blocks |
| Focus trapping (modals) | Not implemented | High -- accessibility requirement |

### WCAG AA Compliance Estimate: ~40%

The framework passes on color contrast (thanks to Luna's findings on AAA text contrast) but fails on:
- 1.3.1 Info and Relationships (missing ARIA)
- 2.1.1 Keyboard (zero keyboard support)
- 2.4.7 Focus Visible (2 of 28 components)
- 3.2.1 On Focus (no consistent focus behavior)
- 4.1.2 Name, Role, Value (missing ARIA labels)

### Recommendations

1. **P0:** Add visible focus rings to ALL interactive components using a theme-aware CSS custom property.
2. **P0:** Add keyboard event handlers to Checkbox, Switch, Tabs, Menu.
3. **P0:** Add ARIA attributes (`role`, `aria-label`, `aria-expanded`, `aria-selected`, `aria-checked`) to all interactive components.
4. **P1:** Add `pointer-events: none` to ALL disabled states.
5. **P1:** Implement focus trapping for modal/dialog components.
6. **P1:** Build a toast/notification system.
7. **P2:** Add copy-to-clipboard to code blocks and values.
8. **P2:** Implement a command palette (Cmd+K).
9. **P2:** Add tooltip component.

---

## 7. Diego - Dashboard Architecture & Information Design

### Overview

Diego evaluated the existing showcase application (Tukuy plugin ecosystem dashboard) and the overall dashboard architecture patterns. The architecture is clean and scalable, but the information design has significant gaps.

### Current Showcase Architecture

**File:** `tukuy_showcase.py`

The showcase uses:
- `AppShell` with `NavSidebar` + `ShellContent` with `NavPanel` components
- Data model representing the Tukuy plugin ecosystem

### Current Layout Structure

```
AppShell
  +-- NavSidebar (left)
  |     +-- NavGroup (per category)
  |           +-- NavItem (per plugin)
  +-- ShellContent (right)
        +-- NavPanel (per plugin, switched by nav)
              +-- Title + Description
              +-- Row of 3 Metric cards
              +-- Requirements Card
              +-- Transformers Table
              +-- Skills Table
```

### Data Model

The plugin data model is rich and well-structured:

| Field | Type | Description |
|-------|------|-------------|
| `display_name` | string | Human-readable plugin name |
| `description` | string | Plugin description |
| `icon` | string | Icon name from icon set |
| `group` | string | Category grouping |
| `requires` | list | Dependency list |
| `version` | string | Semantic version |
| `transformers` | list | Transformer functions |
| `skills` | list | Skill definitions |

### Overview Page

The current overview page displays:
- **4 metric cards:** Plugins count, Transformers count, Skills count, Groups count
- **Category summary table:** Listing categories with plugin counts

Plugins are organized into **9 categories** in the sidebar navigation.

### Plugin Detail Page

Each plugin detail view shows:
- Title and description
- 3 metric cards (plugin-specific stats)
- Requirements card
- Transformers table
- Skills table

### Missing Information Design Elements

**Overview page gaps:**
- No search or filter functionality
- No category browser grid (card-based visual navigation)
- No additional aggregate metrics:
  - Load success rate
  - Average transformers per plugin
  - Average skills per plugin
  - Most-depended-on plugins
  - Plugins with zero dependencies vs. many

**Detail page gaps:**
- No visual dependency graph
- No "used by" reverse dependency view
- No version history or changelog

### Proposed Wireframes

**Home / Overview:**
```
+--------------------------------------------------+
|  [Search: _______________]  [Filter: Category v]  |
+--------------------------------------------------+
|  +--------+  +--------+  +--------+  +--------+  |
|  |Plugins |  |Transf. |  |Skills  |  |Groups  |  |
|  |  47    |  |  128   |  |  83    |  |   9    |  |
|  +--------+  +--------+  +--------+  +--------+  |
+--------------------------------------------------+
|  Category Cards (grid of 9)                       |
|  +----------+  +----------+  +----------+         |
|  | Text     |  | Format   |  | Crypto   |         |
|  | 8 plugins|  | 6 plugins|  | 4 plugins|         |
|  +----------+  +----------+  +----------+         |
|  +----------+  +----------+  +----------+         |
|  | Network  |  | Data     |  | Auth     |         |
|  | 5 plugins|  | 7 plugins|  | 3 plugins|         |
|  +----------+  +----------+  +----------+         |
+--------------------------------------------------+
```

**Plugin Detail:**
```
+--------------------------------------------------+
|  [<- Back]  Plugin Name              v1.2.3      |
|  Description text here...                         |
+--------------------------------------------------+
|  +--------+  +--------+  +--------+              |
|  |Transf. |  |Skills  |  |Requires|              |
|  |  12    |  |   5    |  |   3    |              |
|  +--------+  +--------+  +--------+              |
+--------------------------------------------------+
|  Requirements          |  Transformers            |
|  - plugin-a            |  Name    | Type | Desc   |
|  - plugin-b            |  func1   | text | ...    |
|  - plugin-c            |  func2   | data | ...    |
+--------------------------------------------------+
|  Skills                                           |
|  Name    | Args  | Description                    |
|  skill1  | 2     | ...                             |
|  skill2  | 1     | ...                             |
+--------------------------------------------------+
```

**Category Browser:**
```
+--------------------------------------------------+
|  Category: Text Processing (8 plugins)            |
+--------------------------------------------------+
|  +-------------------+  +-------------------+     |
|  | plugin-name       |  | plugin-name       |     |
|  | Short description |  | Short description |     |
|  | T:5  S:3  R:2     |  | T:8  S:1  R:0     |     |
|  +-------------------+  +-------------------+     |
|  +-------------------+  +-------------------+     |
|  | plugin-name       |  | plugin-name       |     |
|  | Short description |  | Short description |     |
|  | T:3  S:2  R:1     |  | T:6  S:4  R:3     |     |
|  +-------------------+  +-------------------+     |
+--------------------------------------------------+
```

### Recommendations

1. Add card-based plugin grid for the overview page, replacing or supplementing the table.
2. Implement search-as-you-type across plugin names, descriptions, and transformer/skill names.
3. Add category filter chips or tabs for quick filtering.
4. Add requirement-based filtering ("show plugins with no dependencies").
5. Add aggregate metrics (load success rate, avg transformers/plugin).
6. The existing architecture (AppShell + NavSidebar + NavPanel) is clean and should be preserved.

---

## 8. Mei - Mobile & Responsive Design

### Overview

Mei evaluated the framework's mobile and responsive capabilities. The findings are stark: Cacao is fundamentally a desktop-first framework with minimal responsive support. The overall responsive score is **2 / 10**.

### Breakpoint System

**Current breakpoints (only 2):**

| Breakpoint | Width |
|-----------|-------|
| Tablet    | 768px |
| Desktop   | 1024px|

**Missing breakpoints:**

| Breakpoint | Width | Use Case |
|-----------|-------|----------|
| Small phone | 320px | iPhone SE, older devices |
| Phone | 480px | Standard phones |
| Large desktop | 1440px+ | Widescreen monitors |
| Landscape | orientation query | Rotated tablets/phones |

### CRITICAL: Sidebar Mobile Failure

**Files:**
- `cacao/frontend/src/styles/components/admin.less`
- `cacao/frontend/src/components/layout/NavSidebar.js`

The sidebar hides at 768px via `display: none`, but **no hamburger menu button is rendered** to bring it back. Users on tablets and phones have no way to access navigation. This is a **blocking usability bug** on mobile.

### Touch Target Failures

WCAG 2.5.8 and Apple HIG require minimum 44x44px touch targets. Current sizes:

| Component | Current Size | Required | Pass/Fail |
|-----------|-------------|----------|-----------|
| Buttons   | ~36px height | 44px    | FAIL |
| Checkbox  | 18x18px     | 44px    | FAIL |
| Switch    | ~20px track | 44px    | FAIL |
| Slider track | ~5px    | 44px    | FAIL |
| Nav items | varies      | 44px    | Partial |

### Table Responsiveness

Tables use `overflow-x: auto` (horizontal scroll) as the only mobile strategy. This is functional but insufficient:
- No card/stacked view alternative for narrow screens
- No column prioritization (hiding less-important columns)
- No responsive column labels

### Chart Responsiveness

**File:** `cacao/frontend/src/styles/components/charts.less`

Charts use a fixed height of 280px regardless of viewport. On mobile:
- 280px is too tall, consuming most of the viewport
- No width-responsive resizing
- No alternate compact visualization for small screens

### Typography Scaling

Only `Title 1` has responsive scaling:
- Desktop: `2rem` (32px)
- Below 768px: `1.75rem` (28px)

`Title 2`, `Title 3`, `Title 4`, body text, and all other typographic elements remain at fixed sizes. This means:
- Headings may be too large on phones
- No reading-optimized text sizing on small screens

### Card Padding

Card padding (`1.25rem` / 20px) does not reduce on mobile. On a 320px screen, this means 40px of horizontal padding consumed, leaving only 280px for content.

### Form Mobile Issues

- No increased touch target sizes on mobile
- No stacked label layout for narrow screens
- No mobile-optimized date picker or file upload

### Platform-Level Issues

**Viewport meta tag:** Correctly defined -- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.

**No `prefers-reduced-motion` support:** Users who set this system preference (for vestibular disorders) get full animations regardless.

**No safe area insets:** On phones with notches (iPhone X+) or dynamic islands, content may be hidden behind system UI. Missing:
```css
padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
```

### Overall Responsive Score: 2 / 10

### Recommendations

1. **P0:** Add hamburger menu button that toggles sidebar visibility on mobile.
2. **P0:** Increase all touch targets to minimum 44x44px on mobile (use media query to avoid desktop bloat).
3. **P0:** Add 480px breakpoint for phones.
4. **P1:** Add responsive chart heights (e.g., 200px on mobile, 280px on tablet, 350px on desktop).
5. **P1:** Add card/stacked table view for screens under 768px.
6. **P1:** Add responsive typography scaling for Title 2-4.
7. **P1:** Reduce card padding on mobile (e.g., 12px below 480px).
8. **P2:** Add `prefers-reduced-motion: reduce` media query support.
9. **P2:** Add `env(safe-area-inset-*)` padding for notched devices.
10. **P2:** Add 1440px+ breakpoint for large desktop optimization.

---

## 9. Ren - Brand Identity & Visual Personality

### Overview

Ren evaluated the visual personality and brand coherence of the Cacao framework. The core finding is an **identity crisis**: Cacao has a warm, artisanal name that evokes craft and richness, but its visual presentation is generic, flat, and anonymous. Nothing in the interface says "this is Cacao."

### The Identity Problem

**Name:** "Cacao" evokes warmth, craft, organic richness, artisanal quality.
**Visual reality:** Generic flat UI with no distinguishing characteristics. The dark theme could belong to any dashboard framework.

### What's Missing

| Element | Status | Impact |
|---------|--------|--------|
| Visual signature element | None | Nothing identifies Cacao visually |
| Shadow / elevation system | None | Flat without intention |
| Scrollbar styling | None | Browser default |
| Selection color | None | Browser default |
| Cursor definitions | None | Browser default |
| Texture or warmth | None | Feels cold/clinical |

### Border Radius Analysis

Current values are arbitrary:
- Various components use 6px, 8px, and 12px border-radius
- No documented philosophy or scale
- No relationship between element size and roundedness

**Proposed philosophy -- "Soft Craftsmanship":**

| Element Type | Radius | Rationale |
|-------------|--------|-----------|
| Small elements (badges, tags) | 6px | Subtle softening |
| Medium elements (buttons, inputs) | 8px | Comfortable, approachable |
| Large elements (cards, modals) | 12px | Warm, crafted feel |
| Extra-large (panels, sheets) | 16px | Generous, inviting |

Bigger elements get more rounded -- this creates a sense of warmth that increases with the visual weight of the element.

### Focus Ring Problem

The focus ring uses hardcoded Indigo (`rgba(99, 102, 241, ...)`) which:
- Does not match the Dark theme (chocolate/caramel)
- Does not match the Light theme (cream)
- Does not match the Tukuy theme (blue -- closest but still wrong shade)
- Is completely disconnected from the framework's identity

### Transition Uniformity

All transitions use the same `ease` curve and similar durations. There is no variety that communicates personality. A crafted interface should feel slightly different when:
- Hovering (quick, responsive)
- Opening menus (smooth, confident)
- Transitioning pages (deliberate, grounded)

### THE ONE THING: "Cacao Accent Glow"

If the framework implements one brand-defining visual element, it should be this:

**A warm, organic glow on interactive elements** using an `accent-glow` CSS custom property.

```css
/* Dark theme */
--accent-glow: 0 0 12px rgba(212, 165, 116, 0.3);

/* Light theme */
--accent-glow: 0 0 12px rgba(180, 130, 80, 0.2);

/* Applied on focus/hover of interactive elements */
button:focus-visible {
  box-shadow: var(--accent-glow);
}
```

This would:
- Replace the disconnected Indigo focus ring
- Create a visual signature unique to Cacao
- Reinforce the warm "cacao glow" brand on every interaction
- Be subtle enough for professional use, distinctive enough to remember

### Shadow System (Proposed)

The framework currently has no elevation system. A subtle shadow scale would add depth:

| Variable       | Value | Use Case |
|---------------|-------|----------|
| `@shadow-xs`   | `0 1px 2px rgba(0,0,0,0.05)` | Subtle card lift |
| `@shadow-sm`   | `0 1px 3px rgba(0,0,0,0.1)` | Buttons, badges |
| `@shadow-md`   | `0 4px 6px rgba(0,0,0,0.1)` | Cards, dropdowns |
| `@shadow-lg`   | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |
| `@shadow-xl`   | `0 20px 25px rgba(0,0,0,0.1)` | Full-page overlays |

### Color Adjustment Proposals

**Current accent (caramel):** `#d4a574`
**Proposed brighter caramel:** `#e8b86a` -- more vibrant, better contrast, still warm.

The dark theme's chocolate tones should be deepened slightly to increase contrast with the brighter accent.

### Tukuy Theme Identity Disconnect

The Tukuy theme (`cacao/frontend/src/styles/themes/tukuy.less`) completely abandons Cacao's warm identity for a standard blue tech palette. It feels like a different framework entirely.

**Recommendation:** Tukuy should feel like a "technical sibling" of Cacao -- blue-shifted but still warm. Consider:
- Warmer blues (slate-blue instead of pure blue)
- Retaining the border-radius philosophy
- Keeping the accent glow (blue-tinted instead of caramel)

### The Developer Feeling

When a developer uses Cacao, they should feel:

> "This is craft. This is built with intention."

Currently they feel: "This is a dashboard."

### Recommendations

1. **P0:** Implement the "Cacao Accent Glow" as the framework's visual signature.
2. **P0:** Define and apply the shadow elevation system.
3. **P1:** Formalize the border-radius scale with the "Soft Craftsmanship" philosophy.
4. **P1:** Replace Indigo focus ring with theme-aware accent glow.
5. **P1:** Style scrollbars, text selection color, and cursor states.
6. **P2:** Adjust caramel accent to `#e8b86a` for more vibrancy.
7. **P2:** Make Tukuy theme feel like a sibling (warm blues) rather than a stranger.
8. **P2:** Add subtle texture or gradient to empty states and backgrounds.

---

## 10. Zara - Developer Experience & Component Inventory

### Overview

Zara conducted a complete inventory of both frontend stacks and evaluated the developer experience. The framework has a rich component set but lacks several features that modern developers expect from a dashboard framework.

### Complete Component Inventory

#### Legacy Frontend (JavaScript)

**File root:** `cacao/frontend/src/components/`

**Layout (10 components):**
| Component | File |
|-----------|------|
| Row | `layout/Row.js` |
| Col | `layout/Col.js` |
| Grid | `layout/Grid.js` |
| Sidebar | `layout/Sidebar.js` |
| AppShell | `layout/AppShell.js` |
| NavSidebar | `layout/NavSidebar.js` |
| NavGroup | `layout/NavGroup.js` |
| NavItem | `layout/NavItem.js` |
| NavPanel | `layout/NavPanel.js` |
| ShellContent | `layout/ShellContent.js` |

**Display (8 components):**
| Component | File |
|-----------|------|
| Card | `display/Card.js` |
| Metric | `display/Metric.js` |
| Table | `display/Table.js` |
| Alert | `display/Alert.js` |
| Progress | `display/Progress.js` |
| Gauge | `display/Gauge.js` |
| Badge | `display/Badge.js` |
| JsonView | `display/JsonView.js` |

**Typography (5 components):**
| Component | File |
|-----------|------|
| Title | `typography/Title.js` |
| Text | `typography/Text.js` |
| Code | `typography/Code.js` |
| Divider | `typography/Divider.js` |
| Spacer | `typography/Spacer.js` |

**Form (10 components):**
| Component | File |
|-----------|------|
| Button | `form/Button.js` |
| Input | `form/Input.js` |
| Select | `form/Select.js` |
| Slider | `form/Slider.js` |
| Switch | `form/Switch.js` |
| Checkbox | `form/Checkbox.js` |
| Tabs | `form/Tabs.js` |
| DatePicker | `form/DatePicker.js` |
| FileUpload | `form/FileUpload.js` |
| Textarea | `form/Textarea.js` |

**Charts (10 components):**
| Component | File |
|-----------|------|
| LineChart | `charts/LineChart.js` |
| BarChart | `charts/BarChart.js` |
| PieChart | `charts/PieChart.js` |
| AreaChart | `charts/AreaChart.js` |
| ScatterChart | `charts/ScatterChart.js` |
| RadarChart | `charts/RadarChart.js` |
| GaugeChart | `charts/GaugeChart.js` |
| FunnelChart | `charts/FunnelChart.js` |
| HeatmapChart | `charts/HeatmapChart.js` |
| TreemapChart | `charts/TreemapChart.js` |

**Handlers (5 modules):**
| Module | File | Functions |
|--------|------|-----------|
| Encoders | `handlers/encoders.js` | base64, url, html, jwt |
| Generators | `handlers/generators.js` | uuid, password, lorem |
| Converters | `handlers/converters.js` | yaml, case, number base |
| Text | `handlers/text.js` | stats, regex |
| Crypto | `handlers/crypto.js` | hash, hmac |

**Legacy JS Total: 43 components + 5 handler modules**

---

#### Modern Client (TypeScript)

**File root:** `cacao/client/src/`

**Layout (5 components):**
| Component | File |
|-----------|------|
| Box | `components/layout/Box.tsx` |
| Stack / HStack / VStack | `components/layout/Stack.tsx` |
| Grid / GridItem | `components/layout/Grid.tsx` |
| Container | `components/layout/Container.tsx` |
| Divider | `components/layout/Divider.tsx` |

**UI (5 components):**
| Component | File |
|-----------|------|
| Button | `components/ui/Button.tsx` |
| Card | `components/ui/Card.tsx` |
| Text | `components/ui/Text.tsx` |
| Alert | `components/ui/Alert.tsx` |
| Badge | `components/ui/Badge.tsx` |

**Forms (5 components):**
| Component | File |
|-----------|------|
| Input | `components/forms/Input.tsx` |
| Select | `components/forms/Select.tsx` |
| Textarea | `components/forms/Textarea.tsx` |
| Checkbox | `components/forms/Checkbox.tsx` |
| Switch | `components/forms/Switch.tsx` |

**Navigation (5 components):**
| Component | File |
|-----------|------|
| Tabs | `components/navigation/Tabs.tsx` |
| Breadcrumb | `components/navigation/Breadcrumb.tsx` |
| Menu | `components/navigation/Menu.tsx` |
| Navbar | `components/navigation/Navbar.tsx` |
| Sidebar | `components/navigation/Sidebar.tsx` |

**Data (8 components):**
| Component | File |
|-----------|------|
| Table | `components/data/Table.tsx` |
| List | `components/data/List.tsx` |
| Avatar | `components/data/Avatar.tsx` |
| Descriptions | `components/data/Descriptions.tsx` |
| Progress | `components/data/Progress.tsx` |
| Statistic | `components/data/Statistic.tsx` |
| Tag | `components/data/Tag.tsx` |
| Tree | `components/data/Tree.tsx` |

**Loading (5 components):**
| Component | File |
|-----------|------|
| Spinner | `cacao/LoadingStates.tsx` |
| Skeleton | `cacao/LoadingStates.tsx` |
| SkeletonText | `cacao/LoadingStates.tsx` |
| LoadingOverlay | `cacao/LoadingStates.tsx` |
| EmptyState | `cacao/LoadingStates.tsx` |

**Error Handling (1 component):**
| Component | File |
|-----------|------|
| ErrorBoundary | `cacao/ErrorBoundary.tsx` |

**Hooks (2 modules):**
| Hook | File |
|------|------|
| useForm | `cacao/useForm.ts` |
| useAdvanced | `cacao/useAdvanced.ts` |

**TypeScript Client Total: 33 components + 2 hook modules**

---

### Missing Critical DX Features

| Feature | Status | Priority | Notes |
|---------|--------|----------|-------|
| Command palette (Cmd+K) | NOT implemented | **P0** | Standard in dev tools, devs expect this |
| Copy-to-clipboard | NOT implemented | **P0** | Missing on code blocks and metric values |
| Keyboard shortcuts | Minimal | **P0** | No shortcut system |
| Toast notifications | NOT implemented | **P1** | No mechanism for user feedback |
| Syntax highlighting | NOT implemented | **P1** | Code blocks are plain monospace text |
| Theme toggle UI | Partial | **P1** | `data-theme` attribute works but no toggle component |
| Dark/light mode persistence | NOT implemented | **P1** | No localStorage read/write |
| Collapsible sections (Accordion) | Partial | **P2** | Nav groups collapse but no general Accordion |
| Search component | NOT implemented | **P2** | No reusable search/filter pattern |
| Drag-and-drop | NOT implemented | **P2** | No DnD support |

### The "Screenshot Moment"

Every great framework has a moment that makes developers want to share a screenshot. For Cacao, this should be:

**A command palette (Cmd+K) with fuzzy search** across plugins, transformers, skills, and navigation items.

Imagine: a developer presses Cmd+K, types "base64", and instantly sees the relevant plugin, its transformers, and a quick-action to navigate there. This is the kind of feature that gets shared on social media and in developer communities.

### Theme Persistence Gap

The `data-theme` attribute on `<html>` enables runtime theme switching, but:
- No `localStorage` read on page load to restore preference
- No `localStorage` write when theme changes
- No UI component (toggle button or dropdown) to switch themes
- System preference (`prefers-color-scheme`) is not detected

### Recommendations

**P0 -- Implement immediately:**
1. Command palette with Cmd+K shortcut and fuzzy search.
2. Copy-to-clipboard buttons on code blocks and metric/statistic values.
3. Global keyboard shortcut system (register/unregister pattern).

**P1 -- Implement soon:**
4. Toast/notification system with auto-dismiss and manual close.
5. Syntax highlighting for code blocks (Prism.js or Shiki).
6. Theme toggle component with localStorage persistence and `prefers-color-scheme` detection.

**P2 -- Implement when ready:**
7. General-purpose Accordion component (not just nav groups).
8. Reusable Search component with debounced input and result highlighting.
9. Drag-and-drop support for sortable lists and file upload zones.

---

## Cross-Cutting Summary

### Priority Matrix

| Priority | Issue | Experts |
|----------|-------|---------|
| **P0** | Light theme missing status colors | Luna |
| **P0** | Hardcoded Indigo colors bypass theme system | Luna, Ren, Priya |
| **P0** | Mobile sidebar has no toggle button | Mei |
| **P0** | Touch targets below 44px minimum | Mei |
| **P0** | Zero keyboard navigation support | Priya |
| **P0** | Focus rings on only 2/28 components | Priya |
| **P0** | ARIA labels on only 1/28 components | Priya |
| **P0** | Command palette not implemented | Zara |
| **P0** | Copy-to-clipboard not implemented | Zara |
| **P1** | No @keyframes animations | Kai |
| **P1** | Accordion content has no transition | Kai |
| **P1** | Type scale conflict between JS and TS stacks | Sana |
| **P1** | No tabular figures for data display | Sana |
| **P1** | Missing 25+ critical icons | Tomas |
| **P1** | No Icon wrapper component | Tomas |
| **P1** | Toast notification system missing | Priya, Zara |
| **P1** | No syntax highlighting for code blocks | Sana, Zara |
| **P1** | Theme persistence (localStorage) missing | Zara |
| **P1** | Responsive chart heights missing | Mei |
| **P1** | Responsive typography for Title 2-4 | Sana, Mei |
| **P1** | Shadow/elevation system missing | Ren |
| **P1** | "Cacao Accent Glow" visual signature | Ren |
| **P2** | Button/card padding off 4px spacing scale | Marco |
| **P2** | No collapsed sidebar state | Marco |
| **P2** | Vite boilerplate colors in client CSS | Luna |
| **P2** | Uniform easing -- no variety | Kai |
| **P2** | JetBrains Mono missing from code font stack | Sana |
| **P2** | Tukuy theme abandons Cacao identity | Ren |
| **P2** | prefers-reduced-motion not supported | Mei, Kai |
| **P2** | Safe area insets for notched phones | Mei |
| **P2** | Search component not implemented | Diego, Zara |

### Scores by Domain

| Domain | Score | Expert |
|--------|-------|--------|
| Spatial Consistency | 6.8/10 | Marco |
| Color System | 7/10 (with critical gaps) | Luna |
| Motion & Animation | 4/10 | Kai |
| Typography | 6/10 | Sana |
| Iconography | 4/10 | Tomas |
| Interaction & A11y | 3/10 | Priya |
| Dashboard Architecture | 7/10 | Diego |
| Mobile & Responsive | 2/10 | Mei |
| Brand Identity | 3/10 | Ren |
| Developer Experience | 5/10 | Zara |

**Overall Framework UI/UX Score: 4.8 / 10**

### Key Theme

The framework has **strong architectural bones** (clean component model, good theme variable system, rich data model) but is **unfinished at the surface level** (missing accessibility, no brand personality, minimal mobile support, no polish animations). The path from 4.8 to 8.0 is primarily additive -- the foundation does not need to be rebuilt, it needs to be completed.
