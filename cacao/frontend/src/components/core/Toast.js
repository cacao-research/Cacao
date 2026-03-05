/**
 * Toast Notification System
 * Displays transient messages from server or client-side events
 */

const { createElement: h, useState, useEffect, useCallback, useRef } = React;

let _addToast = null;
let _toastId = 0;

/**
 * Show a toast notification.
 * @param {string} message - The message to display
 * @param {object} options - { type: 'info'|'success'|'warning'|'error', duration: ms }
 */
export function showToast(message, options = {}) {
  const { type = 'info', duration = 4000 } = options;
  if (_addToast) {
    _addToast({ id: ++_toastId, message, type, duration });
  }
}

// Expose globally for server-side toast events
window.CacaoToast = { show: showToast };

export function ToastContainer() {
  const [toasts, setToasts] = useState([]);
  const timersRef = useRef({});

  // Expose addToast globally
  useEffect(() => {
    _addToast = (toast) => {
      setToasts(prev => [...prev, toast]);
      // Auto-dismiss after duration
      if (toast.duration > 0) {
        timersRef.current[toast.id] = setTimeout(() => {
          dismissToast(toast.id);
        }, toast.duration);
      }
    };
    return () => { _addToast = null; };
  }, []);

  const dismissToast = useCallback((id) => {
    // Start exit animation
    setToasts(prev => prev.map(t =>
      t.id === id ? { ...t, exiting: true } : t
    ));
    // Remove after animation
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 150);
    // Clear timer
    if (timersRef.current[id]) {
      clearTimeout(timersRef.current[id]);
      delete timersRef.current[id];
    }
  }, []);

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      Object.values(timersRef.current).forEach(clearTimeout);
    };
  }, []);

  if (toasts.length === 0) return null;

  return h('div', { className: 'toast-container', 'aria-live': 'polite', 'aria-label': 'Notifications' },
    toasts.map(toast =>
      h('div', {
        key: toast.id,
        className: 'toast toast-' + toast.type + (toast.exiting ? ' exiting' : ''),
        role: 'status',
      }, [
        h('span', { key: 'msg', className: 'toast-message' }, toast.message),
        h('button', {
          key: 'close',
          className: 'toast-close',
          onClick: () => dismissToast(toast.id),
          'aria-label': 'Dismiss',
        }, '\u00d7'),
      ])
    )
  );
}
