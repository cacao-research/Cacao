/**
 * Component renderer function
 */

const { createElement: h } = React;

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
    console.warn('Unknown component type:', comp.type);
    return h('div', { key, style: { color: 'var(--warning)', fontSize: '0.875rem' } }, '[' + comp.type + ']');
  }

  const children = (comp.children || []).map((c, i) => renderComponent(c, i, setActiveTab, activeTab, renderers));
  return h(Renderer, { props: comp.props || {}, children, key, setActiveTab, activeTab, type: comp.type });
}
