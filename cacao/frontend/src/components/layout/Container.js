/**
 * Container - Centered max-width content wrapper
 */

const { createElement: h } = React;

export function Container({ props, children }) {
  const { size = 'lg', padding = true, center = true } = props;

  const sizes = {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    full: '100%',
  };

  const style = {
    maxWidth: sizes[size] || sizes.lg,
    width: '100%',
  };

  if (center) {
    style.marginLeft = 'auto';
    style.marginRight = 'auto';
  }

  return h('div', {
    className: 'c-container' + (padding ? ' c-container--padded' : ''),
    style,
  }, children);
}
