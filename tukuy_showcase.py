"""
Tukuy Plugin Showcase - Powered by Cacao

Browse all Tukuy plugins, their transformers, skills, and requirements
in a clean admin-style dashboard with the Tukuy theme.

Run with: cacao run tukuy_showcase.py
"""

import cacao as c

# ---------------------------------------------------------------------------
# Discover plugins via the shared registry
# ---------------------------------------------------------------------------

from tukuy.registry import get_shared_registry

registry = get_shared_registry()

# Group ordering and icons
GROUP_ORDER = [
    "Core", "Data", "Web", "Code", "Integrations",
    "Documents", "Media", "Prompt Engineering", "Other",
]

GROUP_ICONS = {
    "Core": "layers",
    "Data": "database",
    "Web": "globe",
    "Code": "code",
    "Integrations": "plug",
    "Documents": "file-text",
    "Media": "image",
    "Prompt Engineering": "message-square",
    "Other": "package",
}

RISK_COLORS = {
    "safe": "success",
    "moderate": "warning",
    "dangerous": "danger",
    "critical": "danger",
}

# ---------------------------------------------------------------------------
# Build structured catalog from live registry
# ---------------------------------------------------------------------------

catalog: dict[str, list[dict]] = {}

for name, plugin in registry.plugins.items():
    manifest = plugin.manifest
    group = manifest.group or "Other"

    transformers = {}
    try:
        transformers = plugin.transformers or {}
    except Exception:
        pass

    skills = {}
    try:
        skills = plugin.skills or {}
    except Exception:
        pass

    entry = {
        "name": manifest.name,
        "display_name": manifest.display_name,
        "description": manifest.description,
        "icon": manifest.icon or "box",
        "group": group,
        "version": manifest.version,
        "experimental": manifest.experimental,
        "deprecated": manifest.deprecated,
        "requires": manifest.requires.to_dict(),
        "transformer_names": sorted(transformers.keys()),
        "skill_names": sorted(skills.keys()),
        "skill_descriptors": {},
    }

    for sname, skill_obj in skills.items():
        desc = skill_obj.descriptor
        entry["skill_descriptors"][sname] = {
            "display_name": desc.resolved_display_name,
            "description": desc.description,
            "category": desc.category,
            "risk_level": desc.resolved_risk_level.value,
            "tags": desc.tags,
            "is_async": desc.is_async,
            "requires_network": desc.requires_network,
            "requires_filesystem": desc.requires_filesystem,
            "input_schema": desc.input_schema,
            "output_schema": desc.output_schema,
        }

    catalog.setdefault(group, []).append(entry)

for group in catalog:
    catalog[group].sort(key=lambda p: p["display_name"])

ordered_groups = [g for g in GROUP_ORDER if g in catalog]
for g in sorted(catalog.keys()):
    if g not in ordered_groups:
        ordered_groups.append(g)

# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------

total_plugins = sum(len(plugins) for plugins in catalog.values())
total_transformers = sum(
    len(p["transformer_names"])
    for plugins in catalog.values()
    for p in plugins
)
total_skills = sum(
    len(p["skill_names"])
    for plugins in catalog.values()
    for p in plugins
)

# Count requirement types across all plugins
plugins_with_network = 0
plugins_with_filesystem = 0
for plugins in catalog.values():
    for p in plugins:
        if p["requires"].get("network"):
            plugins_with_network += 1
        if p["requires"].get("filesystem"):
            plugins_with_filesystem += 1

# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

c.config(title="Tukuy", theme="tukuy-light")

with c.app_shell(brand="Tukuy", default="overview",
                 theme_dark="tukuy", theme_light="tukuy-light"):

    # -- Sidebar --
    with c.nav_sidebar():
        c.nav_item("Overview", key="overview", icon="home")

        for group in ordered_groups:
            plugins = catalog[group]
            icon = GROUP_ICONS.get(group, "package")
            with c.nav_group(group, icon=icon):
                for plugin in plugins:
                    n_items = len(plugin["transformer_names"]) + len(plugin["skill_names"])
                    c.nav_item(
                        plugin["display_name"],
                        key=plugin["name"],
                        icon=plugin["icon"],
                        badge=str(n_items) if n_items else None,
                    )

    # -- Content --
    with c.shell_content():

        # ── Overview ──
        with c.nav_panel("overview"):

            c.title("Tukuy")
            c.text(
                "Tukuy (Quechua: to transform) is a portable Python library for "
                "agent skills and data transformation. It provides a typed, "
                "framework-agnostic system for declaring, composing, and exposing "
                "Python functions as skills that any LLM agent can consume.",
                color="muted",
            )

            c.spacer(size=2)

            # What Tukuy does
            with c.row(gap=4, wrap=True):
                with c.card("Data Transformation"):
                    c.text(
                        "Chain named operations into pipelines: text, HTML, JSON, "
                        "dates, numbers, validation, and more. Over 70 built-in "
                        "plugins cover everything from string manipulation to "
                        "external API integrations.",
                        size="sm",
                    )
                with c.card("Agent Skills"):
                    c.text(
                        "Declare Python functions as typed skills with auto-inferred "
                        "JSON schemas. Bridge to OpenAI, Anthropic, and MCP formats "
                        "with a single decorator. Built-in safety policies and "
                        "sandboxed execution.",
                        size="sm",
                    )
                with c.card("Composable Chains"):
                    c.text(
                        "Build pipelines with Chain, Branch, and Parallel primitives. "
                        "Steps can be transformer names, skill functions, or nested "
                        "chains. Runs sync or async.",
                        size="sm",
                    )

            c.spacer()

            # KPI row
            with c.row():
                c.metric("Plugins", total_plugins)
                c.metric("Transformers", total_transformers)
                c.metric("Skills", total_skills)
                c.metric("Groups", len(ordered_groups))

            c.spacer()

            with c.row(gap=2, wrap=True):
                c.badge(f"{plugins_with_network} network plugins", color="info")
                c.badge(f"{plugins_with_filesystem} filesystem plugins", color="warning")
                c.badge(f"{total_plugins - plugins_with_network - plugins_with_filesystem} pure plugins", color="success")

            c.spacer()

            # Group summary table
            group_rows = []
            for group in ordered_groups:
                plugins = catalog[group]
                t_count = sum(len(p["transformer_names"]) for p in plugins)
                s_count = sum(len(p["skill_names"]) for p in plugins)
                group_rows.append({
                    "Group": group,
                    "Plugins": len(plugins),
                    "Transformers": t_count,
                    "Skills": s_count,
                })

            with c.card("Groups"):
                c.table(
                    group_rows,
                    columns=["Group", "Plugins", "Transformers", "Skills"],
                    searchable=True,
                )

            c.spacer()

            # Full plugin catalog table
            all_plugins_table = []
            for group in ordered_groups:
                for p in catalog[group]:
                    requires_tags = []
                    if p["requires"].get("filesystem"):
                        requires_tags.append("filesystem")
                    if p["requires"].get("network"):
                        requires_tags.append("network")
                    all_plugins_table.append({
                        "Plugin": p["display_name"],
                        "Group": group,
                        "Transformers": len(p["transformer_names"]),
                        "Skills": len(p["skill_names"]),
                        "Requires": ", ".join(requires_tags) if requires_tags else "-",
                        "Version": p["version"],
                    })

            with c.card("All Plugins"):
                c.table(
                    all_plugins_table,
                    columns=["Plugin", "Group", "Transformers", "Skills", "Requires", "Version"],
                    searchable=True,
                    page_size=15,
                )

        # ── Per-plugin panels ──
        for group in ordered_groups:
            for plugin in catalog[group]:
                with c.nav_panel(plugin["name"]):

                    c.title(plugin["display_name"])
                    if plugin["description"]:
                        c.text(plugin["description"], color="muted")

                    c.spacer(size=2)

                    # Badges
                    with c.row(gap=2, wrap=True):
                        c.badge(plugin["group"], color="primary")
                        c.badge(f"v{plugin['version']}", color="info")
                        if plugin["experimental"]:
                            c.badge("Experimental", color="warning")
                        if plugin["deprecated"]:
                            c.badge("Deprecated", color="danger")
                        if plugin["requires"].get("filesystem"):
                            c.badge("Filesystem", color="warning")
                        if plugin["requires"].get("network"):
                            c.badge("Network", color="warning")
                        for imp in plugin["requires"].get("imports", []):
                            c.badge(imp, color="info")

                    c.spacer()

                    # Quick stats
                    with c.row():
                        c.metric("Transformers", len(plugin["transformer_names"]))
                        c.metric("Skills", len(plugin["skill_names"]))

                    c.spacer()

                    # Tabs for transformers / skills
                    has_transformers = bool(plugin["transformer_names"])
                    has_skills = bool(plugin["skill_names"])

                    if has_transformers or has_skills:
                        default_tab = "transformers" if has_transformers else "skills"
                        with c.tabs(default=default_tab):

                            if has_transformers:
                                with c.tab("transformers", "Transformers"):
                                    transformer_rows = [
                                        {"Name": t} for t in plugin["transformer_names"]
                                    ]
                                    c.table(
                                        transformer_rows,
                                        columns=["Name"],
                                        searchable=True,
                                    )

                            if has_skills:
                                with c.tab("skills", "Skills"):
                                    for sname in plugin["skill_names"]:
                                        sd = plugin["skill_descriptors"].get(sname, {})
                                        with c.card(sd.get("display_name", sname)):
                                            if sd.get("description"):
                                                c.text(sd["description"], size="sm")
                                            c.spacer(size=1)

                                            with c.row(gap=2, wrap=True):
                                                risk = sd.get("risk_level", "safe")
                                                c.badge(risk, color=RISK_COLORS.get(risk, "default"))
                                                if sd.get("is_async"):
                                                    c.badge("async", color="info")
                                                if sd.get("requires_network"):
                                                    c.badge("network", color="warning")
                                                if sd.get("requires_filesystem"):
                                                    c.badge("filesystem", color="warning")
                                                for tag in sd.get("tags", []):
                                                    c.badge(tag, color="default")

                                            if sd.get("input_schema"):
                                                c.spacer(size=1)
                                                c.text("Input Schema", size="sm", color="muted")
                                                c.json(sd["input_schema"], expanded=False)

                    else:
                        c.alert(
                            "This plugin provides no transformers or skills.",
                            type="info",
                        )
