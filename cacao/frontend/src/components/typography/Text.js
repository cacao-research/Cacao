const { createElement: h } = React;

export function Text({ props }) {
  return h('p', {
    className: 'text ' + (props.color === 'muted' ? 'text-muted' : '') + ' ' + (props.size === 'sm' ? 'text-sm' : props.size === 'lg' ? 'text-lg' : '')
  }, props.content);
}
