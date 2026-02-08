/**
 * NavPanel - Content panel that shows when matching nav_item is active
 */

const { createElement: h } = React;

export function NavPanel({ props, children, activeTab }) {
  const { panelKey } = props;

  // Only render if this panel's key matches the active nav item
  if (panelKey !== activeTab) {
    return null;
  }

  return h('div', { className: 'nav-panel' }, children);
}
