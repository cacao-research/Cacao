const { createElement: h } = React;

export function Card({ props, children }) {
  return h('div', { className: 'card' }, [
    props.title && h('div', { className: 'card-title', key: 'title' }, props.title),
    ...children
  ]);
}
