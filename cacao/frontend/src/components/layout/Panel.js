/**
 * Panel - Draggable, resizable floating panel (window)
 */

const { createElement: h, useState, useRef, useCallback, useEffect } = React;
import { renderComponent } from '../renderer.js';

export function Panel({ props, children, setActiveTab, activeTab }) {
  const {
    title = 'Panel',
    width = '400px',
    height = '300px',
    draggable = true,
    resizable = true,
    closable = true,
    minimizable = true,
    maximizable = true,
    signal,
    x,
    y,
  } = props;

  const panelRef = useRef(null);
  const [pos, setPos] = useState({ x: x ?? 100, y: y ?? 100 });
  const [size, setSize] = useState({ w: parseInt(width), h: parseInt(height) });
  const [minimized, setMinimized] = useState(false);
  const [maximized, setMaximized] = useState(false);
  const [visible, setVisible] = useState(true);
  const dragRef = useRef(null);
  const resizeRef = useRef(null);

  // Bring to front on click
  const bringToFront = useCallback(() => {
    if (window.CacaoPanelManager) {
      window.CacaoPanelManager.bringToFront(panelRef.current);
    }
  }, []);

  // Drag handlers
  const onDragStart = useCallback((e) => {
    if (!draggable || maximized) return;
    e.preventDefault();
    bringToFront();
    const startX = e.clientX - pos.x;
    const startY = e.clientY - pos.y;

    const onMove = (e) => {
      setPos({ x: e.clientX - startX, y: Math.max(0, e.clientY - startY) });
    };
    const onUp = () => {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup', onUp);
    };
    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup', onUp);
  }, [draggable, maximized, pos, bringToFront]);

  // Resize handlers
  const onResizeStart = useCallback((e, direction) => {
    if (!resizable || maximized) return;
    e.preventDefault();
    e.stopPropagation();
    bringToFront();
    const startX = e.clientX;
    const startY = e.clientY;
    const startW = size.w;
    const startH = size.h;
    const startPosX = pos.x;
    const startPosY = pos.y;

    const onMove = (e) => {
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      const newSize = { ...size };
      const newPos = { ...pos };

      if (direction.includes('e')) newSize.w = Math.max(200, startW + dx);
      if (direction.includes('s')) newSize.h = Math.max(150, startH + dy);
      if (direction.includes('w')) {
        newSize.w = Math.max(200, startW - dx);
        newPos.x = startPosX + dx;
      }
      if (direction.includes('n')) {
        newSize.h = Math.max(150, startH - dy);
        newPos.y = startPosY + dy;
      }
      setSize(newSize);
      setPos(newPos);
    };
    const onUp = () => {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup', onUp);
    };
    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup', onUp);
  }, [resizable, maximized, size, pos, bringToFront]);

  const toggleMaximize = useCallback(() => {
    setMaximized(prev => !prev);
  }, []);

  if (!visible) return null;

  const style = maximized
    ? { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, width: '100vw', height: '100vh', zIndex: 'var(--panel-z, 900)' }
    : { position: 'absolute', left: pos.x, top: pos.y, width: size.w, height: minimized ? 'auto' : size.h, zIndex: 'var(--panel-z, 900)' };

  const resizeHandles = resizable && !maximized && !minimized ? [
    h('div', { key: 'r-e', className: 'panel-resize panel-resize-e', onPointerDown: (e) => onResizeStart(e, 'e') }),
    h('div', { key: 'r-s', className: 'panel-resize panel-resize-s', onPointerDown: (e) => onResizeStart(e, 's') }),
    h('div', { key: 'r-se', className: 'panel-resize panel-resize-se', onPointerDown: (e) => onResizeStart(e, 'se') }),
    h('div', { key: 'r-w', className: 'panel-resize panel-resize-w', onPointerDown: (e) => onResizeStart(e, 'w') }),
    h('div', { key: 'r-n', className: 'panel-resize panel-resize-n', onPointerDown: (e) => onResizeStart(e, 'n') }),
  ] : [];

  return h('div', {
    ref: panelRef,
    className: 'panel' + (minimized ? ' minimized' : '') + (maximized ? ' maximized' : ''),
    style,
    onPointerDown: bringToFront,
  }, [
    // Title bar
    h('div', {
      key: 'titlebar',
      className: 'panel-titlebar',
      onPointerDown: onDragStart,
    }, [
      h('span', { key: 'title', className: 'panel-title' }, title),
      h('div', { key: 'controls', className: 'panel-controls' }, [
        minimizable && h('button', {
          key: 'min',
          className: 'panel-btn',
          onClick: (e) => { e.stopPropagation(); setMinimized(!minimized); },
          'aria-label': 'Minimize',
        }, '\u2013'),
        maximizable && h('button', {
          key: 'max',
          className: 'panel-btn',
          onClick: (e) => { e.stopPropagation(); toggleMaximize(); },
          'aria-label': maximized ? 'Restore' : 'Maximize',
        }, maximized ? '\u2752' : '\u25a1'),
        closable && h('button', {
          key: 'close',
          className: 'panel-btn panel-btn-close',
          onClick: (e) => { e.stopPropagation(); setVisible(false); },
          'aria-label': 'Close',
        }, '\u00d7'),
      ]),
    ]),
    // Content
    !minimized && h('div', { key: 'content', className: 'panel-content' }, children),
    // Resize handles
    ...resizeHandles,
  ]);
}
