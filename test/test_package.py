#!/usr/bin/env python3
"""
Comprehensive test script for Cacao framework package build validation.
This script tests for missing imports, packaging issues, and component availability.
"""

import sys
import os
import traceback
import importlib
import inspect
from pathlib import Path
import json
from datetime import datetime

# Test results tracking
test_results = {
    "timestamp": datetime.now().isoformat(),
    "python_version": sys.version,
    "passed": [],
    "failed": [],
    "warnings": [],
    "total_tests": 0,
    "passed_tests": 0,
    "failed_tests": 0
}

def log_test(test_name, status, message="", error=None):
    """Log test results"""
    test_results["total_tests"] += 1
    
    result = {
        "test": test_name,
        "status": status,
        "message": message,
        "error": str(error) if error else None
    }
    
    if status == "PASSED":
        test_results["passed"].append(result)
        test_results["passed_tests"] += 1
        print(f"✓ {test_name}: {message}")
    elif status == "FAILED":
        test_results["failed"].append(result)
        test_results["failed_tests"] += 1
        print(f"✗ {test_name}: {message}")
        if error:
            print(f"  Error: {error}")
    elif status == "WARNING":
        test_results["warnings"].append(result)
        print(f"⚠ {test_name}: {message}")

def test_basic_imports():
    """Test basic package imports"""
    print("\n=== Testing Basic Imports ===")
    
    # Test main package import
    try:
        import cacao
        log_test("Basic Import", "PASSED", "Successfully imported cacao")
    except Exception as e:
        log_test("Basic Import", "FAILED", "Failed to import cacao", e)
        return False
    
    # Test core modules
    core_modules = [
        'cacao.core',
        'cacao.core.app',
        'cacao.core.server',
        'cacao.core.state',
        'cacao.core.theme',
        'cacao.ui',
        'cacao.ui.types',
        'cacao.utilities',
        'cacao.cli',
        'cacao.extensions'
    ]
    
    for module_name in core_modules:
        try:
            importlib.import_module(module_name)
            log_test(f"Import {module_name}", "PASSED", f"Successfully imported {module_name}")
        except Exception as e:
            log_test(f"Import {module_name}", "FAILED", f"Failed to import {module_name}", e)
    
    return True

def test_component_imports():
    """Test UI component imports"""
    print("\n=== Testing Component Imports ===")
    
    # Test component package
    try:
        import cacao.ui.components
        log_test("Components Package", "PASSED", "Successfully imported cacao.ui.components")
    except Exception as e:
        log_test("Components Package", "FAILED", "Failed to import cacao.ui.components", e)
        return False
    
    # Test specific component categories
    component_categories = [
        'cacao.ui.components.data',
        'cacao.ui.components.forms',
        'cacao.ui.components.navigation',
        'cacao.ui.components.ui'
    ]
    
    for category in component_categories:
        try:
            importlib.import_module(category)
            log_test(f"Import {category}", "PASSED", f"Successfully imported {category}")
        except Exception as e:
            log_test(f"Import {category}", "FAILED", f"Failed to import {category}", e)
    
    return True

def test_static_assets():
    """Test static asset availability"""
    print("\n=== Testing Static Assets ===")
    
    try:
        import cacao
        cacao_path = Path(cacao.__file__).parent
        
        # Check for core static assets
        static_paths = [
            cacao_path / "core" / "static" / "js" / "cacao-core.js",
            cacao_path / "core" / "static" / "js" / "cacao-components.js",
            cacao_path / "core" / "static" / "css" / "icon-styles.css",
            cacao_path / "core" / "static" / "icons" / "cacao.svg",
            cacao_path / "core" / "static" / "index.html"
        ]
        
        for asset_path in static_paths:
            if asset_path.exists():
                log_test(f"Static Asset {asset_path.name}", "PASSED", f"Found {asset_path.name}")
            else:
                log_test(f"Static Asset {asset_path.name}", "FAILED", f"Missing {asset_path}")
        
        # Check for UI component assets
        ui_components_path = cacao_path / "ui" / "components"
        if ui_components_path.exists():
            js_files = list(ui_components_path.rglob("*.js"))
            css_files = list(ui_components_path.rglob("*.css"))
            
            if js_files:
                log_test("Component JS Files", "PASSED", f"Found {len(js_files)} JS files")
            else:
                log_test("Component JS Files", "WARNING", "No JS files found in components")
            
            if css_files:
                log_test("Component CSS Files", "PASSED", f"Found {len(css_files)} CSS files")
            else:
                log_test("Component CSS Files", "WARNING", "No CSS files found in components")
        else:
            log_test("UI Components Path", "FAILED", "UI components directory not found")
            
    except Exception as e:
        log_test("Static Assets", "FAILED", "Failed to check static assets", e)

def test_theme_imports():
    """Test theme imports"""
    print("\n=== Testing Theme Imports ===")
    
    try:
        import cacao.core.theme
        log_test("Theme Module", "PASSED", "Successfully imported cacao.core.theme")
        
        # Check if themes directory exists
        import cacao
        cacao_path = Path(cacao.__file__).parent
        themes_path = cacao_path / "ui" / "themes"
        
        if themes_path.exists():
            theme_files = list(themes_path.glob("*.py"))
            if theme_files:
                log_test("Theme Files", "PASSED", f"Found {len(theme_files)} theme files")
            else:
                log_test("Theme Files", "WARNING", "No theme files found")
        else:
            log_test("Themes Directory", "WARNING", "Themes directory not found")
            
    except Exception as e:
        log_test("Theme Imports", "FAILED", "Failed to test theme imports", e)

def test_cli_functionality():
    """Test CLI functionality"""
    print("\n=== Testing CLI Functionality ===")
    
    try:
        from cacao.cli import commands
        log_test("CLI Commands", "PASSED", "Successfully imported CLI commands")
        
        # Test CLI templates
        import cacao
        cacao_path = Path(cacao.__file__).parent
        templates_path = cacao_path / "cli" / "templates"
        
        if templates_path.exists():
            template_files = list(templates_path.rglob("*"))
            if template_files:
                log_test("CLI Templates", "PASSED", f"Found {len(template_files)} template files")
            else:
                log_test("CLI Templates", "WARNING", "No template files found")
        else:
            log_test("CLI Templates", "FAILED", "CLI templates directory not found")
            
    except Exception as e:
        log_test("CLI Functionality", "FAILED", "Failed to test CLI functionality", e)

def test_example_execution():
    """Test example script execution"""
    print("\n=== Testing Example Script Execution ===")
    
    # Test basic app creation
    try:
        import cacao
        app = cacao.App()
        log_test("App Creation", "PASSED", "Successfully created Cacao app instance")
        
        # Test basic state functionality
        from cacao.core.state import State
        state = State()
        log_test("State Creation", "PASSED", "Successfully created State instance")
        
    except Exception as e:
        log_test("Example Execution", "FAILED", "Failed to execute basic example", e)

def test_package_metadata():
    """Test package metadata"""
    print("\n=== Testing Package Metadata ===")
    
    try:
        import cacao
        
        # Check if package has version
        if hasattr(cacao, '__version__'):
            log_test("Package Version", "PASSED", f"Version: {cacao.__version__}")
        else:
            log_test("Package Version", "WARNING", "No version attribute found")
        
        # Check package path
        package_path = Path(cacao.__file__).parent
        log_test("Package Path", "PASSED", f"Located at: {package_path}")
        
        # Check package structure
        expected_dirs = ['core', 'ui', 'cli', 'extensions', 'utilities']
        missing_dirs = []
        
        for dir_name in expected_dirs:
            if not (package_path / dir_name).exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            log_test("Package Structure", "FAILED", f"Missing directories: {missing_dirs}")
        else:
            log_test("Package Structure", "PASSED", "All expected directories found")
            
    except Exception as e:
        log_test("Package Metadata", "FAILED", "Failed to check package metadata", e)

def test_extensions():
    """Test extensions functionality"""
    print("\n=== Testing Extensions ===")
    
    try:
        from cacao.extensions import react_extension
        log_test("React Extension", "PASSED", "Successfully imported react extension")
        
        # Test plugins
        from cacao.extensions.plugins import pandas_table
        log_test("Pandas Table Plugin", "PASSED", "Successfully imported pandas table plugin")
        
    except Exception as e:
        log_test("Extensions", "FAILED", "Failed to test extensions", e)

def save_test_results():
    """Save test results to file"""
    try:
        os.makedirs("test_results", exist_ok=True)
        
        with open("test_results/test_results.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        # Create summary report
        with open("test_results/test_summary.txt", "w") as f:
            f.write("CACAO PACKAGE TEST SUMMARY\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Timestamp: {test_results['timestamp']}\n")
            f.write(f"Python Version: {test_results['python_version']}\n\n")
            f.write(f"Total Tests: {test_results['total_tests']}\n")
            f.write(f"Passed: {test_results['passed_tests']}\n")
            f.write(f"Failed: {test_results['failed_tests']}\n")
            f.write(f"Warnings: {len(test_results['warnings'])}\n\n")
            
            if test_results['failed']:
                f.write("FAILED TESTS:\n")
                for failure in test_results['failed']:
                    f.write(f"- {failure['test']}: {failure['message']}\n")
                    if failure['error']:
                        f.write(f"  Error: {failure['error']}\n")
                f.write("\n")
            
            if test_results['warnings']:
                f.write("WARNINGS:\n")
                for warning in test_results['warnings']:
                    f.write(f"- {warning['test']}: {warning['message']}\n")
                f.write("\n")
        
        print(f"\nTest results saved to test_results/")
        
    except Exception as e:
        print(f"Failed to save test results: {e}")

def main():
    """Main test runner"""
    print("CACAO PACKAGE BUILD VALIDATION")
    print("=" * 40)
    print(f"Python version: {sys.version}")
    print(f"Test mode: {os.environ.get('CACAO_TEST_MODE', 'false')}")
    print()
    
    # Run all tests
    test_basic_imports()
    test_component_imports()
    test_static_assets()
    test_theme_imports()
    test_cli_functionality()
    test_example_execution()
    test_package_metadata()
    test_extensions()
    
    # Print summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    print(f"Total tests: {test_results['total_tests']}")
    print(f"Passed: {test_results['passed_tests']}")
    print(f"Failed: {test_results['failed_tests']}")
    print(f"Warnings: {len(test_results['warnings'])}")
    
    if test_results['failed_tests'] > 0:
        print("\nFAILED TESTS:")
        for failure in test_results['failed']:
            print(f"- {failure['test']}: {failure['message']}")
    
    if test_results['warnings']:
        print("\nWARNINGS:")
        for warning in test_results['warnings']:
            print(f"- {warning['test']}: {warning['message']}")
    
    # Save results
    save_test_results()
    
    # Exit with appropriate code
    if test_results['failed_tests'] > 0:
        print("\n❌ Some tests failed. Package may have issues.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Package is ready for distribution.")
        sys.exit(0)

if __name__ == "__main__":
    main()