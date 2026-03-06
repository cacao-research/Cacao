/**
 * SearchInput - Filterable search input with debounce and signal support
 */

const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';
import { isStaticMode, staticSignals } from '../core/static-runtime.js';

export function SearchInput({ props }) {
  const {
    placeholder = 'Search...',
    signal: signalRef,
    debounce = 300,
    size = 'md',
    clearable = true,
    on_search,
    icon = true,
  } = props;

  const signalName = signalRef?.__signal__;
  const [value, setValue] = useState('');
  const timerRef = useRef(null);
  const inputRef = useRef(null);

  // Sync from signal
  useEffect(() => {
    if (!signalName) return;
    if (isStaticMode()) {
      const initial = staticSignals.get(signalName);
      if (initial !== undefined) setValue(initial);
      return;
    }
    const unsubscribe = cacaoWs.subscribe((signals) => {
      if (signals[signalName] !== undefined) {
        setValue(signals[signalName]);
      }
    });
    const initial = cacaoWs.getSignal(signalName);
    if (initial !== undefined) setValue(initial);
    return unsubscribe;
  }, [signalName]);

  const emitValue = useCallback((val) => {
    if (signalName) {
      if (isStaticMode()) {
        staticSignals.set(signalName, val);
      } else {
        cacaoWs.send({ type: 'signal_update', name: signalName, value: val });
      }
    }
    if (on_search) {
      const eventName = on_search.__event__ || on_search;
      if (isStaticMode()) {
        import('../core/static-runtime.js').then(m => m.staticDispatcher(eventName, { value: val }));
      } else {
        cacaoWs.send({ type: 'event', name: eventName, data: { value: val } });
      }
    }
  }, [signalName, on_search]);

  const handleInput = useCallback((e) => {
    const val = e.target.value;
    setValue(val);
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => emitValue(val), debounce);
  }, [debounce, emitValue]);

  const handleClear = useCallback(() => {
    setValue('');
    emitValue('');
    inputRef.current?.focus();
  }, [emitValue]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Escape' && value) {
      e.preventDefault();
      handleClear();
    }
  }, [value, handleClear]);

  const sizeClass = size !== 'md' ? ' c-search--' + size : '';

  return h('div', { className: 'c-search' + sizeClass }, [
    icon && h('svg', {
      key: 'icon',
      className: 'c-search-icon',
      viewBox: '0 0 16 16',
      fill: 'none',
      stroke: 'currentColor',
      strokeWidth: '1.5',
      width: size === 'sm' ? 12 : 14,
      height: size === 'sm' ? 12 : 14,
    }, h('path', { d: 'M11.5 11.5L14 14M6.5 12A5.5 5.5 0 106.5 1a5.5 5.5 0 000 11z' })),
    h('input', {
      key: 'input',
      ref: inputRef,
      type: 'text',
      className: 'c-search-input',
      placeholder,
      value,
      onInput: handleInput,
      onKeyDown: handleKeyDown,
    }),
    clearable && value && h('button', {
      key: 'clear',
      className: 'c-search-clear',
      onClick: handleClear,
      'aria-label': 'Clear search',
      type: 'button',
    }, '\u00D7'),
  ]);
}
