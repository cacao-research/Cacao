/**
 * Cacao DevTools Panel
 * Browser-based developer tools for debugging Cacao apps.
 * Shows signal inspector, event log, component tree, and performance profiler.
 * Only active when window.__CACAO_DEBUG__ is true.
 */

const { createElement: h, useState, useEffect, useCallback, useRef, useMemo } = React;
import { cacaoWs } from './websocket.js';
import { isStaticMode } from './static-runtime.js';

// ─── Event Log Store ────────────────────────────────────────────────────
const eventLog = [];
const MAX_LOG_ENTRIES = 200;
let _eventLogListeners = new Set();

function pushEvent(entry) {
  eventLog.push({ ...entry, id: Date.now() + Math.random(), ts: Date.now() });
  if (eventLog.length > MAX_LOG_ENTRIES) eventLog.shift();
  _eventLogListeners.forEach(fn => fn());
}

// ─── Performance Store ──────────────────────────────────────────────────
const perfData = {
  signalUpdates: [],       // { name, ts, duration }
  renderCounts: {},        // componentType -> count
  totalRenders: 0,
  sessionStart: Date.now(),
};
let _perfListeners = new Set();

function recordSignalUpdate(name, duration) {
  perfData.signalUpdates.push({ name, ts: Date.now(), duration });
  if (perfData.signalUpdates.length > 500) perfData.signalUpdates.shift();
  _perfListeners.forEach(fn => fn());
}

function recordRender(componentType) {
  perfData.renderCounts[componentType] = (perfData.renderCounts[componentType] || 0) + 1;
  perfData.totalRenders++;
  _perfListeners.forEach(fn => fn());
}

// ─── Instrument WebSocket ───────────────────────────────────────────────
function instrumentWebSocket() {
  if (cacaoWs._devtoolsInstrumented) return;
  cacaoWs._devtoolsInstrumented = true;

  // Intercept incoming messages
  const origHandle = cacaoWs.handleMessage.bind(cacaoWs);
  cacaoWs.handleMessage = function(message) {
    const start = performance.now();
    pushEvent({ type: 'ws:recv', msgType: message.type, data: message });

    if (message.type === 'update' && message.changes) {
      Object.keys(message.changes).forEach(name => {
        recordSignalUpdate(name, performance.now() - start);
      });
    }

    origHandle(message);
  };

  // Intercept outgoing events
  const origSend = cacaoWs.sendEvent.bind(cacaoWs);
  cacaoWs.sendEvent = function(eventName, eventData) {
    pushEvent({ type: 'ws:send', msgType: 'event', data: { name: eventName, data: eventData } });
    origSend(eventName, eventData);
  };

  // Intercept raw send
  const origRawSend = cacaoWs.send.bind(cacaoWs);
  cacaoWs.send = function(message) {
    pushEvent({ type: 'ws:send', msgType: message.type || 'raw', data: message });
    origRawSend(message);
  };
}

// ─── Instrument renderer for render counts ──────────────────────────────
function instrumentRenderer() {
  if (window.__CACAO_RENDER_INSTRUMENTED__) return;
  window.__CACAO_RENDER_INSTRUMENTED__ = true;

  // Expose a hook that the renderer can call
  window.__CACAO_DEVTOOLS__ = {
    onRender: recordRender,
    pushEvent,
    eventLog,
    perfData,
  };
}

// ─── Signal Inspector Tab ───────────────────────────────────────────────
function SignalInspector() {
  const [signals, setSignals] = useState({});
  const [filter, setFilter] = useState('');
  const [expandedKeys, setExpandedKeys] = useState(new Set());

  useEffect(() => {
    const update = (sigs) => setSignals({ ...sigs });
    // Get initial state
    if (isStaticMode()) {
      setSignals({ ...(window.__CACAO_INITIAL_SIGNALS__ || {}) });
    } else {
      setSignals({ ...cacaoWs.signals });
    }
    const unsub = cacaoWs.subscribe(update);
    return unsub;
  }, []);

  const filtered = useMemo(() => {
    const entries = Object.entries(signals);
    if (!filter) return entries;
    const lower = filter.toLowerCase();
    return entries.filter(([k]) => k.toLowerCase().includes(lower));
  }, [signals, filter]);

  const toggleExpand = useCallback((key) => {
    setExpandedKeys(prev => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  }, []);

  return h('div', { className: 'cacao-devtools__tab-content' },
    h('div', { className: 'cacao-devtools__toolbar' },
      h('input', {
        className: 'cacao-devtools__search',
        placeholder: 'Filter signals...',
        value: filter,
        onChange: e => setFilter(e.target.value),
      }),
      h('span', { className: 'cacao-devtools__count' }, `${filtered.length} signal${filtered.length !== 1 ? 's' : ''}`),
    ),
    h('div', { className: 'cacao-devtools__signal-list' },
      filtered.length === 0
        ? h('div', { className: 'cacao-devtools__empty' }, 'No signals found')
        : filtered.map(([name, value]) => {
            const isExpandable = typeof value === 'object' && value !== null;
            const expanded = expandedKeys.has(name);
            return h('div', { key: name, className: 'cacao-devtools__signal-item' },
              h('div', {
                className: 'cacao-devtools__signal-header',
                onClick: isExpandable ? () => toggleExpand(name) : undefined,
              },
                isExpandable && h('span', { className: 'cacao-devtools__expand-icon' }, expanded ? '\u25BC' : '\u25B6'),
                h('span', { className: 'cacao-devtools__signal-name' }, name),
                h('span', { className: 'cacao-devtools__signal-type' }, typeLabel(value)),
                !isExpandable && h('span', { className: 'cacao-devtools__signal-value' }, formatPreview(value)),
              ),
              expanded && isExpandable && h('pre', { className: 'cacao-devtools__signal-expanded' },
                JSON.stringify(value, null, 2),
              ),
            );
          }),
    ),
  );
}

// ─── Event Log Tab ──────────────────────────────────────────────────────
function EventLog() {
  const [, forceUpdate] = useState(0);
  const [filter, setFilter] = useState('');
  const [autoScroll, setAutoScroll] = useState(true);
  const listRef = useRef(null);

  useEffect(() => {
    const listener = () => forceUpdate(n => n + 1);
    _eventLogListeners.add(listener);
    return () => _eventLogListeners.delete(listener);
  }, []);

  useEffect(() => {
    if (autoScroll && listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  });

  const filtered = useMemo(() => {
    if (!filter) return eventLog;
    const lower = filter.toLowerCase();
    return eventLog.filter(e =>
      (e.msgType || '').toLowerCase().includes(lower) ||
      JSON.stringify(e.data || '').toLowerCase().includes(lower)
    );
  }, [eventLog.length, filter]);

  const clearLog = useCallback(() => {
    eventLog.length = 0;
    forceUpdate(n => n + 1);
  }, []);

  return h('div', { className: 'cacao-devtools__tab-content' },
    h('div', { className: 'cacao-devtools__toolbar' },
      h('input', {
        className: 'cacao-devtools__search',
        placeholder: 'Filter events...',
        value: filter,
        onChange: e => setFilter(e.target.value),
      }),
      h('label', { className: 'cacao-devtools__checkbox-label' },
        h('input', { type: 'checkbox', checked: autoScroll, onChange: () => setAutoScroll(!autoScroll) }),
        'Auto-scroll',
      ),
      h('button', { className: 'cacao-devtools__btn', onClick: clearLog }, 'Clear'),
      h('span', { className: 'cacao-devtools__count' }, `${filtered.length} events`),
    ),
    h('div', { className: 'cacao-devtools__event-list', ref: listRef },
      filtered.length === 0
        ? h('div', { className: 'cacao-devtools__empty' }, 'No events yet')
        : filtered.map(entry =>
            h('div', {
              key: entry.id,
              className: `cacao-devtools__event-item cacao-devtools__event-item--${entry.type === 'ws:send' ? 'out' : 'in'}`,
            },
              h('span', { className: 'cacao-devtools__event-dir' }, entry.type === 'ws:send' ? '\u2191' : '\u2193'),
              h('span', { className: 'cacao-devtools__event-time' }, formatTime(entry.ts)),
              h('span', { className: 'cacao-devtools__event-type' }, entry.msgType),
              h('span', { className: 'cacao-devtools__event-preview' }, eventPreview(entry)),
            ),
          ),
    ),
  );
}

// ─── Component Tree Tab ─────────────────────────────────────────────────
function ComponentTree() {
  const [tree, setTree] = useState(null);
  const [expandedPaths, setExpandedPaths] = useState(new Set(['']));

  useEffect(() => {
    // Fetch component tree from pages endpoint or window data
    if (isStaticMode() && window.__CACAO_PAGES__) {
      setTree(window.__CACAO_PAGES__);
    } else {
      fetch('/api/pages')
        .then(r => r.json())
        .then(data => setTree(data))
        .catch(() => setTree(null));
    }
  }, []);

  const togglePath = useCallback((path) => {
    setExpandedPaths(prev => {
      const next = new Set(prev);
      next.has(path) ? next.delete(path) : next.add(path);
      return next;
    });
  }, []);

  if (!tree) return h('div', { className: 'cacao-devtools__tab-content' },
    h('div', { className: 'cacao-devtools__empty' }, 'Loading component tree...'),
  );

  const pages = tree.pages || {};
  return h('div', { className: 'cacao-devtools__tab-content' },
    h('div', { className: 'cacao-devtools__tree' },
      Object.entries(pages).map(([pagePath, components]) =>
        h('div', { key: pagePath, className: 'cacao-devtools__tree-page' },
          h('div', {
            className: 'cacao-devtools__tree-page-header',
            onClick: () => togglePath(pagePath),
          },
            h('span', { className: 'cacao-devtools__expand-icon' },
              expandedPaths.has(pagePath) ? '\u25BC' : '\u25B6'),
            h('span', { className: 'cacao-devtools__tree-page-name' }, pagePath || '/'),
            h('span', { className: 'cacao-devtools__count' }, `${components.length} root`),
          ),
          expandedPaths.has(pagePath) && h('div', { className: 'cacao-devtools__tree-children' },
            components.map((comp, i) => renderTreeNode(comp, `${pagePath}/${i}`, 0, expandedPaths, togglePath)),
          ),
        ),
      ),
    ),
  );
}

function renderTreeNode(comp, path, depth, expandedPaths, togglePath) {
  if (!comp || !comp.type) return null;
  const children = comp.children || [];
  const hasChildren = children.length > 0;
  const expanded = expandedPaths.has(path);
  const propKeys = Object.keys(comp.props || {}).filter(k => k !== 'children');

  return h('div', { key: path, className: 'cacao-devtools__tree-node', style: { paddingLeft: depth * 16 } },
    h('div', {
      className: 'cacao-devtools__tree-node-header',
      onClick: hasChildren ? () => togglePath(path) : undefined,
    },
      hasChildren
        ? h('span', { className: 'cacao-devtools__expand-icon' }, expanded ? '\u25BC' : '\u25B6')
        : h('span', { className: 'cacao-devtools__expand-icon cacao-devtools__expand-icon--leaf' }, '\u00B7'),
      h('span', { className: 'cacao-devtools__tree-type' }, comp.type),
      propKeys.length > 0 && h('span', { className: 'cacao-devtools__tree-props' },
        propKeys.slice(0, 3).map(k => `${k}=${JSON.stringify(comp.props[k])}`).join(' ') +
        (propKeys.length > 3 ? ' ...' : ''),
      ),
      hasChildren && h('span', { className: 'cacao-devtools__count' }, children.length),
    ),
    expanded && hasChildren && h('div', { className: 'cacao-devtools__tree-children' },
      children.map((child, i) => renderTreeNode(child, `${path}/${i}`, depth + 1, expandedPaths, togglePath)),
    ),
  );
}

// ─── Performance Profiler Tab ───────────────────────────────────────────
function PerfProfiler() {
  const [, forceUpdate] = useState(0);
  const [sortBy, setSortBy] = useState('count');

  useEffect(() => {
    const listener = () => forceUpdate(n => n + 1);
    _perfListeners.add(listener);
    return () => _perfListeners.delete(listener);
  }, []);

  const uptime = ((Date.now() - perfData.sessionStart) / 1000).toFixed(0);

  // Signal update frequency
  const signalStats = useMemo(() => {
    const stats = {};
    for (const u of perfData.signalUpdates) {
      if (!stats[u.name]) stats[u.name] = { name: u.name, count: 0, totalDuration: 0, lastTs: 0 };
      stats[u.name].count++;
      stats[u.name].totalDuration += u.duration;
      stats[u.name].lastTs = u.ts;
    }
    return Object.values(stats);
  }, [perfData.signalUpdates.length]);

  // Render counts sorted
  const renderStats = useMemo(() => {
    return Object.entries(perfData.renderCounts)
      .map(([type, count]) => ({ type, count }))
      .sort((a, b) => sortBy === 'count' ? b.count - a.count : a.type.localeCompare(b.type));
  }, [perfData.totalRenders, sortBy]);

  const clearPerf = useCallback(() => {
    perfData.signalUpdates.length = 0;
    Object.keys(perfData.renderCounts).forEach(k => delete perfData.renderCounts[k]);
    perfData.totalRenders = 0;
    perfData.sessionStart = Date.now();
    forceUpdate(n => n + 1);
  }, []);

  return h('div', { className: 'cacao-devtools__tab-content' },
    h('div', { className: 'cacao-devtools__toolbar' },
      h('span', { className: 'cacao-devtools__perf-stat' }, `Uptime: ${uptime}s`),
      h('span', { className: 'cacao-devtools__perf-stat' }, `Total renders: ${perfData.totalRenders}`),
      h('span', { className: 'cacao-devtools__perf-stat' }, `Signal updates: ${perfData.signalUpdates.length}`),
      h('button', { className: 'cacao-devtools__btn', onClick: clearPerf }, 'Reset'),
    ),

    h('div', { className: 'cacao-devtools__perf-section' },
      h('h4', { className: 'cacao-devtools__perf-heading' }, 'Signal Update Frequency'),
      signalStats.length === 0
        ? h('div', { className: 'cacao-devtools__empty' }, 'No signal updates yet')
        : h('div', { className: 'cacao-devtools__perf-table' },
            h('div', { className: 'cacao-devtools__perf-row cacao-devtools__perf-row--header' },
              h('span', null, 'Signal'),
              h('span', null, 'Updates'),
              h('span', null, 'Avg (ms)'),
              h('span', null, 'Last'),
            ),
            signalStats.map(s =>
              h('div', { key: s.name, className: 'cacao-devtools__perf-row' },
                h('span', { className: 'cacao-devtools__signal-name' }, s.name),
                h('span', null, s.count),
                h('span', null, (s.totalDuration / s.count).toFixed(2)),
                h('span', { className: 'cacao-devtools__event-time' }, formatTime(s.lastTs)),
              ),
            ),
          ),
    ),

    h('div', { className: 'cacao-devtools__perf-section' },
      h('div', { className: 'cacao-devtools__perf-heading-row' },
        h('h4', { className: 'cacao-devtools__perf-heading' }, 'Render Counts'),
        h('button', {
          className: 'cacao-devtools__btn cacao-devtools__btn--tiny',
          onClick: () => setSortBy(sortBy === 'count' ? 'name' : 'count'),
        }, `Sort: ${sortBy}`),
      ),
      renderStats.length === 0
        ? h('div', { className: 'cacao-devtools__empty' }, 'No renders tracked yet')
        : h('div', { className: 'cacao-devtools__perf-table' },
            h('div', { className: 'cacao-devtools__perf-row cacao-devtools__perf-row--header' },
              h('span', null, 'Component'),
              h('span', null, 'Renders'),
            ),
            renderStats.map(s =>
              h('div', { key: s.type, className: 'cacao-devtools__perf-row' },
                h('span', { className: 'cacao-devtools__tree-type' }, s.type),
                h('span', null, s.count),
              ),
            ),
          ),
    ),
  );
}

// ─── Session Viewer (inside Signal Inspector) ───────────────────────────
function SessionInfo() {
  const sessionId = cacaoWs.sessionId || '(unknown)';
  const connected = cacaoWs.connected;
  const signalCount = Object.keys(cacaoWs.signals || {}).length;

  return h('div', { className: 'cacao-devtools__session-info' },
    h('div', { className: 'cacao-devtools__session-row' },
      h('span', { className: 'cacao-devtools__session-label' }, 'Session ID'),
      h('span', { className: 'cacao-devtools__session-value' }, sessionId),
    ),
    h('div', { className: 'cacao-devtools__session-row' },
      h('span', { className: 'cacao-devtools__session-label' }, 'Status'),
      h('span', {
        className: `cacao-devtools__session-value cacao-devtools__session-value--${connected ? 'ok' : 'err'}`,
      }, connected ? 'Connected' : 'Disconnected'),
    ),
    h('div', { className: 'cacao-devtools__session-row' },
      h('span', { className: 'cacao-devtools__session-label' }, 'Signals'),
      h('span', { className: 'cacao-devtools__session-value' }, signalCount),
    ),
    h('div', { className: 'cacao-devtools__session-row' },
      h('span', { className: 'cacao-devtools__session-label' }, 'Mode'),
      h('span', { className: 'cacao-devtools__session-value' }, isStaticMode() ? 'Static' : 'WebSocket'),
    ),
  );
}

// ─── Main DevTools Panel ────────────────────────────────────────────────
const TABS = [
  { id: 'signals', label: 'Signals' },
  { id: 'events', label: 'Events' },
  { id: 'tree', label: 'Tree' },
  { id: 'perf', label: 'Perf' },
];

export function DevTools() {
  const [open, setOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('signals');
  const [position, setPosition] = useState('bottom'); // 'bottom' or 'right'

  useEffect(() => {
    instrumentWebSocket();
    instrumentRenderer();

    // Keyboard shortcut: Ctrl+Shift+D to toggle
    const handler = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        setOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  // Floating toggle button
  const toggle = h('button', {
    className: 'cacao-devtools__toggle',
    onClick: () => setOpen(!open),
    title: 'Cacao DevTools (Ctrl+Shift+D)',
  }, '\u{1F6E0}');

  if (!open) return toggle;

  const tabContent = {
    signals: h(React.Fragment, null,
      h(SessionInfo, null),
      h(SignalInspector, null),
    ),
    events: h(EventLog, null),
    tree: h(ComponentTree, null),
    perf: h(PerfProfiler, null),
  };

  return h(React.Fragment, null,
    toggle,
    h('div', { className: `cacao-devtools cacao-devtools--${position}` },
      h('div', { className: 'cacao-devtools__header' },
        h('span', { className: 'cacao-devtools__title' }, 'Cacao DevTools'),
        h('div', { className: 'cacao-devtools__header-actions' },
          h('button', {
            className: 'cacao-devtools__btn',
            onClick: () => setPosition(position === 'bottom' ? 'right' : 'bottom'),
            title: 'Toggle position',
          }, position === 'bottom' ? '\u2B95' : '\u2B07'),
          h('button', {
            className: 'cacao-devtools__close',
            onClick: () => setOpen(false),
          }, '\u00D7'),
        ),
      ),
      h('div', { className: 'cacao-devtools__tabs' },
        TABS.map(tab =>
          h('button', {
            key: tab.id,
            className: `cacao-devtools__tab ${activeTab === tab.id ? 'cacao-devtools__tab--active' : ''}`,
            onClick: () => setActiveTab(tab.id),
          }, tab.label),
        ),
      ),
      h('div', { className: 'cacao-devtools__body' },
        tabContent[activeTab],
      ),
    ),
  );
}

// ─── Helpers ────────────────────────────────────────────────────────────
function typeLabel(value) {
  if (value === null) return 'null';
  if (Array.isArray(value)) return `array[${value.length}]`;
  return typeof value;
}

function formatPreview(value) {
  if (value === null || value === undefined) return String(value);
  if (typeof value === 'string') return value.length > 60 ? `"${value.slice(0, 57)}..."` : `"${value}"`;
  if (typeof value === 'boolean' || typeof value === 'number') return String(value);
  return JSON.stringify(value).slice(0, 60);
}

function formatTime(ts) {
  const d = new Date(ts);
  return d.toLocaleTimeString('en-US', { hour12: false }) + '.' + String(d.getMilliseconds()).padStart(3, '0');
}

function eventPreview(entry) {
  const d = entry.data;
  if (!d) return '';
  if (d.name) return d.name;
  if (d.changes) return Object.keys(d.changes).join(', ');
  if (d.signal) return d.signal;
  return '';
}
