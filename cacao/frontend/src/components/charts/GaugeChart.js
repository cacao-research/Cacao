const { createElement: h } = React;

export function GaugeChart({ props }) {
  const pct = (props.value / (props.maxValue || 100)) * 100;
  const angle = (pct / 100) * 180;

  return h('div', { className: 'gauge-container' }, [
    h('svg', { className: 'gauge-svg', viewBox: '0 0 120 80', key: 'svg' }, [
      h('defs', { key: 'defs' }, h('linearGradient', { id: 'gaugeGradient2', x1: '0%', y1: '0%', x2: '100%', y2: '0%' }, [
        h('stop', { offset: '0%', stopColor: 'var(--gradient-start)', key: 's1' }),
        h('stop', { offset: '100%', stopColor: 'var(--gradient-end)', key: 's2' })
      ])),
      h('path', { d: 'M10 70 A50 50 0 0 1 110 70', fill: 'none', stroke: 'var(--bg-tertiary)', strokeWidth: 12, strokeLinecap: 'round', key: 'bg' }),
      h('path', { d: 'M10 70 A50 50 0 0 1 110 70', fill: 'none', stroke: 'url(#gaugeGradient2)', strokeWidth: 12, strokeLinecap: 'round', strokeDasharray: ((angle / 180) * 157) + ' 157', key: 'fill' })
    ]),
    h('div', { className: 'gauge-value', key: 'value' }, props.format ? props.format.replace('{value}', props.value) : props.value + '%'),
    props.title && h('div', { className: 'gauge-title', key: 'title' }, props.title)
  ]);
}
