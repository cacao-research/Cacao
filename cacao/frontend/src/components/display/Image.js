/**
 * Image - Image display with caption and lightbox
 */

const { createElement: h, useState, useRef, useEffect } = React;

export function Image({ props }) {
  const { src, alt = '', caption, width, height, lightbox = false, lazy = true } = props;
  const [showLightbox, setShowLightbox] = useState(false);
  const [loaded, setLoaded] = useState(!lazy);
  const imgRef = useRef(null);

  // Lazy loading with IntersectionObserver
  useEffect(() => {
    if (!lazy || loaded) return;
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setLoaded(true);
        observer.disconnect();
      }
    }, { rootMargin: '200px' });

    if (imgRef.current) observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, [lazy, loaded]);

  // ESC to close lightbox
  useEffect(() => {
    if (!showLightbox) return;
    const handler = (e) => { if (e.key === 'Escape') setShowLightbox(false); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [showLightbox]);

  const imgStyle = {};
  if (width) imgStyle.width = typeof width === 'number' ? width + 'px' : width;
  if (height) imgStyle.height = typeof height === 'number' ? height + 'px' : height;

  return h('figure', { className: 'c-image', ref: imgRef }, [
    loaded
      ? h('img', {
          key: 'img',
          src,
          alt,
          style: imgStyle,
          className: 'c-image-img' + (lightbox ? ' c-image-img--clickable' : ''),
          onClick: lightbox ? () => setShowLightbox(true) : undefined,
          loading: lazy ? 'lazy' : undefined,
        })
      : h('div', { key: 'placeholder', className: 'c-image-placeholder', style: imgStyle }),
    caption && h('figcaption', { key: 'caption', className: 'c-image-caption' }, caption),
    showLightbox && h('div', {
      key: 'lightbox',
      className: 'c-image-lightbox',
      onClick: () => setShowLightbox(false),
    }, [
      h('img', { key: 'lbimg', src, alt, className: 'c-image-lightbox-img' }),
      h('button', {
        key: 'close',
        className: 'c-image-lightbox-close',
        onClick: () => setShowLightbox(false),
        'aria-label': 'Close',
      }, '\u00D7'),
    ]),
  ]);
}
