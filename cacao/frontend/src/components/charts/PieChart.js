const { createElement: h } = React;
import { COLORS } from '../core/constants.js';
import { ChartWrapper } from '../core/ChartWrapper.js';

export function PieChart({ props }) {
  const data = props.data || [];

  const chartData = {
    labels: data.map(d => d[props.nameField]),
    datasets: [{
      data: data.map(d => d[props.valueField]),
      backgroundColor: COLORS.slice(0, data.length)
    }]
  };

  return h(ChartWrapper, {
    type: props.donut ? 'doughnut' : 'pie',
    data: chartData,
    height: props.height
  });
}
