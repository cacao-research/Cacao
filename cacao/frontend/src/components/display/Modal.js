/**
 * Modal / Dialog - Overlay dialog component
 */

const { createElement: h, useState, useEffect, useCallback } = React;

export function Modal({ props, children }) {
  const { title, signal, size = 'md', closeOnBackdrop = true, closeOnEscape = true } = props;

  // For signal-driven mode, we rely on the signal value
  // For non-signal mode, always show (controlled by parent rendering)
  const signalName = signal?.__signal__;
  const [visible, setVisible] = useState(!signalName);

  // Listen for signal changes
  useEffect(() => {
    if (!signalName) return;

    const handleSignal = (e) => {
      if (e.detail?.name === signalName) {
        setVisible(!!e.detail.value);
      }
    };
    window.addEventListener('cacao:signal', handleSignal);
    return () => window.removeEventListener('cacao:signal', handleSignal);
  }, [signalName]);

  const close = useCallback(() => {
    if (signalName) {
      // Send signal update to close
      window.dispatchEvent(new CustomEvent('cacao:set-signal', {
        detail: { name: signalName, value: false }
      }));
    }
    setVisible(false);
  }, [signalName]);

  // ESC key handler
  useEffect(() => {
    if (!visible || !closeOnEscape) return;
    const handler = (e) => { if (e.key === 'Escape') close(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [visible, closeOnEscape, close]);

  if (!visible) return null;

  return h('div', {
    className: 'c-modal-overlay',
    onClick: closeOnBackdrop ? (e) => { if (e.target === e.currentTarget) close(); } : undefined,
  },
    h('div', { className: 'c-modal c-modal--' + size, role: 'dialog', 'aria-modal': true }, [
      (title || true) && h('div', { key: 'header', className: 'c-modal-header' }, [
        title && h('div', { key: 'title', className: 'c-modal-title' }, title),
        h('button', {
          key: 'close',
          className: 'c-modal-close',
          onClick: close,
          'aria-label': 'Close',
        }, '\u00D7'),
      ]),
      h('div', { key: 'body', className: 'c-modal-body' }, children),
    ])
  );
}
