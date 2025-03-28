import os
from typing import Any, Dict, Optional
import markdown
import frontmatter
from .renderer_plugin import RendererPlugin

class MarkdownParserPlugin(RendererPlugin):
    """
    Advanced Markdown renderer with frontmatter support and extended syntax.
    """
    def __init__(self):
        super().__init__()
        self._supported_formats = ['md', 'markdown']
        self._dependencies = {
            'markdown': '>=3.3.0',
            'python-frontmatter': '>=1.0.0'
        }
        self._markdown = None
        self._extensions = [
            'extra',              # Tables, footnotes, etc.
            'codehilite',         # Syntax highlighting
            'meta',               # Metadata
            'toc',               # Table of contents
            'sane_lists',        # Better list handling
            'smarty',            # Smart quotes
            'attr_list',         # HTML attributes
            'def_list',          # Definition lists
            'fenced_code',       # Fenced code blocks
            'admonition',        # Admonitions
            'abbr',              # Abbreviations
        ]
        self._extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'linenums': True,
                'guess_lang': True
            },
            'toc': {
                'permalink': True,
                'baselevel': 1,
                'separator': '_'
            }
        }

    def _initialize_resources(self) -> None:
        """Initialize Markdown processor with extensions."""
        self._markdown = markdown.Markdown(
            extensions=self._extensions,
            extension_configs=self._extension_configs
        )

    def _cleanup_resources(self) -> None:
        """Cleanup renderer resources."""
        self._markdown = None

    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate Markdown renderer configuration.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        super().validate_config(config)
        
        # Validate Markdown-specific settings
        md_config = config.get('markdown', {})
        if md_config:
            if 'extensions' in md_config:
                invalid_extensions = [
                    ext for ext in md_config['extensions']
                    if not self._is_valid_extension(ext)
                ]
                if invalid_extensions:
                    raise ValueError(
                        f"Invalid Markdown extensions: {', '.join(invalid_extensions)}"
                    )

    def _is_valid_extension(self, extension: str) -> bool:
        """
        Check if a Markdown extension is valid.
        
        Args:
            extension: Extension name to check
            
        Returns:
            True if extension is valid
        """
        try:
            markdown.Markdown(extensions=[extension])
            return True
        except Exception:
            return False

    def _process_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract and process frontmatter from content.
        
        Args:
            content: Content to process
            
        Returns:
            Dictionary of metadata from frontmatter
        """
        post = frontmatter.loads(content)
        return {
            'content': post.content,
            'metadata': post.metadata
        }

    def _apply_extensions(self, content: str) -> str:
        """
        Apply Markdown extensions to content.
        
        Args:
            content: Content to process
            
        Returns:
            Processed content
        """
        if not self._markdown:
            raise RuntimeError("Markdown processor not initialized")
        
        # Reset the processor to handle multiple conversions
        self._markdown.reset()
        return self._markdown.convert(content)

    def _post_process(self, html: str) -> str:
        """
        Apply post-processing to rendered HTML.
        
        Args:
            html: HTML content to process
            
        Returns:
            Processed HTML
        """
        # Add anchor links to headers
        import re
        html = re.sub(
            r'<h([1-6])>(.*?)</h\1>',
            lambda m: (
                f'<h{m.group(1)} id="{m.group(2).lower().replace(" ", "-")}">'
                f'{m.group(2)}'
                f'<a href="#{m.group(2).lower().replace(" ", "-")}" class="anchor">#</a>'
                f'</h{m.group(1)}>'
            ),
            html
        )
        return html

    def render(self, content: Any, template: Optional[str] = None) -> str:
        """
        Render Markdown content to HTML.
        
        Args:
            content: Content to render
            template: Optional template name
            
        Returns:
            Rendered HTML
        """
        if isinstance(content, str):
            # Process frontmatter if present
            processed = self._process_frontmatter(content)
            html_content = self._apply_extensions(processed['content'])
            html_content = self._post_process(html_content)
            
            # Prepare data for template
            template_data = {
                'content': html_content,
                'metadata': processed['metadata'],
                'toc': self._markdown.toc if hasattr(self._markdown, 'toc') else ''
            }
            
            # Use template if specified
            if template:
                return super().render(template_data, template)
            
            # Otherwise return processed HTML
            return html_content
        else:
            raise ValueError("Content must be a string for Markdown rendering")
