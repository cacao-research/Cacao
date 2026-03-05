# New Components Roadmap

Components to add to Cacao, prioritized by impact.

## High Priority — Docs/Content

### Accordion
- Collapsible sections for FAQs, expandable details
- API: `with c.accordion("Title"):` (context manager) or `c.accordion(items=[...])`
- Supports nested accordions, default open/closed, icon customization
- Multiple mode (all independent) or single mode (one open at a time)

### Steps / Stepper
- Numbered step-by-step guides with status indicators
- API: `with c.steps():` then `with c.step("Title", status="complete"):`
- Vertical and horizontal variants
- Status: pending, active, complete, error

### FileTree
- Render directory structures with icons
- API: `c.file_tree({"src": {"main.py": None, "utils/": {"helper.py": None}}})` or string-based
- Collapsible folders, file type icons, highlight active file
- Alternative: accept a string like `tree` command output

### LinkCard
- Clickable navigation cards with title, description, icon, arrow
- API: `c.link_card("Getting Started", description="Learn the basics", href="/docs/start", icon="book")`
- Grid-friendly for feature showcases or doc navigation

## High Priority — General UI

### Modal / Dialog
- Overlay dialog for confirmations, detail views, forms
- API: `c.modal(signal=show_modal, title="Confirm"):` (context manager)
- Sizes: sm, md, lg, full
- Close on backdrop click, ESC key, close button
- Needs signal-driven open/close state

### Tooltip
- Hover/focus explanations on any element
- API: `c.tooltip("Explanation text", position="top"):` wrapping child elements
- Positions: top, bottom, left, right
- Optional delay, rich content support

### Breadcrumb
- Navigation context for multi-page apps
- API: `c.breadcrumb([{"label": "Home", "href": "/"}, {"label": "Docs"}, {"label": "API"}])`
- Separator customization, icon support
- Auto-truncation for deep paths

### Image
- Standalone image with caption, lightbox, lazy loading
- API: `c.image("url", caption="Figure 1", lightbox=True, width=300)`
- Click to zoom (lightbox overlay)
- Lazy loading with placeholder

## Nice-to-Have

### Timeline
- Changelogs, version history, event sequences
- API: `with c.timeline():` then `c.timeline_item("v1.0", "Initial release", date="2024-01-01")`
- Vertical line with dots/icons, alternating layout option

### Video
- YouTube/Vimeo/direct embed with consistent styling
- API: `c.video("https://youtube.com/watch?v=...", title="Demo")` or `c.video("file.mp4")`
- Auto-detect provider, responsive aspect ratio, poster image

### Diff
- Side-by-side or unified code comparison
- API: `c.diff(old_code, new_code, language="python")`
- Line numbers, added/removed highlighting, syntax coloring

## Implementation Notes

- Each component needs: Python API (ui.py), simple API (simple.py), React component (frontend/src/components/), LESS styles, exports in index.js
- Follow existing patterns: leaf components return Component, container components use @contextmanager
- Context manager components use `_container_context()` and `with` blocks
- Leaf components use `_add_to_current_container()`
- Simple API wrappers call `_ensure_context()` before delegating
