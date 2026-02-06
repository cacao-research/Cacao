const { createElement: h } = React;
import { COLORS } from '../core/constants.js';
import { ChartWrapper } from '../core/ChartWrapper.js';

export function BarChart({ props }) {
  const data = props.data || [];
  const yKeys = props.yFields || [];
  const xField = props.xField;

  const chartData = {
    labels: data.map(d => d[xField]),
    datasets: yKeys.map((k, i) => ({
      label: k,
      data: data.map(d => d[k]),
      backgroundColor: COLORS[i % COLORS.length]
    }))
  };

  return h(ChartWrapper, {
    type: 'bar',
    data: chartData,
    height: props.height,
    options: { indexAxis: props.horizontal ? 'y' : 'x' }
  });
}
