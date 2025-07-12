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
        Discover all modular components by scanning for meta.json files.
        
        Returns:
            List of component metadata dictionaries
        """
        components = []
        
        if not self.components_dir.exists():
            print(f"[ComponentCompiler] Components directory not found: {self.components_dir}")
            return components
            
        # Scan for component directories
        for component_dir in self.components_dir.iterdir():
            if not component_dir.is_dir():
                continue
                
            meta_file = component_dir / "meta.json"
            if not meta_file.exists():
                continue
                
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
                    'meta_path': meta_file,
                    'directory': component_dir,
                    'meta_data': meta_data
                }
                
                # Check for CSS file if specified in meta.json
                if 'css' in meta_data:
                    css_path = component_dir / meta_data['css']
                    if css_path.exists():
                        component_info['css_path'] = css_path
                        print(f"[ComponentCompiler] Found CSS for component: {meta_data['name']} -> {css_path.name}")
                    else:
                        print(f"[ComponentCompiler] CSS file not found: {css_path}")
                
                components.append(component_info)
                print(f"[ComponentCompiler] Discovered component: {meta_data['name']}")
                
            except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                print(f"[ComponentCompiler] Error reading meta.json in {component_dir.name}: {e}")
                continue
                
        self.discovered_components = components
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
                    # Add component header comment
                    css_parts.append(f"/* Component: {component['name']} */")
                    css_parts.append(css_content)
                    css_parts.append("")  # Add empty line between components
                    
        return '\n'.join(css_parts).strip()
            
    def _wrap_component(self, component_info: Dict) -> str:
        """
        Wrap a component's JavaScript with registration logic.
        
        Args:
            component_info: Component metadata dictionary
            
        Returns:
            Wrapped JavaScript code as string
        """
        name = component_info['name']
        js_content = self._read_component_js(component_info['js_path'])
        
        if not js_content:
            return ""
            
        # Convert component name to valid JavaScript identifier
        # Convert hyphens to camelCase (e.g., "enhanced-table" -> "enhancedTable")
        def to_camel_case(text):
            parts = text.split('-')
            return parts[0] + ''.join(word.capitalize() for word in parts[1:])
        
        # Generate valid JavaScript variable name
        js_var_name = to_camel_case(name) if '-' in name else name
        
        # Generate both camelCase and lowercase keys for maximum compatibility
        component_key_camel = name
        component_key_lower = name.lower()  # enhancedtable
        
        wrapper = f"""
// Auto-generated component: {name}
(function() {{
    // Component renderer function
    const {js_var_name}Renderer = {js_content};
    
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {{
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {{}};
    }}
    if (!window.CacaoCore.componentRenderers) {{
        window.CacaoCore.componentRenderers = {{}};
    }}
    
    // Extend the existing registry with the new component (both camelCase and lowercase for compatibility)
    window.CacaoCore.componentRenderers['{name}'] = {js_var_name}Renderer;
}})();
"""
        return wrapper.strip()
        
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
            if component['js_path'].stat().st_mtime > min_output_mtime:
                return True
            if component['meta_path'].stat().st_mtime > min_output_mtime:
                return True
            # Check CSS files if they exist
            if 'css_path' in component and component['css_path'].stat().st_mtime > min_output_mtime:
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