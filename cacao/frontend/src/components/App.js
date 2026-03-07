/**
 * Main App component (was Dashboard)
 */

const { createElement: h, useState, useEffect, useCallback } = React;
import { renderComponent } from './renderer.js';
import { isStaticMode } from './core/static-runtime.js';
import { CommandPalette } from './core/CommandPalette.js';
import { ToastContainer } from './core/Toast.js';
import { NotificationCenter } from './core/NotificationCenter.js';
import { LoginPage } from './core/LoginPage.js';
import { ErrorOverlay } from './core/ErrorOverlay.js';
import { DevTools } from './core/DevTools.js';

// Extract route from URL (supports both pathname and hash-based routing)
function getRouteFromPath() {
  // Check hash first (for static/GitHub Pages mode)
  if (window.location.hash) {
    const hash = window.location.hash.replace(/^#\/?/, '');
    if (hash) return hash;
  }
  // In static mode or file:// protocol, don't use pathname as route
  // (pathname would be the full file path like /C:/Users/.../index.html)
  if (isStaticMode() || window.location.protocol === 'file:') {
    return null;
  }
  // Fall back to pathname (only for server mode)
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
  const [authRequired, setAuthRequired] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);

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
      .then(data => {
        window.__CACAO_SLOTS__ = data.slots || {};
        // Inject head slot content into document <head>
        const headSlot = (data.slots || {}).head;
        if (headSlot && headSlot.length) {
          headSlot.forEach(item => {
            if (item.type === 'RawHtml' && item.props && item.props.html) {
              const container = document.createElement('div');
              container.innerHTML = item.props.html;
              while (container.firstChild) {
                document.head.appendChild(container.firstChild);
              }
            }
          });
        }
        // Show page-build errors in dev overlay
        if (data.error && window.__CACAO_DEBUG__) {
          setTimeout(() => {
            if (window.__CACAO_ERROR_OVERLAY__) {
              window.__CACAO_ERROR_OVERLAY__.addError(data.error);
            }
          }, 100);
        }
        return setPages(data);
      })
      .catch(e => setError(e.message));
  }, []);

  // Check for auth_required flag
  useEffect(() => {
    const check = () => {
      if (window.__CACAO_AUTH_REQUIRED__ && !authenticated) {
        setAuthRequired(true);
      }
    };
    check();
    // Re-check when signals update (auth_required comes via WS)
    const interval = setInterval(check, 500);
    return () => clearInterval(interval);
  }, [authenticated]);

  // Show login page if auth is required
  if (authRequired && !authenticated) {
    const title = pages?.metadata?.title || 'Cacao App';
    return h(LoginPage, {
      title,
      onLogin: (data) => {
        window.__CACAO_AUTH_REQUIRED__ = false;
        setAuthenticated(true);
        setAuthRequired(false);
      },
    });
  }

  if (error) return h('div', { className: 'loading', style: { color: 'var(--danger)' } }, 'Error: ' + error);
  if (!pages) return h('div', { className: 'loading' }, 'Loading...');

  const pageData = pages.pages || {};
  const components = pageData[currentPage] || [];

  const render = (comp, key) => renderComponent(comp, key, setActiveTabWithRoute, activeTab, renderers);

  // Global overlays
  const overlays = [
    h(CommandPalette, { key: 'cmd-palette', setActiveTab: setActiveTabWithRoute, pages: pageData }),
    h(ToastContainer, { key: 'toast' }),
    h(NotificationCenter, { key: 'notifications' }),
    window.__CACAO_DEBUG__ && h(ErrorOverlay, { key: 'error-overlay' }),
    window.__CACAO_DEBUG__ && h(DevTools, { key: 'devtools' }),
  ].filter(Boolean);

  // Check if there's an AppShell component (admin layout)
  const appShellIdx = components.findIndex(c => c.type === 'AppShell');
  if (appShellIdx >= 0) {
    // Render ALL root components (e.g. RawHtml style blocks) plus the AppShell
    const allRendered = components.map((c, i) => render(c, i));
    return h(React.Fragment, null, [
      ...allRendered,
      ...overlays,
    ]);
  }

  // Standard layout with optional right sidebar
  const sidebarIdx = components.findIndex(c => c.type === 'Sidebar');
  const sidebar = sidebarIdx >= 0 ? components[sidebarIdx] : null;
  const mainComponents = sidebarIdx >= 0 ? [...components.slice(0, sidebarIdx), ...components.slice(sidebarIdx + 1)] : components;

  return h(React.Fragment, null, [
    h('div', { className: 'app-container', key: 'app' }, [
      h('div', { className: 'main-content', key: 'main' }, mainComponents.map((c, i) => render(c, i))),
      sidebar && h('div', { className: 'sidebar', key: 'sidebar' }, (sidebar.children || []).map((c, i) => render(c, i)))
    ]),
    ...overlays,
  ]);
}
