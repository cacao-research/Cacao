const { createElement: h, useRef, useEffect, useState } = React;

const PLOTLY_CDN = 'https://cdn.plot.ly/plotly-2.35.2.min.js';

let plotlyLoaded = false;
let plotlyLoading = false;
const plotlyCallbacks = [];

function loadPlotly() {
  if (plotlyLoaded) return Promise.resolve();
  if (plotlyLoading) {
    return new Promise(resolve => plotlyCallbacks.push(resolve));
  }
  plotlyLoading = true;
  return new Promise((resolve, reject) => {
    plotlyCallbacks.push(resolve);
    const script = document.createElement('script');
    script.src = PLOTLY_CDN;
    script.onload = () => {
      plotlyLoaded = true;
      plotlyLoading = false;
      plotlyCallbacks.forEach(cb => cb());
      plotlyCallbacks.length = 0;
    };
    script.onerror = () => {
      plotlyLoading = false;
      reject(new Error('Failed to load Plotly.js'));
    };
    document.head.appendChild(script);
  });
}

export function PlotlyChart({ props }) {
  const containerRef = useRef(null);
  const [ready, setReady] = useState(plotlyLoaded);
  const figure = props.figure || {};
  const height = props.height || 400;
  const responsive = props.responsive !== false;
  const config = props.config || {};

  useEffect(() => {
    if (!plotlyLoaded) {
      loadPlotly().then(() => setReady(true));
    }
  }, []);

  useEffect(() => {
    if (!ready || !containerRef.current || !window.Plotly) return;

    const plotData = figure.data || [];
    const plotLayout = {
      ...(figure.layout || {}),
      height,
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim() || '#ccc' },
      margin: figure.layout?.margin || { l: 50, r: 30, t: 40, b: 40 },
    };

    const plotConfig = {
      responsive,
      displayModeBar: 'hover',
      ...config,
    };

    window.Plotly.react(containerRef.current, plotData, plotLayout, plotConfig);

    return () => {
      if (containerRef.current && window.Plotly) {
        window.Plotly.purge(containerRef.current);
      }
    };
  }, [ready, figure, height, responsive, config]);

  if (!ready) {
    return h('div', { className: 'plotly-chart plotly-chart--loading' },
      h('span', { className: 'plotly-chart__spinner' }, 'Loading Plotly...')
    );
  }

  return h('div', { className: 'plotly-chart' },
    h('div', { ref: containerRef, style: { width: '100%', minHeight: height } })
  );
}
