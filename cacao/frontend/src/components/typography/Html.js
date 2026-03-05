/**
 * Html component - renders raw HTML content safely
 */

const { createElement: h } = React;

export function Html({ props }) {
  const { content } = props;

  return h('div', {
    className: 'html-content',
    dangerouslySetInnerHTML: { __html: content || '' }
  });
}
