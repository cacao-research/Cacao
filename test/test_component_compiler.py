"""
Test suite for the ComponentCompiler function transformation system.
"""
import pytest
import tempfile
import os
from pathlib import Path
from cacao.core.component_compiler import ComponentCompiler


class TestComponentCompiler:
    """Test cases for ComponentCompiler function transformation."""
    
    def test_function_transformation(self):
        """Test that CacaoCore functions are properly transformed."""
        compiler = ComponentCompiler()
        
        # Test input with direct function calls
        input_js = """
        (component) => {
            const el = document.createElement("div");
            if (component.props?.content) {
                applyContent(el, component.props.content);
            }
            if (component.children) {
                renderChildren(el, component.children);
            }
            renderComponent(childComponent);
            return el;
        }
        """
        
        # Expected output with transformed function calls
        expected_calls = [
            "window.CacaoCore.applyContent(el, component.props.content)",
            "window.CacaoCore.renderChildren(el, component.children)",
            "window.CacaoCore.renderComponent(childComponent)"
        ]
        
        # Apply transformation
        result = compiler._transform_function_calls(input_js)
        
        # Verify all expected transformations are present
        for expected_call in expected_calls:
            assert expected_call in result, f"Expected '{expected_call}' not found in transformed code"
        
        # Verify original direct calls are removed
        assert "applyContent(" not in result.replace("window.CacaoCore.applyContent(", "")
        assert "renderChildren(" not in result.replace("window.CacaoCore.renderChildren(", "")
        assert "renderComponent(" not in result.replace("window.CacaoCore.renderComponent(", "")
    
    def test_no_false_positives(self):
        """Test that method calls and already namespaced calls are not transformed."""
        compiler = ComponentCompiler()
        
        # Test input with method calls and already namespaced calls
        input_js = """
        (component) => {
            const el = document.createElement("div");
            obj.renderChildren(el, children);  // Method call - should not transform
            window.CacaoCore.applyContent(el, content);  // Already namespaced - should not transform
            myFunction.applyContent(data);  // Method call - should not transform
            return el;
        }
        """
        
        # Apply transformation
        result = compiler._transform_function_calls(input_js)
        
        # Verify no unwanted transformations occurred
        assert "obj.renderChildren(el, children)" in result
        assert "window.CacaoCore.applyContent(el, content)" in result
        assert "myFunction.applyContent(data)" in result
        
        # Should not have double-transformed anything
        assert "window.CacaoCore.window.CacaoCore." not in result
    
    def test_validation_system(self):
        """Test that validation system detects missing namespacing."""
        compiler = ComponentCompiler()
        
        # Test input with direct function calls (should generate warnings)
        input_js = """
        (component) => {
            renderChildren(el, children);
            applyContent(el, content);
            return el;
        }
        """
        
        # Apply validation
        warnings = compiler._validate_function_calls(input_js, "test-component")
        
        # Should generate warnings for each direct call
        assert len(warnings) == 2
        assert "renderChildren" in warnings[0]
        assert "applyContent" in warnings[1]
        assert "test-component" in warnings[0]
    
    def test_edge_cases(self):
        """Test edge cases in function transformation."""
        compiler = ComponentCompiler()
        
        # Test with whitespace variations
        input_js = """
        renderChildren  (el, children);
        applyContent\t(el, content);
        renderComponent\n(component);
        """
        
        result = compiler._transform_function_calls(input_js)
        
        # Should handle whitespace variations correctly by normalizing them
        assert "window.CacaoCore.renderChildren(el, children)" in result
        assert "window.CacaoCore.applyContent(el, content)" in result
        assert "window.CacaoCore.renderComponent(component)" in result


if __name__ == "__main__":
    # Run basic tests
    test = TestComponentCompiler()
    test.test_function_transformation()
    test.test_no_false_positives()
    test.test_validation_system()
    test.test_edge_cases()
    print("All tests passed!")