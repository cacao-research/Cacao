const { createElement: h } = React;

export function Metric({ props }) {
  return h('div', { className: 'metric' }, [
    h('div', { className: 'metric-label', key: 'label' }, props.label),
    h('div', { className: 'metric-value', key: 'value' }, (props.prefix || '') + props.value + (props.suffix || '')),
    props.trend && h('div', {
      className: 'metric-trend ' + (props.trendDirection || (props.trend.startsWith('+') ? 'up' : 'down')),
      key: 'trend'
    }, (props.trendDirection === 'up' || props.trend.startsWith('+') ? '↑ ' : '↓ ') + props.trend)
  ]);
}
