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

    # Build demo cards HTML
    cards_html = ""
    for slug, _, title, description in DEMOS:
        demo_url = f"{asset_prefix}/demos/{slug}/" if base_path else f"demos/{slug}/"
        cards_html += f"""
        <a href="{demo_url}" class="demo-card">
            <h3>{title}</h3>
            <p>{description}</p>
            <span class="demo-link">View Demo &rarr;</span>
        </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cacao Showcase</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f1117;
            --surface: #1a1b23;
            --border: #2a2b35;
            --text: #e4e4e7;
            --muted: #71717a;
            --accent: #8b5e3c;
            --accent-light: #a0714d;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }}

        .hero {{
            text-align: center;
            padding: 80px 24px 48px;
            max-width: 720px;
            margin: 0 auto;
        }}

        .hero h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #d4a574, #8b5e3c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero p {{
            font-size: 1.2rem;
            color: var(--muted);
            line-height: 1.6;
        }}

        .demos {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 24px;
            max-width: 1080px;
            margin: 0 auto;
            padding: 24px;
        }}

        .demo-card {{
            display: flex;
            flex-direction: column;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 28px;
            text-decoration: none;
            color: inherit;
            transition: border-color 0.2s, transform 0.2s;
        }}

        .demo-card:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
        }}

        .demo-card h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .demo-card p {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.5;
            flex: 1;
        }}

        .demo-link {{
            display: inline-block;
            margin-top: 16px;
            color: var(--accent-light);
            font-weight: 500;
            font-size: 0.9rem;
        }}

        .footer {{
            text-align: center;
            padding: 48px 24px;
            color: var(--muted);
            font-size: 0.85rem;
        }}

        .footer a {{
            color: var(--accent-light);
            text-decoration: none;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Cacao Showcase</h1>
        <p>Interactive demos built with Cacao &mdash; the reactive Python web framework.
           Each demo runs entirely in the browser as a static build.</p>
    </div>

    <div class="demos">{cards_html}
    </div>

    <div class="footer">
        Built with <a href="https://github.com/cacao-research/Cacao">Cacao</a>
        &middot; <a href="https://github.com/cacao-research/Cacao">GitHub</a>
        &middot; <a href="https://pypi.org/project/cacao/">PyPI</a>
    </div>
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
