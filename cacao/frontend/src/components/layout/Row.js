const { createElement: h } = React;

export function Row({ props, children }) {
  return h('div', {
    className: 'c-row' + (props.justify === 'between' ? ' justify-between' : ''),
    style: { gap: ((props.gap || 4) * 4) + 'px' }
  }, children);
}
