/**
 * Static Runtime for Cacao
 * Client-side signal management and event handling (no WebSocket)
 */

import { builtinHandlers } from '../../handlers/index.js';

// Signal store - client-side state management
class StaticSignals {
  constructor() {
    this.signals = {};
    this.listeners = new Set();
  }

  init(initialState) {
    this.signals = { ...initialState };
    window.__cacao_signals__ = this.signals;
    this.notifyListeners();
  }

  get(name) {
    return this.signals[name];
  }

  set(name, value) {
    this.signals[name] = value;
    window.__cacao_signals__ = this.signals;
    this.notifyListeners();
  }

  getAll() {
    return { ...this.signals };
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notifyListeners() {
    this.listeners.forEach(listener => listener(this.signals));
  }
}

// Event dispatcher - routes events to JavaScript handlers
class StaticEventDispatcher {
  constructor(signalStore) {
    // Start with built-in handlers
    this.handlers = { ...builtinHandlers };
    this.signals = signalStore;
  }

  register(eventName, handler) {
    this.handlers[eventName] = handler;
  }

  registerAll(handlers) {
    Object.entries(handlers).forEach(([name, handler]) => {
      this.handlers[name] = handler;
    });
  }

  dispatch(eventName, eventData = {}) {
    const handler = this.handlers[eventName];
    if (handler) {
      try {
        // Handle async handlers
        const result = handler(this.signals, eventData);
        if (result && typeof result.catch === 'function') {
          result.catch(e => console.error(`[Cacao Static] Error in async handler "${eventName}":`, e));
        }
      } catch (e) {
        console.error(`[Cacao Static] Error in handler "${eventName}":`, e);
      }
    } else {
      console.warn(`[Cacao Static] No handler for event: ${eventName}`);
    }
  }
}

// Global instances
const staticSignals = new StaticSignals();
const staticDispatcher = new StaticEventDispatcher(staticSignals);

// Compatibility layer - mimics cacaoWs interface for components
const cacaoStatic = {
  connected: true,
  signals: staticSignals.signals,

  getSignal(name) {
    return staticSignals.get(name);
  },

  sendEvent(eventName, eventData = {}) {
    staticDispatcher.dispatch(eventName, eventData);
  },

  subscribe(listener) {
    return staticSignals.subscribe(listener);
  }
};

// Check if we're in static mode
function isStaticMode() {
  return window.__CACAO_STATIC__ === true;
}

// Initialize static mode
function initStaticMode(config) {
  window.__CACAO_STATIC__ = true;

  // Initialize signals with defaults
  if (config.signals) {
    staticSignals.init(config.signals);
  }

  // Register additional custom handlers (built-ins are already loaded)
  if (config.handlers) {
    staticDispatcher.registerAll(config.handlers);
  }

  // Store component tree
  if (config.pages) {
    window.__CACAO_PAGES__ = config.pages;
  }

  const builtinCount = Object.keys(builtinHandlers).length;
  const customCount = Object.keys(config.handlers || {}).length;
  console.log(`[Cacao Static] Initialized with ${Object.keys(config.signals || {}).length} signals, ${builtinCount} built-in handlers, ${customCount} custom handlers`);
}

export {
  staticSignals,
  staticDispatcher,
  cacaoStatic,
  isStaticMode,
  initStaticMode,
  builtinHandlers
};
