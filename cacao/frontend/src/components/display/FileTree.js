/**
 * FileTree - Directory structure display
 */

const { createElement: h, useState } = React;

function getFileIcon(name, isDir) {
  if (isDir) return '\uD83D\uDCC1';
  const ext = name.split('.').pop()?.toLowerCase();
  const icons = {
    py: '\uD83D\uDC0D', js: '\uD83D\uDFE8', ts: '\uD83D\uDD35', jsx: '\u269B\uFE0F', tsx: '\u269B\uFE0F',
    md: '\uD83D\uDCDD', json: '\uD83D\uDCC4', css: '\uD83C\uDFA8', less: '\uD83C\uDFA8',
    html: '\uD83C\uDF10', yml: '\u2699\uFE0F', yaml: '\u2699\uFE0F', toml: '\u2699\uFE0F',
    png: '\uD83D\uDDBC\uFE0F', jpg: '\uD83D\uDDBC\uFE0F', svg: '\uD83D\uDDBC\uFE0F', gif: '\uD83D\uDDBC\uFE0F',
  };
  return icons[ext] || '\uD83D\uDCC4';
}

function TreeNode({ name, value, depth, highlight }) {
  const isDir = value !== null && typeof value === 'object';
  const [open, setOpen] = useState(true);
  const isHighlighted = highlight && name === highlight;

  return h('div', { className: 'c-file-tree-node' }, [
    h('div', {
      key: 'label',
      className: 'c-file-tree-label' + (isHighlighted ? ' c-file-tree-label--highlight' : ''),
      style: { paddingLeft: (depth * 16 + 4) + 'px' },
      onClick: isDir ? () => setOpen(!open) : undefined,
    }, [
      isDir && h('span', { key: 'arrow', className: 'c-file-tree-arrow' + (open ? ' c-file-tree-arrow--open' : '') }, '\u25B6'),
      h('span', { key: 'icon', className: 'c-file-tree-icon' }, getFileIcon(name, isDir)),
      h('span', { key: 'name', className: 'c-file-tree-name' }, name),
    ]),
    isDir && open && h('div', { key: 'children', className: 'c-file-tree-children' },
      Object.entries(value).map(([k, v]) =>
        h(TreeNode, { key: k, name: k, value: v, depth: depth + 1, highlight })
      )
    ),
  ]);
}

function parseTreeString(str) {
  // Parse tree command-like string output into a nested object
  const lines = str.trim().split('\n');
  const root = {};
  const stack = [{ obj: root, indent: -1 }];

  for (const line of lines) {
    const cleaned = line.replace(/[│├└──\s]/g, '').replace(/\u2502|\u251C|\u2514|\u2500/g, '');
    if (!cleaned) continue;

    const indent = line.search(/[^\s│├└──\u2502\u251C\u2514\u2500]/);
    const name = cleaned.trim();
    const isDir = name.endsWith('/');
    const cleanName = isDir ? name.slice(0, -1) : name;

    while (stack.length > 1 && stack[stack.length - 1].indent >= indent) {
      stack.pop();
    }

    const parent = stack[stack.length - 1].obj;
    if (isDir) {
      parent[cleanName] = {};
      stack.push({ obj: parent[cleanName], indent });
    } else {
      parent[cleanName] = null;
    }
  }

  return root;
}

export function FileTree({ props }) {
  let { data, highlight } = props;

  if (typeof data === 'string') {
    data = parseTreeString(data);
  }

  return h('div', { className: 'c-file-tree' },
    Object.entries(data).map(([k, v]) =>
      h(TreeNode, { key: k, name: k, value: v, depth: 0, highlight })
    )
  );
}
