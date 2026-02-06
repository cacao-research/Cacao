/**
 * Cacao Component Renderer
 * Main entry point - exports renderers map and mounts app
 */

import { COLORS } from './core/constants.js';
import { formatValue } from './core/utils.js';
import { ChartWrapper } from './core/ChartWrapper.js';

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

// Mount app
ReactDOM.createRoot(document.getElementById('root')).render(
  React.createElement(App, { renderers })
);
