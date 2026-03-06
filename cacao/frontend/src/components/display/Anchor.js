/**
 * Anchor - Invisible anchor point for deep linking
 *
 * Renders an element with an id that can be scrolled to via URL hash.
 * Supports #anchor-id in the URL to auto-scroll on page load.
 */

const { createElement: h, useEffect, useRef } = React;

export function Anchor({ props }) {
  const { id, offset = 0 } = props;
  const ref = useRef(null);

  // Auto-scroll on mount if URL hash matches
  useEffect(() => {
    if (!id) return;
    const hash = window.location.hash;
    // Support both #id and #/page#id formats
    const target = hash.includes('#') ? hash.split('#').pop() : '';
    if (target === id) {
      // Delay to let page render
      setTimeout(() => {
        if (ref.current) {
          const top = ref.current.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
        }
      }, 100);
    }
  }, [id, offset]);

  return h('div', {
    ref,
    id,
    className: 'c-anchor',
    'aria-hidden': 'true',
  });
}
