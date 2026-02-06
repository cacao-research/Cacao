const { createElement: h } = React;

export function Progress({ props }) {
  return h('div', { className: 'progress-container' }, [
    props.label && h('div', { className: 'progress-label', key: 'label' }, props.label),
    h('div', { className: 'progress-bar', key: 'bar' },
      h('div', { className: 'progress-fill', style: { width: ((props.value / (props.max || 100)) * 100) + '%' } })
    )
  ]);
}
