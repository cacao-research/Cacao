/**
 * JsonView - Interactive JSON tree viewer
 */

const { createElement: h, useState } = React;

function formatValue(value) {
  if (value === null) return 'null';
  if (value === undefined) return 'undefined';
  if (typeof value === 'string') return `"${value}"`;
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  return String(value);
}

function JsonNode({ name, value, depth = 0, expanded: defaultExpanded }) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  const type = Array.isArray(value) ? 'array' : typeof value;
  const isExpandable = type === 'object' || type === 'array';
  const isEmpty = isExpandable && Object.keys(value || {}).length === 0;

  const indent = { paddingLeft: `${depth * 16}px` };

  // Render primitive values
  if (!isExpandable || value === null) {
    return h('div', { className: 'json-node json-leaf', style: indent },
      name !== null && h('span', { className: 'json-key' }, `"${name}": `),
      h('span', { className: `json-value json-${type === 'object' ? 'null' : type}` },
        formatValue(value)
      )
    );
  }

  // Render expandable nodes (objects/arrays)
  const entries = Object.entries(value);
  const bracket = type === 'array' ? ['[', ']'] : ['{', '}'];

  return h('div', { className: 'json-node' }, [
    h('div', {
      className: 'json-expandable',
      style: indent,
      onClick: () => setIsExpanded(!isExpanded),
      key: 'header'
    }, [
      h('span', { className: 'json-toggle', key: 'toggle' }, isExpanded ? '\u25bc' : '\u25b6'),
      name !== null && h('span', { className: 'json-key', key: 'key' }, `"${name}": `),
      h('span', { className: 'json-bracket', key: 'open' }, bracket[0]),
      !isExpanded && h('span', { className: 'json-collapsed', key: 'dots' },
        isEmpty ? '' : `... ${entries.length} ${type === 'array' ? 'items' : 'keys'}`
      ),
      !isExpanded && h('span', { className: 'json-bracket', key: 'close' }, bracket[1]),
    ]),
    isExpanded && entries.map(([k, v], i) =>
      h(JsonNode, {
        key: k,
        name: type === 'array' ? null : k,
        value: v,
        depth: depth + 1,
        expanded: defaultExpanded
      })
    ),
    isExpanded && h('div', { style: indent, key: 'closing' },
      h('span', { className: 'json-bracket' }, bracket[1])
    )
  ]);
}

export function JsonView({ props }) {
  const { data, expanded = true } = props;

  return h('div', { className: 'json-view' },
    h(JsonNode, { name: null, value: data, depth: 0, expanded })
  );
}
