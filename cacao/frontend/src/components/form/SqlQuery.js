const { createElement: h, useState, useCallback, useEffect, useRef } = React;
import { formatValue } from '../core/utils.js';
import { cacaoWs } from '../core/websocket.js';

export function SqlQuery({ props }) {
  const title = props.title;
  const editable = props.editable !== false;
  const autoRun = props.autoRun || false;
  const pageSize = props.pageSize || 25;
  const initialQuery = props.query || '';

  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState(null);
  const [columns, setColumns] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const ranAutoRun = useRef(false);

  const runQuery = useCallback(() => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);

    cacaoWs.send({
      type: 'sql_query',
      connection: props.connection,
      connType: props.connType,
      query: query.trim(),
      maxRows: props.maxRows || 1000,
    });
  }, [query, props.connection, props.connType, props.maxRows]);

  // Listen for query results from server
  useEffect(() => {
    const handler = (msg) => {
      if (msg.type === 'sql:result') {
        setResults(msg.data || []);
        setColumns(msg.columns || []);
        setError(null);
        setLoading(false);
        setPage(0);
      } else if (msg.type === 'sql:error') {
        setError(msg.error || 'Unknown error');
        setResults(null);
        setLoading(false);
      }
    };
    cacaoWs.addListener(handler);
    return () => cacaoWs.removeListener(handler);
  }, []);

  // Auto-run on mount
  useEffect(() => {
    if (autoRun && initialQuery.trim() && !ranAutoRun.current) {
      ranAutoRun.current = true;
      // Small delay to ensure WebSocket is connected
      setTimeout(() => runQuery(), 300);
    }
  }, [autoRun, initialQuery, runQuery]);

  const totalPages = results ? Math.ceil(results.length / pageSize) : 0;
  const pageData = results ? results.slice(page * pageSize, (page + 1) * pageSize) : [];

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      runQuery();
    }
  };

  return h('div', { className: 'sql-query' }, [
    title && h('div', { className: 'sql-query__title', key: 'title' }, title),

    h('div', { className: 'sql-query__editor', key: 'editor' }, [
      h('textarea', {
        key: 'textarea',
        className: 'sql-query__input',
        value: query,
        readOnly: !editable,
        onInput: (e) => setQuery(e.target.value),
        onKeyDown: handleKeyDown,
        placeholder: 'SELECT * FROM ...',
        rows: Math.min(query.split('\n').length + 1, 12),
        spellCheck: false,
      }),
      h('div', { className: 'sql-query__actions', key: 'actions' }, [
        h('button', {
          key: 'run',
          className: 'sql-query__run-btn',
          onClick: runQuery,
          disabled: loading || !query.trim(),
        }, loading ? 'Running...' : '\u25B6 Run'),
        h('span', { key: 'hint', className: 'sql-query__hint' }, 'Ctrl+Enter to run'),
      ]),
    ]),

    error && h('div', { className: 'sql-query__error', key: 'error' }, error),

    results && h('div', { className: 'sql-query__results', key: 'results' }, [
      h('div', { className: 'sql-query__results-info', key: 'info' },
        `${results.length} row${results.length !== 1 ? 's' : ''} returned`
      ),
      h('div', { className: 'df-table-wrap', key: 'table' },
        h('table', { className: 'df-table df-table--striped' }, [
          h('thead', { key: 'head' },
            h('tr', null, columns.map(c =>
              h('th', { key: c, className: 'df-th' }, c)
            ))
          ),
          h('tbody', { key: 'body' }, pageData.map((row, i) =>
            h('tr', { key: i }, columns.map(c =>
              h('td', { key: c }, formatValue(row[c]))
            ))
          )),
        ])
      ),
      totalPages > 1 && h('div', { className: 'df-footer', key: 'footer' }, [
        h('span', { className: 'df-footer__info', key: 'info' },
          `Showing ${page * pageSize + 1}\u2013${Math.min((page + 1) * pageSize, results.length)} of ${results.length}`
        ),
        h('div', { className: 'df-pagination', key: 'pages' }, [
          h('button', {
            key: 'prev',
            className: 'df-page-btn',
            disabled: page === 0,
            onClick: () => setPage(p => p - 1),
          }, '\u2190'),
          h('span', { key: 'current', className: 'df-page-info' }, `${page + 1} / ${totalPages}`),
          h('button', {
            key: 'next',
            className: 'df-page-btn',
            disabled: page >= totalPages - 1,
            onClick: () => setPage(p => p + 1),
          }, '\u2192'),
        ]),
      ]),
    ]),
  ]);
}
