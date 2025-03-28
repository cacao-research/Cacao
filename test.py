import pytest
import sys
from cacao import State, Component, mix
from cacao.core.server import CacaoServer

@pytest.fixture
def server():
    """Fixture for creating a test server instance"""
    server = CacaoServer(testing=True)
    yield server
    server.shutdown()

@pytest.fixture
def test_state():
    """Fixture for creating a test state instance"""
    return State(initial_value=0)

@pytest.fixture
def test_component():
    """Fixture for creating a basic test component"""
    class TestComponent(Component):
        def render(self):
            return {
                "type": "div",
                "props": {"content": "Test Component"}
            }
    return TestComponent()

def test_imports():
    """Verify core imports are working"""
    assert State is not None
    assert Component is not None
    assert mix is not None

if __name__ == "__main__":
    """
    Main test runner - executes pytest with specified arguments when this file is run directly
    """
    print("🍫 Cacao Test Runner 🍫")
    print("=======================")
    
    # Default arguments: run all tests and filter warnings
    args = ["test/", "-v", "--no-header", "-p", "no:warnings"]
    
    # Check for specific test files or patterns
    if len(sys.argv) > 1:
        # If additional arguments are provided, use them instead of default "test/" path
        args = sys.argv[1:] + ["-v", "--no-header", "-p", "no:warnings"]
    
    print(f"Running tests: {' '.join(arg for arg in args if not arg.startswith('-'))}\n")
    
    # Run pytest with specified arguments
    exit_code = pytest.main(args)
    
    # Summary based on exit code
    if exit_code == 0:
        print("\n✅ All tests passed successfully!")
    else:
        print(f"\n❌ Tests completed with failures. Exit code: {exit_code}")
    
    sys.exit(exit_code)