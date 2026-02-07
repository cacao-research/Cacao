const { createElement: h } = React;

export function Sidebar({ props, children }) {
  return h('div', { className: 'sidebar' }, children);
}
