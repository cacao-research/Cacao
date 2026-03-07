/**
 * Error Overlay for Cacao dev mode.
 * Shows server-side errors as a browser overlay with friendly messages,
 * suggestions, and collapsible tracebacks.
 */

const { createElement: h, useState, useEffect, useCallback } = React;

export function ErrorOverlay() {
  const [errors, setErrors] = useState([]);
  const [collapsed, setCollapsed] = useState({});

  const addError = useCallback((err) => {
    setErrors(prev => {
      const next = [...prev, { ...err, id: Date.now() + Math.random() }];
      // Keep at most 10 errors
      return next.slice(-10);
    });
  }, []);

  const dismissError = useCallback((id) => {
    setErrors(prev => prev.filter(e => e.id !== id));
  }, []);

  const dismissAll = useCallback(() => {
    setErrors([]);
  }, []);

  const toggleTraceback = useCallback((id) => {
    setCollapsed(prev => ({ ...prev, [id]: !prev[id] }));
  }, []);

  // Listen for server:error messages and page-level errors
  useEffect(() => {
    // Expose the addError function for websocket handler
    window.__CACAO_ERROR_OVERLAY__ = { addError };

    return () => {
      delete window.__CACAO_ERROR_OVERLAY__;
    };
  }, [addError]);

  if (!errors.length) return null;

  return h('div', { className: 'cacao-error-overlay' },
    h('div', { className: 'cacao-error-overlay__header' },
      h('span', { className: 'cacao-error-overlay__badge' }, errors.length),
      h('span', null, 'Server Error' + (errors.length > 1 ? 's' : '')),
      h('div', { className: 'cacao-error-overlay__actions' },
        errors.length > 1 && h('button', {
          className: 'cacao-error-overlay__btn',
          onClick: dismissAll,
        }, 'Dismiss All'),
        h('button', {
          className: 'cacao-error-overlay__close',
          onClick: dismissAll,
          title: 'Close overlay',
        }, '\u00D7'),
      ),
    ),
    h('div', { className: 'cacao-error-overlay__list' },
      errors.map(err =>
        h('div', { key: err.id, className: 'cacao-error-overlay__item' },
          h('div', { className: 'cacao-error-overlay__item-header' },
            h('span', { className: 'cacao-error-overlay__item-type' }, err.title || err.type || 'Error'),
            h('button', {
              className: 'cacao-error-overlay__item-dismiss',
              onClick: () => dismissError(err.id),
            }, '\u00D7'),
          ),
          h('p', { className: 'cacao-error-overlay__item-message' }, err.message),
          err.suggestion && h('p', { className: 'cacao-error-overlay__item-suggestion' }, err.suggestion),
          err.context && h('p', { className: 'cacao-error-overlay__item-context' },
            'While: ', err.context,
          ),
          err.traceback && h('div', { className: 'cacao-error-overlay__traceback-toggle' },
            h('button', {
              className: 'cacao-error-overlay__btn cacao-error-overlay__btn--small',
              onClick: () => toggleTraceback(err.id),
            }, collapsed[err.id] ? 'Hide Traceback' : 'Show Traceback'),
            collapsed[err.id] && h('pre', { className: 'cacao-error-overlay__traceback' }, err.traceback),
          ),
        )
      ),
    ),
  );
}
