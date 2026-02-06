const { createElement: h } = React;
import { formatValue } from '../core/utils.js';

export function Table({ props }) {
  const data = props.data || [];
  const columns = props.columns || (data[0] ? Object.keys(data[0]) : []);
  const colDefs = columns.map(c => typeof c === 'string' ? { key: c, title: c } : c);

  return h('div', { className: 'table-container' },
    h('table', null, [
      h('thead', { key: 'head' }, h('tr', null, colDefs.map(c => h('th', { key: c.key }, c.title || c.key)))),
      h('tbody', { key: 'body' }, data.slice(0, props.pageSize || 10).map((row, i) =>
        h('tr', { key: i }, colDefs.map(c => h('td', { key: c.key }, formatValue(row[c.key]))))
      ))
    ])
  );
}
