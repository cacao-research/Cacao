const { createElement: h } = React;

export function Alert({ props }) {
  return h('div', { className: 'alert alert-' + (props.type || 'info') }, [
    props.title && h('strong', { key: 'title' }, props.title + ': '),
    props.message
  ]);
}
