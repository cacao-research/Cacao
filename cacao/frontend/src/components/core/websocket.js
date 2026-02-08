/**
 * WebSocket Manager for Cacao
 * Handles connection to server and event dispatching
 * Also supports static mode (no server, client-side only)
 */

import { cacaoStatic, isStaticMode, staticSignals, staticDispatcher } from './static-runtime.js';

class CacaoWebSocket {
  constructor() {
    this.ws = null;
    this.connected = false;
    this.signals = {};
    this.listeners = new Set();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    // In static mode, don't connect to WebSocket
    if (isStaticMode()) {
      console.log('[Cacao] Running in static mode - no WebSocket');
      this.connected = true;
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const url = `${protocol}//${window.location.host}/ws`;

    console.log('[Cacao] Connecting to WebSocket:', url);

    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('[Cacao] WebSocket connected');
      this.connected = true;
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (e) {
        console.error('[Cacao] Failed to parse message:', e);
      }
    };

    this.ws.onclose = () => {
      console.log('[Cacao] WebSocket disconnected');
      this.connected = false;
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('[Cacao] WebSocket error:', error);
    };
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`[Cacao] Reconnecting (attempt ${this.reconnectAttempts})...`);
      setTimeout(() => this.connect(), this.reconnectDelay * this.reconnectAttempts);
    }
  }

  handleMessage(message) {
    const { type } = message;

    switch (type) {
      case 'init':
        // Initial state from server: { type: 'init', state: {...}, sessionId: '...' }
        this.signals = message.state || {};
        this.sessionId = message.sessionId;
        window.__cacao_signals__ = this.signals;
        this.notifyListeners();
        console.log('[Cacao] Received initial state:', this.signals);
        break;

      case 'update':
        // Signal updates from server: { type: 'update', changes: {...} }
        if (message.changes) {
          Object.entries(message.changes).forEach(([name, value]) => {
            this.signals[name] = value;
          });
          window.__cacao_signals__ = this.signals;
          this.notifyListeners();
          console.log('[Cacao] State updated:', message.changes);
        }
        break;

      default:
        console.log('[Cacao] Unknown message type:', type, message);
    }
  }

  sendEvent(eventName, eventData = {}) {
    // In static mode, dispatch to local handlers
    if (isStaticMode()) {
      staticDispatcher.dispatch(eventName, eventData);
      return;
    }

    if (!this.connected || !this.ws) {
      console.warn('[Cacao] Cannot send event - not connected');
      return;
    }

    const message = {
      type: 'event',
      name: eventName,
      data: eventData
    };

    console.log('[Cacao] Sending event:', message);
    this.ws.send(JSON.stringify(message));
  }

  getSignal(name) {
    if (isStaticMode()) {
      return staticSignals.get(name);
    }
    return this.signals[name];
  }

  subscribe(listener) {
    if (isStaticMode()) {
      return staticSignals.subscribe(listener);
    }
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notifyListeners() {
    this.listeners.forEach(listener => listener(this.signals));
  }
}

// Global instance
const cacaoWs = new CacaoWebSocket();

// Connect on load (unless in static mode - that's initialized separately)
if (typeof window !== 'undefined' && !isStaticMode()) {
  cacaoWs.connect();
}

// Export for use in components
export { cacaoWs };
