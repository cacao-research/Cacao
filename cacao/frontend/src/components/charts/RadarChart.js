const { createElement: h } = React;
import { COLORS } from '../core/constants.js';
import { ChartWrapper } from '../core/ChartWrapper.js';

export function RadarChart({ props }) {
  const data = props.data || [];
  const valueFields = props.valueFields || [];

  const chartData = {
    labels: data.map(d => d[props.categoryField]),
    datasets: valueFields.map((k, i) => ({
      label: k,
      data: data.map(d => d[k]),
      borderColor: COLORS[i % COLORS.length],
      backgroundColor: COLORS[i % COLORS.length] + '40',
      fill: props.fill
    }))
  };

  return h(ChartWrapper, { type: 'radar', data: chartData, height: props.height });
}
