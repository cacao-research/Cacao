const { createElement: h, useState, useMemo } = React;
import { formatValue } from '../core/utils.js';

export function DataFrameView({ props }) {
  const data = props.data || [];
  const columns = props.columns || (data[0] ? Object.keys(data[0]).map(k => ({ key: k, title: k })) : []);
  const colDefs = columns.map(c => typeof c === 'string' ? { key: c, title: c } : c);
  const pageSize = props.pageSize || 25;
  const searchable = props.searchable !== false;
  const sortable = props.sortable !== false;
  const paginate = props.paginate !== false;
  const showDtypes = props.showDtypes !== false;
  const showShape = props.showShape !== false;
  const striped = props.striped !== false;
  const shape = props.shape;
  const framework = props.framework || 'unknown';
  const title = props.title;

  const [search, setSearch] = useState('');
  const [sortCol, setSortCol] = useState(null);
  const [sortDir, setSortDir] = useState('asc');
  const [page, setPage] = useState(0);

  const filtered = useMemo(() => {
    if (!search) return data;
    const q = search.toLowerCase();
    return data.filter(row =>
      colDefs.some(c => String(row[c.key] ?? '').toLowerCase().includes(q))
    );
  }, [data, search, colDefs]);

  const sorted = useMemo(() => {
    if (!sortCol) return filtered;
    return [...filtered].sort((a, b) => {
      const va = a[sortCol], vb = b[sortCol];
      if (va == null && vb == null) return 0;
      if (va == null) return 1;
      if (vb == null) return -1;
      if (typeof va === 'number' && typeof vb === 'number') {
        return sortDir === 'asc' ? va - vb : vb - va;
      }
      const sa = String(va), sb = String(vb);
      return sortDir === 'asc' ? sa.localeCompare(sb) : sb.localeCompare(sa);
    });
  }, [filtered, sortCol, sortDir]);

  const totalPages = paginate ? Math.ceil(sorted.length / pageSize) : 1;
  const pageData = paginate ? sorted.slice(page * pageSize, (page + 1) * pageSize) : sorted;

  const handleSort = (key) => {
    if (!sortable) return;
    if (sortCol === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortCol(key);
      setSortDir('asc');
    }
    setPage(0);
  };

  const dtypeBadgeClass = (dtype) => {
    if (!dtype) return 'df-dtype';
    const d = dtype.toLowerCase();
    if (d.includes('int') || d.includes('float') || d.includes('f64') || d.includes('i64') || d.includes('u')) return 'df-dtype df-dtype--num';
    if (d.includes('bool')) return 'df-dtype df-dtype--bool';
    if (d.includes('date') || d.includes('time')) return 'df-dtype df-dtype--date';
    if (d.includes('str') || d.includes('object') || d.includes('utf8')) return 'df-dtype df-dtype--str';
    return 'df-dtype';
  };

  const frameworkLabel = framework === 'pandas' ? 'pandas' : framework === 'polars' ? 'polars' : null;

  return h('div', { className: 'df-view' }, [
    // Header
    (title || showShape || searchable) && h('div', { className: 'df-header', key: 'header' }, [
      h('div', { className: 'df-header__left', key: 'left' }, [
        title && h('span', { className: 'df-title', key: 'title' }, title),
        frameworkLabel && h('span', { className: 'df-framework', key: 'fw' }, frameworkLabel),
        showShape && shape && h('span', { className: 'df-shape', key: 'shape' },
          `${shape[0].toLocaleString()} rows × ${shape[1]} cols`
        ),
      ]),
      searchable && h('input', {
        key: 'search',
        className: 'df-search',
        type: 'text',
        placeholder: 'Search...',
        value: search,
        onInput: (e) => { setSearch(e.target.value); setPage(0); },
      }),
    ]),

    // Table
    h('div', { className: 'df-table-wrap', key: 'table' },
      h('table', { className: striped ? 'df-table df-table--striped' : 'df-table' }, [
        h('thead', { key: 'head' },
          h('tr', null, colDefs.map(c =>
            h('th', {
              key: c.key,
              className: sortable ? 'df-th df-th--sortable' : 'df-th',
              onClick: () => handleSort(c.key),
            }, [
              h('span', { className: 'df-th__label', key: 'label' }, c.title || c.key),
              sortCol === c.key && h('span', { className: 'df-th__sort', key: 'sort' },
                sortDir === 'asc' ? ' \u25B2' : ' \u25BC'
              ),
              showDtypes && c.dtype && h('span', {
                className: dtypeBadgeClass(c.dtype),
                key: 'dtype',
              }, c.dtype),
            ])
          ))
        ),
        h('tbody', { key: 'body' }, pageData.map((row, i) =>
          h('tr', { key: i }, colDefs.map(c =>
            h('td', { key: c.key, 'data-label': c.title || c.key }, formatValue(row[c.key]))
          ))
        )),
      ])
    ),

    // Footer / Pagination
    paginate && totalPages > 1 && h('div', { className: 'df-footer', key: 'footer' }, [
      h('span', { className: 'df-footer__info', key: 'info' },
        `Showing ${page * pageSize + 1}–${Math.min((page + 1) * pageSize, sorted.length)} of ${sorted.length}`
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
  ]);
}
