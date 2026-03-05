/**
 * Html component - renders pre-rendered HTML with prose styling
 *
 * Use this when you already have HTML content that needs
 * the same typography treatment as the Markdown component.
 * For raw HTML injection without styling, use RawHtml.
 */

const { createElement: h, useRef, useEffect } = React;

/**
 * Attach copy button handlers to code blocks within the content
 */
function attachCopyHandlers(container) {
  const buttons = container.querySelectorAll('.c-code-copy');
  for (const btn of buttons) {
    if (btn.dataset.bound) return;
    btn.dataset.bound = 'true';
    btn.addEventListener('click', () => {
      const code = btn.closest('pre').querySelector('code');
      if (!code) return;
      navigator.clipboard.writeText(code.textContent).then(() => {
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
      }).catch(() => {
        btn.textContent = 'Failed';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
      });
    });
  }
}

export function Html({ props }) {
  const { content } = props;
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      attachCopyHandlers(containerRef.current);
    }
  }, [content]);

  return h('div', {
    ref: containerRef,
    className: 'prose',
    dangerouslySetInnerHTML: { __html: content || '' }
  });
}
