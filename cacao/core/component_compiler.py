"""
Component Compiler for Cacao Framework

This module provides the ComponentCompiler class that automatically discovers
and compiles modular components into a single cacao-components.js file.

The compiler implements Stage 2 of the two-stage loading architecture:
1. Stage 1: Static components in cacao-core.js
2. Stage 2: Dynamic components compiled into cacao-components.js

Usage:
    from cacao.core.component_compiler import ComponentCompiler
    
    compiler = ComponentCompiler()
    success = compiler.compile()
"""

import os
import json
import hashlib
import warnings
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class ComponentCompiler:
    """
    Compiles modular component JavaScript files into a single cacao-components.js file.
    
    The compiler discovers components by scanning for directories containing meta.json files,
    reads their JavaScript implementations, and wraps them with registration logic that
    extends the global window.CacaoCore.componentRenderers object.
    """
    
    def __init__(self,
                 components_dir: str = "cacao/ui/components",
                 output_path: str = "cacao/core/static/js/cacao-components.js",
                 css_output_path: str = "cacao/core/static/css/cacao-components.css"):
        """
        Initialize the ComponentCompiler.
        
        Args:
            components_dir: Directory to scan for modular components
            output_path: Path where the compiled cacao-components.js file should be written
            css_output_path: Path where the compiled cacao-components.css file should be written
        """
        self.components_dir = Path(components_dir)
        self.output_path = Path(output_path)
        self.css_output_path = Path(css_output_path)
        self.discovered_components: List[Dict] = []
        
    def discover_components(self) -> List[Dict]:
        """
        Discover all modular components using both folder-based and meta.json approaches.
        
        The discovery process:
        1. First uses folder-based discovery (new approach)
        2. Then falls back to meta.json discovery (deprecated)
        3. Ensures no duplicate components
        
        Returns:
            List of component metadata dictionaries
        """
        components = []
        component_names = set()  # Track discovered component names to avoid duplicates
        
        if not self.components_dir.exists():
            print(f"[ComponentCompiler] Components directory not found: {self.components_dir}")
            return components
            
        # 1. First try folder-based discovery (new approach)
        folder_components = self._discover_folder_based_components(self.components_dir)
        for component in folder_components:
            if component['name'] not in component_names:
                components.append(component)
                component_names.add(component['name'])
                
        # 2. Then try meta.json discovery (deprecated approach)
        meta_components = self._discover_meta_json_components()
        for component in meta_components:
            if component['name'] not in component_names:
                components.append(component)
                component_names.add(component['name'])
                
        self.discovered_components = components
        return components
        
    def _discover_meta_json_components(self) -> List[Dict]:
        """
        Discover components using the deprecated meta.json approach.
        
        Returns:
            List of component metadata dictionaries
        """
        components = []
        
        # Scan for component directories with meta.json
        for component_dir in self.components_dir.iterdir():
            if not component_dir.is_dir():
                continue
                
            meta_file = component_dir / "meta.json"
            if not meta_file.exists():
                continue
                
            # Issue deprecation warning
            warnings.warn(
                f"Component '{component_dir.name}' uses deprecated meta.json format. "
                f"Please migrate to folder-based naming convention: "
                f"rename files to '{component_dir.name.lower()}.js', '{component_dir.name.lower()}.css', etc.",
                DeprecationWarning,
                stacklevel=2
            )
            print(f"[ComponentCompiler] DEPRECATED: meta.json found in {component_dir.name} - please migrate to folder-based naming")
                
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta_data = json.load(f)
                    
                # Validate required fields
                if not all(key in meta_data for key in ['name', 'js']):
                    print(f"[ComponentCompiler] Invalid meta.json in {component_dir.name}: missing required fields")
                    continue
                    
                # Build full paths
                js_path = component_dir / meta_data['js']
                if not js_path.exists():
                    print(f"[ComponentCompiler] JavaScript file not found: {js_path}")
                    continue
                
                component_info = {
                    'name': meta_data['name'],
                    'js_path': js_path,
                    'directory': component_dir,
                    'meta_data': meta_data
                }
                
                # Extract category from parent folder if not root
                if component_dir.parent != self.components_dir:
                    component_info['category'] = component_dir.parent.name.lower()
                
                # Check for CSS file if specified in meta.json
                if 'css' in meta_data:
                    css_path = component_dir / meta_data['css']
                    if css_path.exists():
                        component_info['css_path'] = css_path
                        print(f"[ComponentCompiler] Found CSS for component: {meta_data['name']} -> {css_path.name}")
                    else:
                        print(f"[ComponentCompiler] CSS file not found: {css_path}")
                
                # Check for Python file if specified in meta.json
                if 'py' in meta_data:
                    py_path = component_dir / meta_data['py']
                    if py_path.exists():
                        component_info['py_path'] = py_path
                        print(f"[ComponentCompiler] Found Python for component: {meta_data['name']} -> {py_path.name}")
                    else:
                        print(f"[ComponentCompiler] Python file not found: {py_path}")
                
                components.append(component_info)
                print(f"[ComponentCompiler] Discovered meta.json component: {meta_data['name']}")
                
            except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                print(f"[ComponentCompiler] Error reading meta.json in {component_dir.name}: {e}")
                continue
                
        return components
        
    def _is_component_folder(self, folder_path: Path) -> bool:
        """
        Check if a folder is a component folder by looking for component files.
        
        Supports both naming conventions:
        1. New: component.js, component.css, component.py
        2. Legacy: {folder_name}.js, {folder_name}.css, {folder_name}.py
        
        Args:
            folder_path: Path to the folder to check
            
        Returns:
            True if the folder contains component files, False otherwise
        """
        if not folder_path.is_dir():
            return False
            
        folder_name = folder_path.name.lower()
        
        # Check for at least one file with valid extension
        for extension in ['.js', '.css', '.py']:
            # Check new naming convention first: component.{ext}
            component_file = folder_path / f"component{extension}"
            if component_file.exists():
                return True
                
            # Check legacy naming convention: {folder_name}.{ext}
            legacy_file = folder_path / f"{folder_name}{extension}"
            if legacy_file.exists():
                return True
                
        return False
        
    def _get_component_files(self, folder_path: Path) -> Dict[str, Path]:
        """
        Get component files from a folder based on naming convention.
        
        Supports both naming conventions:
        1. New: component.js, component.css, component.py
        2. Legacy: {folder_name}.js, {folder_name}.css, {folder_name}.py
        
        Args:
            folder_path: Path to the component folder
            
        Returns:
            Dictionary mapping file types to their paths
        """
        files = {}
        folder_name = folder_path.name.lower()
        
        # Check for each file type
        for extension in ['.js', '.css', '.py']:
            ext_name = extension[1:]  # Remove the dot from extension
            
            # Check new naming convention first: component.{ext}
            component_file = folder_path / f"component{extension}"
            if component_file.exists():
                files[ext_name] = component_file
                continue
                
            # Check legacy naming convention: {folder_name}.{ext}
            legacy_file = folder_path / f"{folder_name}{extension}"
            if legacy_file.exists():
                files[ext_name] = legacy_file
                
        return files
        
    def _extract_component_metadata(self, folder_path: Path) -> Dict:
        """
        Extract component metadata from folder structure.
        
        Args:
            folder_path: Path to the component folder
            
        Returns:
            Component metadata dictionary
        """
        folder_name = folder_path.name.lower()
        
        # Determine category from parent folder
        category = None
        parent_path = folder_path.parent
        if parent_path != self.components_dir:
            category = parent_path.name.lower()
            
        # Get component files
        component_files = self._get_component_files(folder_path)
        
        # Build component info
        component_info = {
            'name': folder_name,
            'directory': folder_path,
            'category': category
        }
        
        # Add file paths
        if 'js' in component_files:
            component_info['js_path'] = component_files['js']
        if 'css' in component_files:
            component_info['css_path'] = component_files['css']
        if 'py' in component_files:
            component_info['py_path'] = component_files['py']
            
        return component_info
        
    def _discover_folder_based_components(self, directory: Path) -> List[Dict]:
        """
        Recursively discover components using folder-based naming convention.
        
        Args:
            directory: Directory to scan for components
            
        Returns:
            List of component metadata dictionaries
        """
        components = []
        
        if not directory.exists():
            return components
            
        try:
            # Recursively walk through directories
            for item in directory.rglob('*'):
                if item.is_dir() and self._is_component_folder(item):
                    component_info = self._extract_component_metadata(item)
                    components.append(component_info)
                    print(f"[ComponentCompiler] Discovered folder-based component: {component_info['name']}")
                    
        except Exception as e:
            print(f"[ComponentCompiler] Error during folder-based discovery: {e}")
            
        return components
        
    def _read_component_js(self, js_path: Path) -> str:
        """
        Read the JavaScript content from a component file.
        
        Args:
            js_path: Path to the JavaScript file
            
        Returns:
            JavaScript content as string
        """
        try:
            with open(js_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"[ComponentCompiler] Error reading {js_path}: {e}")
            return ""
            
    def _read_component_css(self, css_path: Path) -> str:
        """
        Read the CSS content from a component file.
        
        Args:
            css_path: Path to the CSS file
            
        Returns:
            CSS content as string
        """
        try:
            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"[ComponentCompiler] Error reading {css_path}: {e}")
            return ""
            
    def _transform_function_calls(self, js_content: str) -> str:
        """
        Transform direct CacaoCore function calls to use proper namespacing.
        
        This method transforms direct function calls like:
        - renderChildren(el, children) -> window.CacaoCore.renderChildren(el, children)
        - applyContent(el, content) -> window.CacaoCore.applyContent(el, content)
        - renderComponent(component) -> window.CacaoCore.renderComponent(component)
        
        Args:
            js_content: Original JavaScript content
            
        Returns:
            Transformed JavaScript content with proper namespacing
        """
        import re
        
        # Define the whitelist of CacaoCore functions that need transformation
        cacao_core_functions = [
            'renderChildren',
            'applyContent',
            'renderComponent'
        ]
        
        transformed_content = js_content
        transformations_made = []
        
        for func_name in cacao_core_functions:
            # Pattern to match direct function calls (not method calls or already namespaced)
            # This pattern matches: functionName( but not object.functionName( or window.CacaoCore.functionName(
            pattern = r'(?<![\w.])\b' + re.escape(func_name) + r'\s*\('
            
            # Find all matches to track transformations
            matches = re.findall(pattern, transformed_content)
            if matches:
                transformations_made.extend([func_name] * len(matches))
                
                # Replace with namespaced version
                replacement = f'window.CacaoCore.{func_name}('
                transformed_content = re.sub(pattern, replacement, transformed_content)
        
        # Log transformations for debugging
        if transformations_made:
            print(f"[ComponentCompiler] Transformed function calls: {', '.join(transformations_made)}")
        
        return transformed_content
        
    def _validate_function_calls(self, js_content: str, component_name: str) -> List[str]:
        """
        Validate that all CacaoCore function calls are properly namespaced.
        
        Args:
            js_content: JavaScript content to validate
            component_name: Name of the component being validated
            
        Returns:
            List of validation warnings
        """
        import re
        
        warnings = []
        cacao_core_functions = ['renderChildren', 'applyContent', 'renderComponent']
        
        for func_name in cacao_core_functions:
            # Check for direct function calls that weren't properly transformed
            direct_call_pattern = r'(?<![\w.])\b' + re.escape(func_name) + r'\s*\('
            if re.search(direct_call_pattern, js_content):
                warnings.append(f"Component '{component_name}' contains direct call to '{func_name}()' - should use 'window.CacaoCore.{func_name}()'")
        
        return warnings
            
    def _aggregate_css(self, components: List[Dict]) -> str:
        """
        Aggregate CSS from all components into a single CSS string.
        
        Args:
            components: List of component metadata dictionaries
            
        Returns:
            Combined CSS content as string
        """
        css_parts = []
        
        for component in components:
            if 'css_path' in component:
                css_content = self._read_component_css(component['css_path'])
                if css_content:
                    # Determine component type for better logging
                    component_type = "folder-based" if 'category' in component else "meta.json"
                    
                    # Add component header comment with type info
                    css_parts.append(f"/* Component: {component['name']} ({component_type}) */")
                    css_parts.append(css_content)
                    css_parts.append("")  # Add empty line between components
                    
                    print(f"[ComponentCompiler] Added CSS for {component_type} component: {component['name']}")
                else:
                    component_type = "folder-based" if 'category' in component else "meta.json"
                    print(f"[ComponentCompiler] Warning: Empty CSS content for {component_type} component: {component['name']}")
                    
        return '\n'.join(css_parts).strip()
            
    def _wrap_component(self, component_info: Dict) -> str:
        """
        Wrap a component's JavaScript with registration logic.
        Ensures that any errors in component registration are caught
        and do not break the overall application.
        """
        # Safely get component name
        name = component_info.get('name', 'UnknownComponent')
        try:
            # Skip if no JS path provided
            if 'js_path' not in component_info:
                comp_type = "folder-based" if 'category' in component_info else "meta.json"
                print(f"[ComponentCompiler] Skipping {comp_type} component '{name}' - no JavaScript file found")
                return ""

            # Read JS content with its own try/except
            try:
                js_content = self._read_component_js(component_info['js_path'])
            except Exception as e:
                print(f"[ComponentCompiler] Error reading JS for '{name}': {e}")
                return ""

            if not js_content:
                comp_type = "folder-based" if 'category' in component_info else "meta.json"
                print(f"[ComponentCompiler] Failed to read JavaScript for {comp_type} component: {name}")
                return ""

            # Transform function calls safely
            try:
                js_content = self._transform_function_calls(js_content)
            except Exception as e:
                print(f"[ComponentCompiler] Error transforming JS for '{name}': {e}")

            # Validate function calls safely
            try:
                validation_warnings = self._validate_function_calls(js_content, name)
                for warning in validation_warnings:
                    print(f"[ComponentCompiler] WARNING: {warning}")
            except Exception as e:
                print(f"[ComponentCompiler] Error validating JS for '{name}': {e}")

            # Helper to convert hyphens to camelCase
            def to_camel_case(text):
                parts = text.split('-')
                return parts[0] + ''.join(word.capitalize() for word in parts[1:])

            js_var_name = to_camel_case(name) if '-' in name else name

            import re
            is_class = js_content.strip().startswith('class ')
            if is_class:
                match = re.match(r'class\s+([A-Za-z0-9_]+)', js_content.strip())
                class_name = match.group(1) if match else 'UnknownClass'

                wrapper = f"""
// Auto-generated component: {name}
(function(){{
    try {{
        {js_content}

        // Ensure the global registry exists
        if (!window.CacaoCore) {{
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {{}};
        }}
        if (!window.CacaoCore.componentRenderers) {{
            window.CacaoCore.componentRenderers = {{}};
        }}

        // Register the class directly
        window.CacaoCore.componentRenderers['{name}'] = {class_name};
    }} catch (error) {{
        console.error('[CacaoComponents] Error registering component: {name}', error);
    }}
}})();
"""
            else:
                wrapper = f"""
// Auto-generated component: {name}
(function(){{
    try {{
        const {js_var_name}Renderer = {js_content};

        // Ensure the global registry exists
        if (!window.CacaoCore) {{
            console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
            window.CacaoCore = {{}};
        }}
        if (!window.CacaoCore.componentRenderers) {{
            window.CacaoCore.componentRenderers = {{}};
        }}

        // Register the renderer function
        window.CacaoCore.componentRenderers['{name}'] = {js_var_name}Renderer;
    }} catch (error) {{
        console.error('[CacaoComponents] Error registering component: {name}', error);
    }}
}})();
"""
            return wrapper.strip()

        except Exception as e:
            print(f"[ComponentCompiler] Unexpected error wrapping component '{name}': {e}")
            return ""

    def _generate_file_header(self) -> str:
        """
        Generate the header comment for the compiled file.
        
        Returns:
            Header comment as string
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        component_count = len(self.discovered_components)
        
        header = f"""/*
 * Auto-generated Cacao Components
 * Generated on: {timestamp}
 * Components: {component_count}
 *
 * This file extends window.CacaoCore.componentRenderers with compiled components.
 * It must be loaded AFTER cacao-core.js to ensure the global registry exists.
 */
"""
        return header
        
    def _generate_css_header(self) -> str:
        """
        Generate the header comment for the compiled CSS file.
        
        Returns:
            CSS header comment as string
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        css_component_count = len([c for c in self.discovered_components if 'css_path' in c])
        
        header = f"""/*
 * Auto-generated Cacao Component Styles
 * Generated on: {timestamp}
 * Components with CSS: {css_component_count}
 *
 * This file contains compiled CSS from all modular components.
 * Include this file in your HTML to apply component-specific styles.
 */
"""
        return header
        
    def _should_rebuild(self) -> bool:
        """
        Check if the compiled files need to be rebuilt.
        
        Returns:
            True if rebuild is needed, False otherwise
        """
        if not self.output_path.exists() or not self.css_output_path.exists():
            return True
            
        js_output_mtime = self.output_path.stat().st_mtime
        css_output_mtime = self.css_output_path.stat().st_mtime
        min_output_mtime = min(js_output_mtime, css_output_mtime)
        
        # Check if any component files are newer than the output
        for component in self.discovered_components:
            # Check JavaScript files if they exist
            if 'js_path' in component and component['js_path'].stat().st_mtime > min_output_mtime:
                return True
            # Check meta.json files if they exist (for meta.json-based components)
            if 'meta_path' in component and component['meta_path'].stat().st_mtime > min_output_mtime:
                return True
            # Check CSS files if they exist
            if 'css_path' in component and component['css_path'].stat().st_mtime > min_output_mtime:
                return True
            # Check Python files if they exist
            if 'py_path' in component and component['py_path'].stat().st_mtime > min_output_mtime:
                return True
                
        return False
        
    def compile(self, force: bool = False, verbose: bool = False) -> bool:
        """
        Compile all discovered components into cacao-components.js.
        
        Args:
            force: If True, rebuild even if files haven't changed
            verbose: If True, show detailed compilation information
            
        Returns:
            True if compilation succeeded, False otherwise
        """
        try:
            # Discover components
            components = self.discover_components()
            
            if not components:
                if verbose:
                    print("[ComponentCompiler] No modular components found")
                # Create empty compiled files to prevent loading errors
                self._create_empty_compiled_file()
                self._create_empty_css_file()
                return True
                
            # Check if rebuild is needed
            if not force and not self._should_rebuild():
                if verbose:
                    print("[ComponentCompiler] Components are up to date, skipping compilation")
                return True
                
            if verbose:
                print(f"[ComponentCompiler] Compiling {len(components)} components...")
                
            # Generate JS compiled content
            compiled_parts = [self._generate_file_header()]
            
            for component in components:
                wrapped_js = self._wrap_component(component)
                if wrapped_js:
                    compiled_parts.append(wrapped_js)
                    if verbose:
                        print(f"[ComponentCompiler] Compiled JS: {component['name']}")
                else:
                    print(f"[ComponentCompiler] Failed to compile JS: {component['name']}")
                    
            # Write compiled JS file
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(compiled_parts))
                f.write('\n')
                
            if verbose:
                print(f"[ComponentCompiler] Successfully compiled JS to: {self.output_path}")
                
            # Compile and write CSS
            try:
                css_content = self._aggregate_css(components)
                css_parts = [self._generate_css_header()]
                
                if css_content:
                    css_parts.append(css_content)
                    if verbose:
                        css_count = len([c for c in components if 'css_path' in c])
                        print(f"[ComponentCompiler] Aggregated CSS from {css_count} components")
                else:
                    css_parts.append("/* No component CSS found */")
                    if verbose:
                        print("[ComponentCompiler] No component CSS files found")
                
                # Write compiled CSS file
                self.css_output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(self.css_output_path, 'w', encoding='utf-8') as f:
                    f.write('\n\n'.join(css_parts))
                    f.write('\n')
                    
                if verbose:
                    print(f"[ComponentCompiler] Successfully compiled CSS to: {self.css_output_path}")
                    
            except Exception as e:
                print(f"[ComponentCompiler] CSS compilation failed: {e}")
                # Still return True since JS compilation succeeded
                print("[ComponentCompiler] Continuing with JS-only compilation")
                
            return True
            
        except Exception as e:
            print(f"[ComponentCompiler] Compilation failed: {e}")
            return False
            
    def _create_empty_compiled_file(self):
        """Create an empty compiled file with just the header to prevent loading errors."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        header = f"""/*
 * Auto-generated Cacao Components
 * Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 * Components: 0
 *
 * No modular components found. This file exists to prevent loading errors.
 */

// Empty compiled components file - no modular components to register
console.log('[CacaoComponents] No modular components found');
"""
        
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(header)
    def _create_empty_css_file(self):
        """Create an empty CSS file with just the header to prevent loading errors."""
        self.css_output_path.parent.mkdir(parents=True, exist_ok=True)
        
        header = f"""/*
 * Auto-generated Cacao Component Styles
 * Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
 * Components with CSS: 0
 *
 * No component CSS found. This file exists to prevent loading errors.
 */

/* Empty compiled CSS file - no component styles to include */
"""
        
        with open(self.css_output_path, 'w', encoding='utf-8') as f:
            f.write(header)



def compile_components(components_dir: str = "cacao/ui/components",
                      output_path: str = "cacao/core/static/js/cacao-components.js",
                      css_output_path: str = "cacao/core/static/css/cacao-components.css",
                      force: bool = False,
                      verbose: bool = False) -> bool:
    """
    Convenience function to compile components.
    
    Args:
        components_dir: Directory to scan for modular components
        output_path: Path where the compiled cacao-components.js file should be written
        css_output_path: Path where the compiled cacao-components.css file should be written
        force: If True, rebuild even if files haven't changed
        verbose: If True, show detailed compilation information
        
    Returns:
        True if compilation succeeded, False otherwise
    """
    compiler = ComponentCompiler(components_dir, output_path, css_output_path)
    return compiler.compile(force=force, verbose=verbose)