import os
import json
from typing import Any, Dict, Optional
import jinja2
import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from .renderer_plugin import RendererPlugin
from .theme import theme_manager

class HtmlRendererPlugin(RendererPlugin):
    """
    Advanced HTML renderer with syntax highlighting, templating, and CSS framework support.
    """
    def __init__(self):
        super().__init__()
        self._supported_formats = ['html', 'html5']
        self._dependencies = {
            'jinja2': '>=3.0.0',  # Fixed version requirement
            'pygments': '>=2.10.0'
        }
        self._jinja_env = None
        self._formatter = HtmlFormatter(
            style='monokai',
            cssclass='highlight',
            linenos=True
        )
        self._template_dirs = []

    def _initialize_resources(self) -> None:
        """Initialize Jinja environment and other resources."""
        if 'template_dir' in self.config:
            self._template_dirs.append(self.config['template_dir'])
        
        self._jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self._template_dirs),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self._jinja_env.filters.update({
            'highlight_code': self._highlight_code,
            'to_json': self._to_json,
            'generate_toc': self._generate_toc,
            'static_url': lambda path: f"/_static/{path}"
        })

    def _cleanup_resources(self) -> None:
        """Cleanup renderer resources."""
        self._jinja_env = None

    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate HTML renderer configuration.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        super().validate_config(config)
        
        # Validate CSS framework settings if specified
        css_framework = config.get('css_framework', {})
        if css_framework:
            if 'name' not in css_framework:
                raise ValueError("CSS framework configuration must include 'name'")
            
            supported_frameworks = ['bootstrap', 'tailwind', 'bulma']
            if css_framework['name'] not in supported_frameworks:
                raise ValueError(
                    f"Unsupported CSS framework: {css_framework['name']}. "
                    f"Supported frameworks: {', '.join(supported_frameworks)}"
                )

    def _highlight_code(self, code: str, language: str = 'python') -> str:
        """
        Syntax highlight code using Pygments.
        
        Args:
            code: Code to highlight
            language: Programming language
            
        Returns:
            HTML with syntax highlighting
        """
        try:
            lexer = get_lexer_by_name(language)
            return highlight(code, lexer, self._formatter)
        except ClassNotFound:
            return code

    def _to_json(self, value: Any) -> str:
        """
        Convert value to JSON string.
        
        Args:
            value: Value to convert
            
        Returns:
            JSON string
        """
        return json.dumps(value, indent=2)

    def _generate_toc(self, content: str) -> str:
        """
        Generate table of contents from HTML content.
        
        Args:
            content: HTML content
            
        Returns:
            Table of contents HTML
        """
        # Simple TOC generation - could be enhanced with BeautifulSoup
        import re
        toc = ['<ul class="toc">']
        for match in re.finditer(r'<h([1-6]).*?>(.*?)</h\1>', content):
            level, title = match.groups()
            toc.append(
                f'<li class="toc-level-{level}">'
                f'<a href="#{title.lower().replace(" ", "-")}">{title}</a>'
                '</li>'
            )
        toc.append('</ul>')
        return '\n'.join(toc)

    def get_css(self) -> str:
        """
        Get combined CSS including syntax highlighting, theme styles, and framework.
        
        Returns:
            Combined CSS string
        """
        css_parts = [self._formatter.get_style_defs()]
        
        # Process theme CSS with variables
        try:
            css_file = os.path.join(theme_manager.static_dir, 'style.css')
            with open(css_file, 'r') as f:
                css_template = f.read()
                
            # Create a temporary Jinja environment for CSS
            css_env = jinja2.Environment()
            template = css_env.from_string(css_template)
            theme_css = template.render(
                theme={
                    'options': theme_manager.theme_options
                }
            )
            css_parts.append(theme_css)
        except Exception as e:
            self.logger.error(f"Failed to process theme CSS: {str(e)}")
        
        # Add CSS framework if configured
        framework = self.config.get('css_framework', {}).get('name')
        if framework:
            framework_css = self._get_framework_css(framework)
            if framework_css:
                css_parts.append(framework_css)
        
        return '\n'.join(css_parts)

    def _get_framework_css(self, framework: str) -> Optional[str]:
        """
        Get CSS framework code.
        
        Args:
            framework: Framework name
            
        Returns:
            CSS string or None if not found
        """
        framework_paths = {
            'bootstrap': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
            'tailwind': 'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
            'bulma': 'https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css'
        }
        
        if framework in framework_paths:
            return f'<link rel="stylesheet" href="{framework_paths[framework]}">'
        return None

    def render(self, content: Any, template: Optional[str] = None) -> str:
        """
        Render content using template.
        
        Args:
            content: Content to render
            template: Optional template name
            
        Returns:
            Rendered HTML
        """
        if not self._jinja_env:
            raise RuntimeError("Renderer not initialized")
        
        # Use default template if none specified
        template_name = template or self.config.get('template', 'page.html')
        
        try:
            template = self._jinja_env.get_template(template_name)
            
            # Prepare theme context
            theme_context = {
                'name': theme_manager.current_theme,
                'options': theme_manager.theme_options,
                'static_dir': theme_manager.static_dir,
                'get_static_url': lambda path: f"/_static/{path}"
            }
            
            # Merge content with theme options
            if isinstance(content, dict):
                content.update({
                    'enable_search': theme_manager.theme_options.get('enable_search', True),
                    'enable_toc': theme_manager.theme_options.get('enable_toc', True),
                    'primary_color': theme_manager.theme_options.get('primary_color', '#2563eb'),
                    'secondary_color': theme_manager.theme_options.get('secondary_color', '#475569')
                })
            
            return template.render(
                content=content,
                theme=theme_context,
                css=self.get_css(),
                config=self.config
            )
        except jinja2.TemplateNotFound as e:
            raise RuntimeError(f"Template not found: {template_name}. Error: {str(e)}")
