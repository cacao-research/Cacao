"""
React extension for Cacao.
Provides integration with React components from npm packages.
"""

import os
import asyncio
from typing import Optional
from ..core.server import CacaoServer

class ReactExtension:
    """
    Extension that adds React support to Cacao.
    
    This extension modifies the HTML template to include the React bridge script,
    which enables the use of React components from npm packages in Cacao applications.
    
    Usage:
        app = cacao.App(extensions=[ReactExtension()])
    """
    
    def __init__(self, dev_mode: bool = False):
        """
        Initialize the React extension.
        
        Args:
            dev_mode: Whether to use development versions of React (default: False)
        """
        self.dev_mode = dev_mode
        
    def apply(self, server: CacaoServer) -> None:
        """
        Apply the extension to the server.
        
        Args:
            server: The CacaoServer instance to extend
        """
        # Store the original _serve_html_template method
        original_serve_html = server._serve_html_template

        # Override the _serve_html_template method to inject scripts/CSS
        async def extended_serve_html_template(writer: asyncio.StreamWriter, session_id: str) -> None:
            # Get the HTML content by reading the template file directly
            cacao_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            template_path = os.path.join(cacao_base_dir, "core", "static", "index.html")
            
            try:
                with open(template_path, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback to the original method if file not found
                return await original_serve_html(writer, session_id)

            # Add React CSS before </head>
            css_link = '<link rel="stylesheet" href="/static/css/react-components.css">'
            if '</head>' in content:
                content = content.replace('</head>', f'  {css_link}\n</head>', 1)

            # Add React bridge script after cacao-core.js
            script_tag = '<script src="/static/js/react-bridge.js"></script>'
            cacao_core_tag = '<script src="/static/js/cacao-core.js"></script>'
            if cacao_core_tag in content:
                content = content.replace(cacao_core_tag, f'{cacao_core_tag}\n  {script_tag}', 1)
            elif '</body>' in content:
                content = content.replace('</body>', f'  {script_tag}\n</body>', 1)

            # Format the content with the session ID
            content = content.replace('{session_id}', session_id)

            # Write the response with modified content
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Set-Cookie: cacao_session={session_id}; Path=/; HttpOnly; SameSite=Strict\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
                f"{content}"
            )
            writer.write(response.encode("utf-8"))
            await writer.drain()

        # Apply the override
        server._serve_html_template = extended_serve_html_template