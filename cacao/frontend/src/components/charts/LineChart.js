const { createElement: h } = React;
import { COLORS } from '../core/constants.js';
import { ChartWrapper } from '../core/ChartWrapper.js';

export function LineChart({ props }) {
  const data = props.data || [];
  const yKeys = props.yFields || [];
  const xField = props.xField;

  const chartData = {
    labels: data.map(d => d[xField]),
    datasets: yKeys.map((k, i) => ({
      label: k,
      data: data.map(d => d[k]),
      borderColor: COLORS[i % COLORS.length],
      backgroundColor: props.area ? COLORS[i % COLORS.length] + '40' : 'transparent',
      fill: props.area,
      tension: props.smooth ? 0.4 : 0
    }))
  };

  return h(ChartWrapper, { type: 'line', data: chartData, height: props.height });
}
