/**
 * Badge - Small status indicator component
 */

const { createElement: h } = React;

export function Badge({ props }) {
  const { text, color = 'default' } = props;

  return h('span', { className: `c-badge c-badge-${color}` }, text);
}
