/**
 * Main App component (was Dashboard)
 */

const { createElement: h, useState, useEffect, useCallback } = React;
import { renderComponent } from './renderer.js';
import { isStaticMode } from './core/static-runtime.js';

// Extract route from URL (supports both pathname and hash-based routing)
function getRouteFromPath() {
  // Check hash first (for static/GitHub Pages mode)
  if (window.location.hash) {
    const hash = window.location.hash.replace(/^#\/?/, '');
    if (hash) return hash;
  }
  // Fall back to pathname
  const path = window.location.pathname;
  // Remove leading slash, return null if empty (will use default)
  const route = path.replace(/^\/+/, '');
  return route || null;
}

// Get base path for static deployments (e.g., GitHub Pages)
function getBasePath() {
  return window.__CACAO_BASE_PATH__ || '';
}

export function App({ renderers }) {
  const [pages, setPages] = useState(null);
  const [currentPage, setCurrentPage] = useState('/');
  // Initialize activeTab from URL if present
  const [activeTab, setActiveTab] = useState(() => getRouteFromPath());
  const [error, setError] = useState(null);

  // Wrap setActiveTab to also update URL
  const setActiveTabWithRoute = useCallback((tab) => {
    setActiveTab(tab);
    // Update URL without page reload
    if (tab) {
      // In static mode, use hash-based routing for GitHub Pages compatibility
      if (isStaticMode()) {
        const newHash = '#/' + tab;
        if (window.location.hash !== newHash) {
          window.history.pushState({ tab }, '', newHash);
        }
      } else {
        const newPath = '/' + tab;
        if (window.location.pathname !== newPath) {
          window.history.pushState({ tab }, '', newPath);
        }
      }
    }
  }, []);

  // Handle browser back/forward (and hashchange for static mode)
  useEffect(() => {
    const handleNavigation = (event) => {
      const tab = event?.state?.tab || getRouteFromPath();
      setActiveTab(tab);
    };
    window.addEventListener('popstate', handleNavigation);
    window.addEventListener('hashchange', handleNavigation);
    return () => {
      window.removeEventListener('popstate', handleNavigation);
      window.removeEventListener('hashchange', handleNavigation);
    };
  }, []);

  // Replace initial history state with current tab
  useEffect(() => {
    if (activeTab) {
      const url = isStaticMode() ? '#/' + activeTab : '/' + activeTab;
      window.history.replaceState({ tab: activeTab }, '', url);
    }
  }, []);

  useEffect(() => {
    // In static mode, pages are embedded in window.__CACAO_PAGES__
    if (isStaticMode() && window.__CACAO_PAGES__) {
      setPages(window.__CACAO_PAGES__);
      return;
    }

    // Dynamic mode - fetch from server
    fetch('/api/pages')
      .then(r => r.json())
      .then(data => setPages(data))
      .catch(e => setError(e.message));
  }, []);

  if (error) return h('div', { className: 'loading', style: { color: 'var(--danger)' } }, 'Error: ' + error);
  if (!pages) return h('div', { className: 'loading' }, 'Loading...');

  const pageData = pages.pages || {};
  const components = pageData[currentPage] || [];

  const render = (comp, key) => renderComponent(comp, key, setActiveTabWithRoute, activeTab, renderers);

  // Check if there's an AppShell component (admin layout)
  const appShellIdx = components.findIndex(c => c.type === 'AppShell');
  if (appShellIdx >= 0) {
    // Render the AppShell which handles its own layout
    return render(components[appShellIdx], 'app-shell');
  }

  // Standard layout with optional right sidebar
  const sidebarIdx = components.findIndex(c => c.type === 'Sidebar');
  const sidebar = sidebarIdx >= 0 ? components[sidebarIdx] : null;
  const mainComponents = sidebarIdx >= 0 ? [...components.slice(0, sidebarIdx), ...components.slice(sidebarIdx + 1)] : components;

  return h('div', { className: 'app-container' }, [
    h('div', { className: 'main-content', key: 'main' }, mainComponents.map((c, i) => render(c, i))),
    sidebar && h('div', { className: 'sidebar', key: 'sidebar' }, (sidebar.children || []).map((c, i) => render(c, i)))
  ]);
}
