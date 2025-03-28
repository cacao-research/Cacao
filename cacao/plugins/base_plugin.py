from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

class BasePlugin(ABC):
    """
    Enhanced base class for all Cacao plugins with improved lifecycle management,
    configuration handling, and error reporting.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config: Dict[str, Any] = {}
        self.initialized: bool = False
        self._version: str = "1.0.0"
        self._dependencies: Dict[str, str] = {}

    @property
    def version(self) -> str:
        """Get plugin version."""
        return self._version

    @property
    def dependencies(self) -> Dict[str, str]:
        """Get plugin dependencies."""
        return self._dependencies

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the plugin with the provided settings.
        
        Args:
            config: Dictionary containing plugin configuration
        """
        self.validate_config(config)
        self.config = config

    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate the provided configuration.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        pass

    def initialize(self) -> None:
        """
        Initialize plugin resources and validate dependencies.
        
        Raises:
            RuntimeError: If initialization fails
        """
        if self.initialized:
            return
        
        try:
            self._check_dependencies()
            self._initialize_resources()
            self.initialized = True
        except Exception as e:
            self.logger.error(f"Failed to initialize plugin: {str(e)}")
            raise RuntimeError(f"Plugin initialization failed: {str(e)}")

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.
        """
        if not self.initialized:
            return
        
        try:
            self._cleanup_resources()
            self.initialized = False
        except Exception as e:
            self.logger.error(f"Failed to cleanup plugin: {str(e)}")

    def _check_dependencies(self) -> None:
        """
        Check if all required dependencies are available.
        
        Raises:
            ImportError: If a required dependency is missing
        """
        for dep, version_req in self._dependencies.items():
            try:
                module = __import__(dep)
                if hasattr(module, '__version__'):
                    # Strip the >= from the version requirement
                    min_version = version_req.replace('>=', '')
                    if module.__version__ < min_version:
                        raise ImportError(
                            f"Plugin requires {dep} {version_req}, found {module.__version__}"
                        )
            except ImportError as e:
                if "No module named" in str(e):
                    raise ImportError(f"Missing required dependency: {dep} {version_req}")
                raise

    @abstractmethod
    def _initialize_resources(self) -> None:
        """
        Initialize plugin-specific resources. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def _cleanup_resources(self) -> None:
        """
        Cleanup plugin-specific resources. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process the input data. Must be implemented by subclasses.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        pass
