const { createElement: h } = React;

export function MplChart({ props }) {
  const title = props.title;
  const format = props.format || 'svg';

  return h('div', { className: 'mpl-chart' }, [
    title && h('div', { className: 'mpl-chart__title', key: 'title' }, title),
    format === 'svg'
      ? h('div', {
          key: 'svg',
          className: 'mpl-chart__content',
          dangerouslySetInnerHTML: { __html: props.svg || '' },
        })
      : h('img', {
          key: 'img',
          className: 'mpl-chart__content',
          src: props.src,
          alt: title || 'Matplotlib figure',
        }),
  ]);
}
