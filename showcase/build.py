"""
Build all showcase apps into a single static site for GitHub Pages.

Usage:
    python showcase/build.py [--base-path /Cacao]

Output structure:
    dist/
        index.html          (landing page)
        demos/
            dashboard/      (cacao build output)
            metrics/
            hello/
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# Showcase app definitions: (slug, file, title, description)
DEMOS = [
    ("dashboard", "dashboard.py", "Sales Dashboard",
     "Interactive dashboard with charts, metrics, and data tables"),
    ("analytics", "analytics.py", "Analytics",
     "Multi-chart analytics with real-time data visualization"),
    ("gallery", "gallery.py", "Component Gallery",
     "Every UI component Cacao offers, all in one page"),
    ("devtools", "devtools.py", "DevTools",
     "Browser-based developer utilities — no server required"),
    ("metrics", "metrics.py", "Company Metrics",
     "KPI dashboard with progress bars, alerts, and system health"),
    ("hello", "hello.py", "Hello Cacao",
     "The simplest Cacao app — get started in 4 lines of Python"),
]

SHOWCASE_DIR = Path(__file__).parent
ROOT_DIR = SHOWCASE_DIR.parent


def build_demo(slug: str, app_file: str, base_path: str, output_dir: Path) -> bool:
    """Build a single demo app using cacao build directly."""
    from cacao.cli.commands import build_command

    app_path = str(SHOWCASE_DIR / app_file)
    demo_output = str(output_dir / "demos" / slug)

    # Base path for this demo: /Cacao/demos/dashboard
    demo_base = f"{base_path}/demos/{slug}" if base_path else ""

    print(f"  Building {slug}...")
    try:
        # Reset cacao global state between builds
        import cacao
        import cacao.simple
        cacao.reset()
        # Restore config function — build_command's
        # `from cacao.config import ...` shadows it with the submodule
        cacao.config = cacao.simple.config

        args = [app_path, "-o", demo_output, "--base-path", demo_base]
        build_command(args)
        return True
    except SystemExit:
        return False
    except Exception as e:
        print(f"    FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_landing_page(base_path: str, output_dir: Path) -> None:
    """Generate the showcase landing page."""
    asset_prefix = base_path if base_path else "."

    # Demo card icons (SVG)
    icons = {
        "dashboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="4" rx="1"/><rect x="14" y="11" width="7" height="10" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>',
        "analytics": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/></svg>',
        "gallery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>',
        "devtools": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/><line x1="14" y1="4" x2="10" y2="20"/></svg>',
        "metrics": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg>',
        "hello": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
    }

    # Build demo cards HTML
    cards_html = ""
    for slug, _, title, description in DEMOS:
        demo_url = f"{asset_prefix}/demos/{slug}/" if base_path else f"demos/{slug}/"
        icon = icons.get(slug, icons["hello"])
        cards_html += f"""
            <a href="{demo_url}" class="demo-card">
                <div class="demo-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{description}</p>
                <span class="demo-link">View Demo <span class="arrow">&rarr;</span></span>
            </a>"""

    # Feature items
    features = [
        ("Pure Python", "Write web apps in Python. No JavaScript, no HTML templates, no CSS. Just Python.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M9 12l2 2 4-4"/></svg>'),
        ("50+ Components", "Charts, tables, forms, metrics, progress bars, accordions, timelines, and more.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>'),
        ("Reactive Signals", "Built-in reactive state management. Signals automatically sync Python state to the browser.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>'),
        ("Static Builds", "Deploy anywhere with zero server. Build to static HTML/JS for GitHub Pages, S3, or any CDN.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>'),
        ("Real-time WebSocket", "Live data sync over WebSocket. Build dashboards that update in real-time.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg>'),
        ("Dark & Light Themes", "Beautiful themes out of the box. Components automatically adapt to dark and light mode.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'),
    ]

    features_html = ""
    for feat_title, feat_desc, feat_icon in features:
        features_html += f"""
            <div class="feature">
                <div class="feature-icon">{feat_icon}</div>
                <h3>{feat_title}</h3>
                <p>{feat_desc}</p>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cacao - Reactive Python Web Framework</title>
    <meta name="description" content="Build interactive dashboards and tools in pure Python. 50+ components, static builds, real-time WebSocket updates.">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #09090b;
            --bg-alt: #0f0f13;
            --surface: #18181b;
            --surface-hover: #1f1f23;
            --border: #27272a;
            --border-hover: #3f3f46;
            --text: #fafafa;
            --text-secondary: #a1a1aa;
            --muted: #71717a;
            --accent: #c4956a;
            --accent-hover: #d4a574;
            --accent-glow: rgba(196, 149, 106, 0.15);
            --accent-dim: #8b5e3c;
            --code-bg: #111113;
            --green: #4ade80;
            --blue: #60a5fa;
            --purple: #a78bfa;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* ---- Navbar ---- */
        .navbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
            padding: 0 24px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(9, 9, 11, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
        }}

        .nav-logo {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--accent);
            text-decoration: none;
            letter-spacing: -0.02em;
        }}

        .nav-links {{
            display: flex;
            gap: 32px;
            list-style: none;
        }}

        .nav-links a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .nav-links a:hover {{ color: var(--text); }}

        .nav-cta {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 20px;
            background: var(--accent-dim);
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 600;
            transition: background 0.2s;
        }}

        .nav-cta:hover {{ background: var(--accent); }}

        /* ---- Hero ---- */
        .hero {{
            position: relative;
            padding: 160px 24px 100px;
            text-align: center;
            max-width: 900px;
            margin: 0 auto;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 100px;
            font-size: 0.8rem;
            color: var(--accent);
            font-weight: 500;
            margin-bottom: 32px;
            position: relative;
            z-index: 1;
        }}

        .hero-badge .dot {{
            width: 6px;
            height: 6px;
            background: var(--green);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}

        .hero h1 {{
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.03em;
            margin-bottom: 24px;
            position: relative;
            z-index: 1;
        }}

        .hero h1 .gradient {{
            background: linear-gradient(135deg, #f5e6d3, #d4a574, #8b5e3c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero-sub {{
            font-size: 1.2rem;
            color: var(--text-secondary);
            line-height: 1.7;
            max-width: 600px;
            margin: 0 auto 40px;
            position: relative;
            z-index: 1;
        }}

        .hero-actions {{
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            border-radius: 10px;
            font-size: 0.95rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
            border: none;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--accent), var(--accent-dim));
            color: white;
            box-shadow: 0 4px 24px rgba(196, 149, 106, 0.25);
        }}

        .btn-primary:hover {{
            box-shadow: 0 8px 32px rgba(196, 149, 106, 0.35);
            transform: translateY(-1px);
        }}

        .btn-secondary {{
            background: var(--surface);
            color: var(--text);
            border: 1px solid var(--border);
        }}

        .btn-secondary:hover {{
            background: var(--surface-hover);
            border-color: var(--border-hover);
        }}

        /* ---- Install bar ---- */
        .install-bar {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-top: 32px;
            position: relative;
            z-index: 1;
        }}

        .install-cmd {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 12px 20px;
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}

        .install-cmd .prompt {{ color: var(--accent); }}
        .install-cmd .pkg {{ color: var(--text); }}

        /* ---- Stats ---- */
        .stats {{
            display: flex;
            justify-content: center;
            gap: 64px;
            padding: 60px 24px;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            background: var(--bg-alt);
        }}

        .stat {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, var(--text), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .stat-label {{
            font-size: 0.85rem;
            color: var(--muted);
            margin-top: 4px;
            font-weight: 500;
        }}

        /* ---- Code showcase ---- */
        .code-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 100px 24px;
        }}

        .code-section .section-label {{
            text-align: center;
            margin-bottom: 48px;
        }}

        .code-compare {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2px;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .code-panel {{
            background: var(--code-bg);
            padding: 32px;
        }}

        .code-panel-label {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--muted);
            margin-bottom: 20px;
        }}

        .code-panel pre {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            line-height: 1.7;
            overflow-x: auto;
        }}

        .code-panel pre .kw {{ color: #c678dd; }}
        .code-panel pre .fn {{ color: #61afef; }}
        .code-panel pre .str {{ color: #98c379; }}
        .code-panel pre .num {{ color: #d19a66; }}
        .code-panel pre .cm {{ color: #5c6370; font-style: italic; }}
        .code-panel pre .op {{ color: #56b6c2; }}

        .result-panel {{
            background: var(--surface);
            padding: 32px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .mock-metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            background: var(--bg);
            border-radius: 10px;
            border: 1px solid var(--border);
        }}

        .mock-metric-label {{
            font-size: 0.85rem;
            color: var(--muted);
        }}

        .mock-metric-value {{
            font-size: 1.5rem;
            font-weight: 700;
        }}

        .mock-metric-trend {{
            font-size: 0.8rem;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .trend-up {{
            color: var(--green);
            background: rgba(74, 222, 128, 0.1);
        }}

        .mock-chart {{
            height: 120px;
            background: var(--bg);
            border-radius: 10px;
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}

        .mock-chart svg {{
            width: 100%;
            height: 100%;
        }}

        /* ---- Features ---- */
        .features {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 100px 24px;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
        }}

        .feature {{
            padding: 32px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            transition: border-color 0.2s, transform 0.2s;
        }}

        .feature:hover {{
            border-color: var(--border-hover);
            transform: translateY(-2px);
        }}

        .feature-icon {{
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--accent-glow);
            border-radius: 10px;
            margin-bottom: 20px;
            color: var(--accent);
        }}

        .feature-icon svg {{ width: 22px; height: 22px; }}

        .feature h3 {{
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .feature p {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        /* ---- Section labels ---- */
        .section-label h2 {{
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 12px;
        }}

        .section-label p {{
            font-size: 1.05rem;
            color: var(--text-secondary);
        }}

        /* ---- Demos ---- */
        .demos-section {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 100px 24px;
        }}

        .demos-section .section-label {{
            text-align: center;
            margin-bottom: 48px;
        }}

        .demos-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}

        .demo-card {{
            display: flex;
            flex-direction: column;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 28px;
            text-decoration: none;
            color: inherit;
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }}

        .demo-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .demo-card:hover {{
            border-color: var(--accent-dim);
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        }}

        .demo-card:hover::before {{ opacity: 1; }}

        .demo-icon {{
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--accent-glow);
            border-radius: 10px;
            margin-bottom: 20px;
            color: var(--accent);
        }}

        .demo-icon svg {{ width: 22px; height: 22px; }}

        .demo-card h3 {{
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .demo-card p {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.5;
            flex: 1;
        }}

        .demo-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 20px;
            color: var(--accent);
            font-weight: 600;
            font-size: 0.875rem;
        }}

        .demo-link .arrow {{
            transition: transform 0.2s;
            display: inline-block;
        }}

        .demo-card:hover .demo-link .arrow {{
            transform: translateX(4px);
        }}

        /* ---- Footer ---- */
        .footer {{
            text-align: center;
            padding: 60px 24px;
            border-top: 1px solid var(--border);
            background: var(--bg-alt);
        }}

        .footer-logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent);
            margin-bottom: 16px;
        }}

        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-bottom: 24px;
        }}

        .footer-links a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .footer-links a:hover {{ color: var(--text); }}

        .footer-copy {{
            font-size: 0.8rem;
            color: var(--muted);
        }}

        /* ---- Responsive ---- */
        @media (max-width: 768px) {{
            .nav-links {{ display: none; }}
            .stats {{ gap: 32px; flex-wrap: wrap; }}
            .stat-value {{ font-size: 2rem; }}
            .code-compare {{ grid-template-columns: 1fr; }}
            .features-grid {{ grid-template-columns: 1fr; }}
            .demos-grid {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 2.5rem; }}
        }}

        @media (max-width: 1024px) {{
            .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .demos-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <a href="#" class="nav-logo">Cacao</a>
        <ul class="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#code">Code</a></li>
            <li><a href="#demos">Demos</a></li>
        </ul>
        <a href="https://github.com/cacao-research/Cacao" class="nav-cta" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
            GitHub
        </a>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div class="hero-badge">
            <span class="dot"></span>
            Open Source &middot; pip install cacao
        </div>
        <h1>
            Build web apps in<br>
            <span class="gradient">pure Python</span>
        </h1>
        <p class="hero-sub">
            Cacao is a reactive framework that turns Python scripts into interactive
            dashboards, internal tools, and data apps. No frontend skills required.
        </p>
        <div class="hero-actions">
            <a href="#demos" class="btn btn-primary">Explore Demos</a>
            <a href="https://github.com/cacao-research/Cacao" class="btn btn-secondary" target="_blank">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
                Star on GitHub
            </a>
        </div>
        <div class="install-bar">
            <div class="install-cmd">
                <span class="prompt">$</span>
                <span class="pkg">pip install cacao</span>
            </div>
        </div>
    </section>

    <!-- Stats -->
    <section class="stats">
        <div class="stat">
            <div class="stat-value">50+</div>
            <div class="stat-label">Components</div>
        </div>
        <div class="stat">
            <div class="stat-value">6</div>
            <div class="stat-label">Chart Types</div>
        </div>
        <div class="stat">
            <div class="stat-value">0</div>
            <div class="stat-label">JavaScript Required</div>
        </div>
        <div class="stat">
            <div class="stat-value">4</div>
            <div class="stat-label">Lines to Start</div>
        </div>
    </section>

    <!-- Code Showcase -->
    <section class="code-section" id="code">
        <div class="section-label">
            <h2>Write Python. Get a web app.</h2>
            <p>Cacao turns simple Python scripts into polished, interactive interfaces.</p>
        </div>
        <div class="code-compare">
            <div class="code-panel">
                <div class="code-panel-label">app.py</div>
                <pre><span class="kw">import</span> cacao <span class="kw">as</span> c

c.<span class="fn">config</span>(<span class="str">title</span>=<span class="str">"My Dashboard"</span>)

<span class="kw">with</span> c.<span class="fn">row</span>():
    c.<span class="fn">metric</span>(<span class="str">"Revenue"</span>, <span class="str">"$45K"</span>,
           <span class="str">trend</span>=<span class="str">"+20%"</span>, <span class="str">trend_direction</span>=<span class="str">"up"</span>)
    c.<span class="fn">metric</span>(<span class="str">"Users"</span>, <span class="str">"1,247"</span>,
           <span class="str">trend</span>=<span class="str">"+12%"</span>, <span class="str">trend_direction</span>=<span class="str">"up"</span>)

<span class="kw">with</span> c.<span class="fn">card</span>(<span class="str">"Trend"</span>):
    c.<span class="fn">line</span>(data, <span class="str">x</span>=<span class="str">"date"</span>, <span class="str">y</span>=<span class="str">"revenue"</span>)</pre>
            </div>
            <div class="code-panel result-panel">
                <div class="code-panel-label">Result</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <div class="mock-metric">
                        <div>
                            <div class="mock-metric-label">Revenue</div>
                            <div class="mock-metric-value">$45K</div>
                        </div>
                        <span class="mock-metric-trend trend-up">+20%</span>
                    </div>
                    <div class="mock-metric">
                        <div>
                            <div class="mock-metric-label">Users</div>
                            <div class="mock-metric-value">1,247</div>
                        </div>
                        <span class="mock-metric-trend trend-up">+12%</span>
                    </div>
                </div>
                <div style="padding: 16px 20px; background: var(--bg); border-radius: 10px; border: 1px solid var(--border);">
                    <div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">Trend</div>
                    <div class="mock-chart">
                        <svg viewBox="0 0 400 120" preserveAspectRatio="none">
                            <defs>
                                <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="rgba(196,149,106,0.3)"/>
                                    <stop offset="100%" stop-color="rgba(196,149,106,0)"/>
                                </linearGradient>
                            </defs>
                            <path d="M0,100 Q50,90 100,70 T200,50 T300,35 T400,20 L400,120 L0,120 Z" fill="url(#chartGrad)"/>
                            <path d="M0,100 Q50,90 100,70 T200,50 T300,35 T400,20" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section class="features" id="features">
        <div class="section-label" style="text-align: center; margin-bottom: 48px;">
            <h2>Everything you need</h2>
            <p>A complete toolkit for building data-driven web applications.</p>
        </div>
        <div class="features-grid">{features_html}
        </div>
    </section>

    <!-- Demos -->
    <section class="demos-section" id="demos">
        <div class="section-label">
            <h2>Live Demos</h2>
            <p>Each demo is a static build &mdash; no server, just HTML, CSS, and JS generated from Python.</p>
        </div>
        <div class="demos-grid">{cards_html}
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-logo">Cacao</div>
        <div class="footer-links">
            <a href="https://github.com/cacao-research/Cacao" target="_blank">GitHub</a>
            <a href="https://pypi.org/project/cacao/" target="_blank">PyPI</a>
            <a href="https://github.com/cacao-research/Cacao#readme" target="_blank">Documentation</a>
        </div>
        <div class="footer-copy">
            Built with Cacao &middot; Open Source under MIT License
        </div>
    </footer>

    <script>
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(a => {{
            a.addEventListener('click', e => {{
                e.preventDefault();
                const target = document.querySelector(a.getAttribute('href'));
                if (target) target.scrollIntoView({{ behavior: 'smooth' }});
            }});
        }});

        // Animate stats on scroll
        const observer = new IntersectionObserver(entries => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }});
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.stat, .feature, .demo-card').forEach(el => {{
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        }});
    </script>
</body>
</html>"""

    (output_dir / "index.html").write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Cacao showcase for GitHub Pages")
    parser.add_argument("--base-path", default="", help="Base path (e.g., /Cacao)")
    parser.add_argument("-o", "--output", default="dist", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output)
    base_path = args.base_path.rstrip("/")

    # Clean output
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    print(f"Building Cacao showcase...")
    print(f"  Output: {output_dir.resolve()}")
    if base_path:
        print(f"  Base path: {base_path}")
    print()

    # Build each demo
    success = 0
    for slug, app_file, title, desc in DEMOS:
        if build_demo(slug, app_file, base_path, output_dir):
            success += 1

    print()

    # Generate landing page
    generate_landing_page(base_path, output_dir)
    print(f"Generated landing page")

    print(f"\nDone: {success}/{len(DEMOS)} demos built")
    print(f"Preview: python -m http.server -d {output_dir}")


if __name__ == "__main__":
    main()
