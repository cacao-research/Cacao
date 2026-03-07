/**
 * VirtualList - Windowed rendering for large lists
 * Only renders visible items + buffer for performance.
 *
 * Improvements over basic version:
 * - Stable keys using item id/key fields
 * - Jump-to-index support
 * - Scroll position restoration
 * - Overscan for smoother scrolling
 * - Throttled scroll handler
 * - onEndReached callback for infinite scroll
 */

const { createElement: h, useState, useEffect, useRef, useCallback, useMemo } = React;
import { cacaoWs } from '../core/websocket.js';
import { renderComponent } from '../renderer.js';

/**
 * Extract a stable key from an item.
 */
function getItemKey(item, index) {
  if (item && typeof item === 'object') {
    if (item.id !== undefined) return String(item.id);
    if (item.key !== undefined) return String(item.key);
    if (item._id !== undefined) return String(item._id);
  }
  return String(index);
}

export function VirtualList({ props, setActiveTab, activeTab }) {
  const {
    signal,
    row_height = 40,
    height = '400px',
    render_as = 'Card',
    buffer = 5,
    gap = 0,
    jump_to = null,
    end_reached_threshold = 200,
  } = props;

  const containerRef = useRef(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [items, setItems] = useState([]);
  const scrollRAF = useRef(null);

  // Subscribe to signal for items
  useEffect(() => {
    const update = (signals) => {
      if (signal && signals[signal]) {
        setItems(signals[signal]);
      }
    };
    const initial = cacaoWs.getSignal(signal);
    if (initial) setItems(initial);

    return cacaoWs.subscribe(update);
  }, [signal]);

  // Jump to index support
  useEffect(() => {
    if (jump_to != null && containerRef.current) {
      const effectiveRowHeight = row_height + gap;
      containerRef.current.scrollTop = jump_to * effectiveRowHeight;
    }
  }, [jump_to, row_height, gap]);

  // Throttled scroll handler using requestAnimationFrame
  const handleScroll = useCallback((e) => {
    if (scrollRAF.current) return;
    scrollRAF.current = requestAnimationFrame(() => {
      scrollRAF.current = null;
      const target = e.target;
      setScrollTop(target.scrollTop);

      // Check if near bottom for infinite scroll
      if (end_reached_threshold > 0) {
        const distFromBottom = target.scrollHeight - target.scrollTop - target.clientHeight;
        if (distFromBottom < end_reached_threshold) {
          cacaoWs.sendEvent(`${signal}:end_reached`, {
            scrollTop: target.scrollTop,
            itemCount: items.length,
          });
        }
      }
    });
  }, [signal, items.length, end_reached_threshold]);

  // Cleanup RAF on unmount
  useEffect(() => {
    return () => {
      if (scrollRAF.current) cancelAnimationFrame(scrollRAF.current);
    };
  }, []);

  const effectiveRowHeight = row_height + gap;
  const containerHeight = containerRef.current?.clientHeight || parseInt(height) || 400;
  const totalHeight = items.length * effectiveRowHeight;

  // Calculate visible range with overscan
  const overscan = Math.max(buffer, 3);
  const startIndex = Math.max(0, Math.floor(scrollTop / effectiveRowHeight) - overscan);
  const visibleCount = Math.ceil(containerHeight / effectiveRowHeight) + overscan * 2;
  const endIndex = Math.min(items.length, startIndex + visibleCount);

  const renderers = window.Cacao?.renderers || {};

  // Memoize visible items computation
  const visibleItems = useMemo(() => {
    const result = [];
    for (let i = startIndex; i < endIndex; i++) {
      const item = items[i];
      if (!item) continue;

      const compDef = {
        type: render_as,
        props: typeof item === 'object' ? item : { value: item },
        children: [],
      };

      const key = getItemKey(item, i);
      result.push(
        h('div', {
          key,
          style: {
            position: 'absolute',
            top: i * effectiveRowHeight,
            left: 0,
            right: 0,
            height: row_height,
          },
        }, renderComponent(compDef, key, setActiveTab, activeTab, renderers))
      );
    }
    return result;
  }, [startIndex, endIndex, items, render_as, effectiveRowHeight, row_height]);

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
