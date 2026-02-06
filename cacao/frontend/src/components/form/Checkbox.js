const { createElement: h } = React;

export function Checkbox({ props }) {
  return h('div', { className: 'checkbox-container' }, [
    h('input', { type: 'checkbox', className: 'checkbox', key: 'input' }),
    h('div', { key: 'text' }, [
      h('div', { className: 'checkbox-label', key: 'label' }, props.label),
      props.description && h('div', { className: 'checkbox-desc', key: 'desc' }, props.description)
    ])
  ]);
}
