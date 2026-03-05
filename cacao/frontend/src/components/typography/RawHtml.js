/**
 * RawHtml component - renders raw HTML content with zero styling
 */

const { createElement: h } = React;

export function RawHtml({ props }) {
  const { content } = props;

  return h('div', {
    className: 'raw-html',
    dangerouslySetInnerHTML: { __html: content || '' }
  });
}
