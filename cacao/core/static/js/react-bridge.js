/*
  react-bridge.js
  Provides integration between Cacao and React components from npm packages.
  This script dynamically loads React, ReactDOM, and requested npm packages.
*/

(function() {
    // Keep track of loaded packages to avoid duplicate loading
    const loadedPackages = new Set();
    const loadedCSS = new Set();
    const mountedComponents = new Map();
    
    // Function to load a script dynamically
    function loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.async = true;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    // Function to load CSS dynamically
    function loadCSS(href) {
        return new Promise((resolve) => {
            if (loadedCSS.has(href)) {
                resolve();
                return;
            }
            
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = resolve;
            link.onerror = resolve; // Continue even if CSS fails to load
            document.head.appendChild(link);
            loadedCSS.add(href);
        });
    }
    
    // Function to load React and ReactDOM if not already loaded
    async function ensureReactLoaded() {
        if (window.React && window.ReactDOM) {
            return;
        }
        
        console.log("[ReactBridge] Loading React and ReactDOM");
        
        try {
            // Load React and ReactDOM from CDN
            await loadScript("https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js");
            await loadScript("https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js");
            
            console.log("[ReactBridge] React and ReactDOM loaded successfully");
        } catch (error) {
            console.error("[ReactBridge] Failed to load React:", error);
            throw new Error("Failed to load React libraries");
        }
    }
    
    // Function to load an npm package
    async function loadPackage(packageName, version = "latest", cdn = "https://cdn.jsdelivr.net/npm") {
        const packageKey = `${packageName}@${version}`;

        if (loadedPackages.has(packageKey)) {
            // Special handling for codemirror v5 which attaches to window.CodeMirror
            return packageName === 'codemirror' ? window.CodeMirror : window[packageName];
        }

        console.log(`[ReactBridge] Loading package: ${packageKey}`);
        let packageUrl = `${cdn}/${packageName}@${version}`;
        let scriptUrl;

        // Special handling for codemirror v5 path
        if (packageName === 'codemirror' && version.startsWith('5.')) {
            scriptUrl = `${packageUrl}/lib/codemirror.js`;
        } else {
            // Default paths for other packages
            scriptUrl = `${packageUrl}/dist/umd/${packageName}.min.js`; // Try UMD first
        }

        try {
            await loadScript(scriptUrl);
            loadedPackages.add(packageKey);
            console.log(`[ReactBridge] Package loaded: ${packageKey} from ${scriptUrl}`);
            // Special handling for codemirror v5 which attaches to window.CodeMirror
            return packageName === 'codemirror' ? window.CodeMirror : window[packageName];
        } catch (error) {
            console.warn(`[ReactBridge] Failed to load ${scriptUrl}:`, error);

            // Try alternative path if the first one failed (and not codemirror v5)
            if (!(packageName === 'codemirror' && version.startsWith('5.'))) {
                scriptUrl = `${packageUrl}/dist/${packageName}.min.js`;
                console.log(`[ReactBridge] Trying alternative path: ${scriptUrl}`);
                try {
                    await loadScript(scriptUrl);
                    loadedPackages.add(packageKey);
                    console.log(`[ReactBridge] Package loaded (alternative path): ${packageKey} from ${scriptUrl}`);
                    return window[packageName]; // Assume standard window[packageName] for alternatives
                } catch (altError) {
                    console.error(`[ReactBridge] Failed to load package ${packageKey} (alternative path):`, altError);
                    throw new Error(`Failed to load package: ${packageName}`);
                }
            } else {
                 console.error(`[ReactBridge] Failed to load package ${packageKey}:`, error);
                 throw new Error(`Failed to load package: ${packageName}`);
            }
        }
    }
    
    // Function to render a React component
    async function renderReactComponent(config) {
        const { id, package: packageName, component: componentName, props, version, css, cdn } = config;
        
        // Create container if it doesn't exist
        let container = document.getElementById(id);
        if (!container) {
            container = document.createElement('div');
            container.id = id;
            document.getElementById('app').appendChild(container);
        }
        
        try {
            // Ensure React is loaded
            await ensureReactLoaded();
            
            // Load CSS files if specified
            if (css && Array.isArray(css)) {
                for (const cssFile of css) {
                    const cssUrl = `${cdn}/${packageName}@${version}/${cssFile}`;
                    await loadCSS(cssUrl);
                }
            }
            
            // Load the package
            const packageModule = await loadPackage(packageName, version, cdn);
            
            if (!packageModule) {
                throw new Error(`Package ${packageName} loaded but not available in window scope`);
            }
            
            // Get the component from the package
            // Adjust component access for codemirror v5 vs others
            const Component = (packageName === 'codemirror' && version.startsWith('5.'))
                              ? packageModule // It's directly window.CodeMirror
                              : packageModule[componentName];
            
            if (!Component) {
                throw new Error(`Component ${componentName} not found in package ${packageName}`);
            }
            
            // Special handling for CodeMirror v5
            if (packageName === 'codemirror' && version.startsWith('5.')) {
                console.log(`[ReactBridge] Initializing CodeMirror v5 directly`);
                // Ensure the container is empty before initializing
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                // Instantiate CodeMirror directly
                const editor = new Component(container, props.options); // Component is window.CodeMirror here
                if (props.value) {
                    editor.setValue(props.value);
                }
                // Store reference for potential future unmounting (though CM5 doesn't have a clean unmount)
                mountedComponents.set(id, { container, packageName, componentName, instance: editor });
            } else {
                // Standard React component rendering
                console.log(`[ReactBridge] Rendering React component: ${componentName} from ${packageName}`);
                const reactElement = React.createElement(Component, props);
                ReactDOM.render(reactElement, container);
                // Store reference to unmount later if needed
                mountedComponents.set(id, { container, packageName, componentName });
            }
            
            return true;
        } catch (error) {
            console.error(`[ReactBridge] Error rendering component:`, error);
            // Display error message in the container
            container.innerHTML = `<div class="error">Error loading React component: ${error.message}</div>`;
            return false;
        }
    }
    
    // Function to unmount a React component
    function unmountReactComponent(id) {
        if (mountedComponents.has(id)) {
            const { container } = mountedComponents.get(id);
            if (window.ReactDOM && container) {
                ReactDOM.unmountComponentAtNode(container);
                mountedComponents.delete(id);
                return true;
            }
        }
        return false;
    }
    
    // Extend the CacaoCore renderer to handle React components
    if (window.CacaoCore) {
        // Store the original renderComponent function
        const originalRenderComponent = window.CacaoCore.renderComponent || 
                                       (typeof renderComponent === 'function' ? renderComponent : null);
        
        if (originalRenderComponent) {
            // Override the renderComponent function
            window.CacaoCore.renderComponent = function(component) {
                if (component && component.type === 'react-component') {
                    const container = document.createElement('div');
                    container.id = component.props.id;
                    container.className = 'react-component-container';
                    
                    // Add loading indicator
                    const loadingDiv = document.createElement('div');
                    loadingDiv.className = 'react-loading';
                    loadingDiv.textContent = `Loading ${component.props.package}...`;
                    container.appendChild(loadingDiv);
                    
                    // Render the React component asynchronously
                    setTimeout(() => {
                        renderReactComponent(component.props).then(success => {
                            if (success) {
                                loadingDiv.remove();
                            }
                        });
                    }, 0);
                    
                    return container;
                }
                
                // Fall back to the original renderer for non-React components
                return originalRenderComponent(component);
            };
        }
    }
    
    // Export the API
    window.ReactBridge = {
        renderComponent: renderReactComponent,
        unmountComponent: unmountReactComponent,
        loadPackage: loadPackage,
        loadCSS: loadCSS
    };
})();