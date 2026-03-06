/**
 * VirtualList - Windowed rendering for large lists
 * Only renders visible items + buffer for performance
 */

const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';
import { renderComponent } from '../renderer.js';

export function VirtualList({ props, setActiveTab, activeTab }) {
  const {
    signal,
    row_height = 40,
    height = '400px',
    render_as = 'Card',
    buffer = 5,
    gap = 0,
  } = props;

  const containerRef = useRef(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [items, setItems] = useState([]);

  // Subscribe to signal for items
  useEffect(() => {
    const update = (signals) => {
      if (signal && signals[signal]) {
        setItems(signals[signal]);
      }
    };
    // Initial value
    const initial = cacaoWs.getSignal(signal);
    if (initial) setItems(initial);

    return cacaoWs.subscribe(update);
  }, [signal]);

  const handleScroll = useCallback((e) => {
    setScrollTop(e.target.scrollTop);
  }, []);

  const effectiveRowHeight = row_height + gap;
  const containerHeight = containerRef.current?.clientHeight || parseInt(height) || 400;
  const totalHeight = items.length * effectiveRowHeight;
  const startIndex = Math.max(0, Math.floor(scrollTop / effectiveRowHeight) - buffer);
  const visibleCount = Math.ceil(containerHeight / effectiveRowHeight) + buffer * 2;
  const endIndex = Math.min(items.length, startIndex + visibleCount);

  const renderers = window.Cacao?.renderers || {};
  const visibleItems = [];

  for (let i = startIndex; i < endIndex; i++) {
    const item = items[i];
    if (!item) continue;

    // Build a component definition for each item
    const compDef = {
      type: render_as,
      props: typeof item === 'object' ? item : { value: item },
      children: [],
    };

    visibleItems.push(
      h('div', {
        key: i,
        style: {
          position: 'absolute',
          top: i * effectiveRowHeight,
          left: 0,
          right: 0,
          height: row_height,
        },
      }, renderComponent(compDef, i, setActiveTab, activeTab, renderers))
    );
  }

  return h('div', {
    ref: containerRef,
    className: 'virtual-list',
    style: { height, overflow: 'auto', position: 'relative' },
    onScroll: handleScroll,
  },
    h('div', {
      style: { height: totalHeight, position: 'relative' },
    }, visibleItems)
  );
}
