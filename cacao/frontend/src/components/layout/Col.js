const { createElement: h } = React;

export function Col({ props, children }) {
  return h('div', {
    className: 'c-col' + (props.span ? ' col-span-' + props.span : ''),
    style: { gap: ((props.gap || 4) * 4) + 'px' }
  }, children);
}
