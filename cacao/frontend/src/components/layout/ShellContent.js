/**
 * ShellContent - Main content area of AppShell
 */

const { createElement: h } = React;

export function ShellContent({ props, children }) {
  return h('div', { className: 'shell-content' }, children);
}
