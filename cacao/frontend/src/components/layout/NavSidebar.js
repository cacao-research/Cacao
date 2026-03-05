/**
 * NavSidebar - Navigation sidebar container
 */

const { createElement: h } = React;

export function NavSidebar({ props, children }) {
  return h('nav', { className: 'nav-sidebar', 'aria-label': 'Main navigation' }, children);
}
