/**
 * Cacao Component Renderer
 * Main entry point - exports renderers map and mounts app
 * Supports lazy loading of component categories
 */

import { COLORS } from './core/constants.js';
import { formatValue } from './core/utils.js';
import { ChartWrapper } from './core/ChartWrapper.js';
import { initStaticMode, isStaticMode, staticSignals, staticDispatcher } from './core/static-runtime.js';
import { initShortcuts, registerShortcut, getShortcuts } from './core/shortcuts.js';
import { initTheme, setTheme, toggleTheme } from './core/ThemeToggle.js';
import { showToast } from './core/Toast.js';
import { openCommandPalette, registerCommand } from './core/CommandPalette.js';
import { PanelManager } from './core/PanelManager.js';

// Eager imports (always loaded)
import * as layout from './layout/index.js';
import * as typography from './typography/index.js';

// Lazy-loadable categories
import * as display from './display/index.js';
import * as form from './form/index.js';
import * as charts from './charts/index.js';

import { cacaoWs } from './core/websocket.js';
import { App } from './App.js';

// Category registry for lazy loading
const categoryModules = {
  layout,
  display,
  typography,
  form,
  charts,
};

// Track loaded categories
const loadedCategories = new Set(['layout', 'typography']);
const pendingLoads = new Map();

// Build renderers map (eagerly loaded categories first)
const renderers = {
  ...layout,
  ...typography,
};

/**
 * Load a component category on demand.
 * Returns immediately if already loaded; otherwise loads and merges into renderers.
 */
function loadCategory(categoryName) {
  if (loadedCategories.has(categoryName)) return Promise.resolve();

  if (pendingLoads.has(categoryName)) return pendingLoads.get(categoryName);

  const mod = categoryModules[categoryName];
  if (mod) {
    // Module already bundled — just merge into renderers
    Object.assign(renderers, mod);
    loadedCategories.add(categoryName);
    return Promise.resolve();
  }

  return Promise.resolve();
}

/**
 * Ensure all categories used by a page are loaded.
 * Called before rendering with the categories list from the server.
 */
function ensureCategories(categories) {
  if (!categories || categories.length === 0) {
    // Load everything
    return loadAllCategories();
  }
  return Promise.all(categories.map(loadCategory));
}

/**
 * Load all component categories.
 */
function loadAllCategories() {
  const promises = Object.keys(categoryModules).map(loadCategory);
  return Promise.all(promises);
}

// Load all categories on startup (progressive enhancement)
loadAllCategories();

// Initialize keyboard shortcuts and theme
initShortcuts();
initTheme();

// Export static mode utilities for external use
window.Cacao = {
  initStatic: initStaticMode,
  isStaticMode,
  signals: staticSignals,
  dispatcher: staticDispatcher,
  renderers,
  // WebSocket / chat streaming
  ws: cacaoWs,
  // Feature APIs
  toast: showToast,
  setTheme,
  toggleTheme,
  openCommandPalette,
  registerCommand,
  // Shortcuts
  registerShortcut,
  getShortcuts,
  // Theme registration (for plugins)
  registerTheme(name, vars) {
    const root = document.documentElement;
    const style = document.createElement('style');
    const props = Object.entries(vars).map(([k, v]) => `--${k}: ${v};`).join('\n  ');
    style.textContent = `[data-theme="${name}"] {\n  ${props}\n}`;
    document.head.appendChild(style);
  },
  // Custom component registration (for plugins)
  registerComponent(name, renderFn) {
    renderers[name] = renderFn;
  },
  // Panel manager
  panelManager: PanelManager,
  // Lazy loading API
  loadCategory,
  ensureCategories,
  loadAllCategories,
  loadedCategories,
};

// Mount app (defer if in static mode to allow initialization first)
function mountApp() {
  ReactDOM.createRoot(document.getElementById('root')).render(
    React.createElement(App, { renderers })
  );
}

// Auto-mount unless static mode initialization is pending
if (!window.__CACAO_DEFER_MOUNT__) {
  mountApp();
}

// Export mount function for static mode
window.Cacao.mount = mountApp;
