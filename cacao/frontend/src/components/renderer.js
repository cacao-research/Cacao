/**
 * Component renderer function
 */

const { createElement: h } = React;
import { ErrorBoundary } from './core/ErrorBoundary.js';

/**
 * Find close matches for a component name (Levenshtein-based)
 */
function didYouMean(name, candidates, maxResults = 3) {
  const lower = name.toLowerCase();
  const scored = candidates
    .map(c => ({ name: c, dist: levenshtein(lower, c.toLowerCase()) }))
    .filter(c => c.dist <= Math.max(2, Math.floor(name.length * 0.4)))
    .sort((a, b) => a.dist - b.dist);
  return scored.slice(0, maxResults).map(s => s.name);
}

/**
 * Levenshtein distance between two strings
 */
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, (_, i) => {
    const row = new Array(n + 1);
    row[0] = i;
    return row;
  });
  for (let j = 1; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

/**
 * Render a component from its JSON definition
 * @param {object} comp - Component definition
 * @param {string|number} key - React key
 * @param {function} setActiveTab - Tab state setter
 * @param {string} activeTab - Current active tab
 * @param {object} renderers - Map of component renderers
 * @returns {React.Element|null}
 */
export function renderComponent(comp, key, setActiveTab, activeTab, renderers) {
  if (!comp || !comp.type) return null;

  const Renderer = renderers[comp.type];
  if (!Renderer) {
    const candidates = Object.keys(renderers);
    const suggestions = didYouMean(comp.type, candidates);
    const hint = suggestions.length
      ? ` Did you mean: ${suggestions.join(', ')}?`
      : '';

    console.warn(`Unknown component type: "${comp.type}".${hint}`);

    return h('div', {
      key,
      className: 'cacao-unknown-component',
    },
      h('span', { className: 'cacao-unknown-component__icon' }, '\u26A0'),
      h('span', null, `Unknown: "${comp.type}"`),
      hint && h('span', { className: 'cacao-unknown-component__hint' }, hint),
    );
  }

  // Track render counts for DevTools profiler
  if (window.__CACAO_DEVTOOLS__?.onRender) {
    window.__CACAO_DEVTOOLS__.onRender(comp.type);
  }

  const children = (comp.children || []).map((c, i) => renderComponent(c, i, setActiveTab, activeTab, renderers));
  const element = h(
    ErrorBoundary,
    { key, componentType: comp.type, type: comp.type, props: comp.props || {} },
    h(Renderer, { props: comp.props || {}, children, setActiveTab, activeTab, type: comp.type }),
  );

  // Universal id prop: wrap with cloneElement to inject id onto the outermost DOM node
  const id = comp.props?.id;
  if (id) {
    return React.cloneElement(element, { id });
  }
  return element;
}
