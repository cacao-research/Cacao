import pytest
from cacao.extensions.plugins import Plugin, register_plugin, PLUGINS

class TestPlugin(Plugin):
    """Test plugin implementation for testing purposes."""
    __test__ = False  # Prevent pytest from collecting this class
    
    def __init__(self, name: str):
        super().__init__(name)
        self.registered = False
        self.data = {}
    
    def register(self) -> None:
        """Implementation of the required register method."""
        self.registered = True

@pytest.fixture
def reset_plugins():
    """Fixture to reset the global PLUGINS list before and after tests."""
    original_plugins = PLUGINS.copy()
    PLUGINS.clear()
    yield
    PLUGINS.clear()
    PLUGINS.extend(original_plugins)

def test_plugin_registration(reset_plugins):
    plugin = TestPlugin("test-plugin")
    register_plugin(plugin)
    assert plugin in PLUGINS
    assert plugin.registered is True
    assert len(PLUGINS) == 1

def test_multiple_plugin_registration(reset_plugins):
    plugin1 = TestPlugin("plugin-1")
    plugin2 = TestPlugin("plugin-2")
    register_plugin(plugin1)
    register_plugin(plugin2)
    assert len(PLUGINS) == 2
    assert plugin1 in PLUGINS
    assert plugin2 in PLUGINS

def test_plugin_custom_functionality(reset_plugins):
    plugin = TestPlugin("data-plugin")
    register_plugin(plugin)
    plugin.data["theme"] = "dark"
    plugin.data["color"] = "#333"
    assert plugin.data["theme"] == "dark"
    assert plugin.data["color"] == "#333"

def test_abstract_plugin_registration():
    abstract_plugin = Plugin("abstract")
    with pytest.raises(NotImplementedError):
        abstract_plugin.register()