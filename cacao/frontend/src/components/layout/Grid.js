const { createElement: h } = React;

export function Grid({ props, children }) {
  return h('div', {
    className: 'c-grid',
    style: {
      gap: ((props.gap || 4) * 4) + 'px',
      gridTemplateColumns: 'repeat(' + (props.cols || 12) + ', 1fr)'
    }
  }, children);
}
