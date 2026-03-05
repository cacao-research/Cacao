/**
 * Hero - Full-width banner section with centered content
 */

const { createElement: h } = React;

export function Hero({ props, children }) {
  const { title, subtitle, background, image, height = '400px', align = 'center', gradient } = props;

  const style = { minHeight: height };

  if (image) {
    style.backgroundImage = 'url(' + image + ')';
    style.backgroundSize = 'cover';
    style.backgroundPosition = 'center';
  }

  if (gradient) {
    const existing = style.backgroundImage || '';
    const grad = 'linear-gradient(' + gradient + ')';
    style.backgroundImage = existing ? grad + ', ' + existing : grad;
  } else if (image) {
    // Default overlay for readability
    style.backgroundImage = 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.6)), ' + style.backgroundImage;
  }

  if (background && !image && !gradient) {
    style.background = background;
  }

  return h('div', {
    className: 'c-hero c-hero--' + align,
    style,
  }, [
    h('div', { key: 'content', className: 'c-hero-content' }, [
      title && h('h1', { key: 'title', className: 'c-hero-title' }, title),
      subtitle && h('p', { key: 'subtitle', className: 'c-hero-subtitle' }, subtitle),
      children && children.length > 0 && h('div', { key: 'actions', className: 'c-hero-actions' }, children),
    ]),
  ]);
}
