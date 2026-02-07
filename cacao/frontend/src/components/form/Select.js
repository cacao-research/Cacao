const { createElement: h } = React;

export function Select({ props }) {
  return h('div', { className: 'select-container' }, [
    h('label', { className: 'select-label', key: 'label' }, props.label),
    h('select', { className: 'select', key: 'select' },
      (props.options || []).map((o, i) => h('option', { key: i, value: o.value || o }, o.label || o))
    )
  ]);
}
