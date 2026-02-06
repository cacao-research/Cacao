const { createElement: h } = React;

export function Slider({ props }) {
  return h('div', { className: 'slider-container' }, [
    h('label', { className: 'slider-label', key: 'label' }, props.label),
    h('input', { type: 'range', className: 'slider', min: props.min || 0, max: props.max || 100, step: props.step || 1, key: 'input' })
  ]);
}
