const { createElement: h } = React;

export function Button({ props }) {
  return h('button', { className: 'btn btn-' + (props.variant || 'primary') }, props.label);
}
