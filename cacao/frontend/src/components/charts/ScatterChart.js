const { createElement: h } = React;
import { COLORS } from '../core/constants.js';
import { ChartWrapper } from '../core/ChartWrapper.js';

export function ScatterChart({ props }) {
  const data = props.data || [];

  const chartData = {
    datasets: [{
      label: 'Data',
      data: data.map(d => ({ x: d[props.xField], y: d[props.yField] })),
      backgroundColor: COLORS[0]
    }]
  };

  return h(ChartWrapper, { type: 'scatter', data: chartData, height: props.height });
}
