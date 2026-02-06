const { createElement: h } = React;

export function Title({ props }) {
  return h('h' + (props.level || 1), { className: 'title title-' + (props.level || 1) }, props.text);
}
