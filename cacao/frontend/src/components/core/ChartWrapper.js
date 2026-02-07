/**
 * Chart.js wrapper component
 */

const { createElement: h, useEffect, useRef } = React;

export function ChartWrapper({ type, data, options, height }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data) return;
    if (chartRef.current) chartRef.current.destroy();

    const ctx = canvasRef.current.getContext('2d');
    Chart.defaults.color = '#c4a98a';
    Chart.defaults.borderColor = 'rgba(139, 115, 85, 0.2)';

    chartRef.current = new Chart(ctx, {
      type,
      data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: data.datasets?.length > 1 } },
        ...options
      }
    });

    return () => { if (chartRef.current) chartRef.current.destroy(); };
  }, [type, JSON.stringify(data)]);

  return h('div', { style: { height: height || 300, width: '100%' } },
    h('canvas', { ref: canvasRef })
  );
}
