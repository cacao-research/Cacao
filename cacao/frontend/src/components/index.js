/**
 * Cacao Component Renderer
 * Main entry point - exports renderers map and mounts app
 */

import { COLORS } from './core/constants.js';
import { formatValue } from './core/utils.js';
import { ChartWrapper } from './core/ChartWrapper.js';
import { initStaticMode, isStaticMode, staticSignals, staticDispatcher } from './core/static-runtime.js';

import * as layout from './layout/index.js';
import * as display from './display/index.js';
import * as typography from './typography/index.js';
import * as form from './form/index.js';
import * as charts from './charts/index.js';

import { App } from './App.js';

// Build renderers map
const renderers = {
  ...layout,
  ...display,
  ...typography,
  ...form,
  ...charts,
};

// Export static mode utilities for external use
window.Cacao = {
  initStatic: initStaticMode,
  isStaticMode,
  signals: staticSignals,
  dispatcher: staticDispatcher,
  renderers
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
