/**
 * Split - Two-pane resizable layout with draggable divider
 */

const { createElement: h, useState, useRef, useCallback, useEffect } = React;

export function Split({ props, children }) {
  const { direction = 'horizontal', defaultSize = 50, minSize = 20, maxSize = 80 } = props;
  const isHorizontal = direction === 'horizontal';
  const [size, setSize] = useState(defaultSize);
  const dragging = useRef(false);
  const containerRef = useRef(null);

  const onMouseDown = useCallback((e) => {
    e.preventDefault();
    dragging.current = true;
    document.body.style.cursor = isHorizontal ? 'col-resize' : 'row-resize';
    document.body.style.userSelect = 'none';
  }, [isHorizontal]);

  useEffect(() => {
    const onMouseMove = (e) => {
      if (!dragging.current || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      let pct;
      if (isHorizontal) {
        pct = ((e.clientX - rect.left) / rect.width) * 100;
      } else {
        pct = ((e.clientY - rect.top) / rect.height) * 100;
      }
      setSize(Math.min(maxSize, Math.max(minSize, pct)));
    };

    const onMouseUp = () => {
      if (dragging.current) {
        dragging.current = false;
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
      }
    };

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
    return () => {
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };
  }, [isHorizontal, minSize, maxSize]);

  const firstChild = children[0] || null;
  const secondChild = children[1] || null;

  const firstStyle = isHorizontal
    ? { width: size + '%', height: '100%' }
    : { height: size + '%', width: '100%' };

  const secondStyle = isHorizontal
    ? { width: (100 - size) + '%', height: '100%' }
    : { height: (100 - size) + '%', width: '100%' };

  return h('div', {
    ref: containerRef,
    className: 'c-split c-split--' + direction,
  }, [
    h('div', { key: 'first', className: 'c-split-pane', style: firstStyle }, firstChild),
    h('div', {
      key: 'handle',
      className: 'c-split-handle c-split-handle--' + direction,
      onMouseDown,
    },
      h('div', { className: 'c-split-handle-bar' })
    ),
    h('div', { key: 'second', className: 'c-split-pane', style: secondStyle }, secondChild),
  ]);
}
