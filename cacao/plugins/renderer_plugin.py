from abc import abstractmethod
from typing import Any, Dict, List, Optional
from cacao.plugins.base_plugin import BasePlugin

class RendererPlugin(BasePlugin):
    """
    Base class for renderer plugins with advanced formatting capabilities.
    """
    def __init__(self):
        super().__init__()
        self._supported_formats: List[str] = []
        self._template_dirs: List[str] = []

    @property
    def supported_formats(self) -> List[str]:
        """Get list of supported output formats."""
        return self._supported_formats

    def add_template_directory(self, path: str) -> None:
        """
        Add a directory to search for templates.
        
        Args:
            path: Directory path containing templates
        """
        if path not in self._template_dirs:
            self._template_dirs.append(path)

    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate renderer configuration.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        required_keys = ['template', 'output_format']
        missing = [key for key in required_keys if key not in config]
        if missing:
            raise ValueError(f"Missing required config keys: {', '.join(missing)}")
        
        if config['output_format'] not in self.supported_formats:
            raise ValueError(
                f"Unsupported output format: {config['output_format']}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )

    @abstractmethod
    def render(self, content: Any, template: Optional[str] = None) -> str:
        """
        Render content using optional template.
        
        Args:
            content: Content to render
            template: Optional template name to use
            
        Returns:
            Rendered content as string
        """
        pass

    def process(self, data: Any) -> str:
        """
        Process input data by rendering it according to configuration.
        
        Args:
            data: Input data to render
            
        Returns:
            Rendered output as string
        """
        template = self.config.get('template')
        return self.render(data, template)
