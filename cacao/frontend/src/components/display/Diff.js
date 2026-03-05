/**
 * Diff - Side-by-side or unified code comparison
 */

const { createElement: h, useMemo } = React;

function diffLines(oldLines, newLines) {
  // Simple LCS-based diff
  const m = oldLines.length;
  const n = newLines.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (oldLines[i - 1] === newLines[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtrack to build diff
  const result = [];
  let i = m, j = n;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && oldLines[i - 1] === newLines[j - 1]) {
      result.unshift({ type: 'equal', oldLine: i, newLine: j, text: oldLines[i - 1] });
      i--; j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      result.unshift({ type: 'add', newLine: j, text: newLines[j - 1] });
      j--;
    } else {
      result.unshift({ type: 'remove', oldLine: i, text: oldLines[i - 1] });
      i--;
    }
  }
  return result;
}

function UnifiedView({ diff, language }) {
  return h('table', { className: 'c-diff-table' },
    h('tbody', null,
      diff.map((line, i) => {
        const cls = line.type === 'add' ? 'c-diff-line--add' : line.type === 'remove' ? 'c-diff-line--remove' : '';
        const prefix = line.type === 'add' ? '+' : line.type === 'remove' ? '-' : ' ';
        return h('tr', { key: i, className: 'c-diff-line ' + cls }, [
          h('td', { key: 'old', className: 'c-diff-gutter' }, line.oldLine || ''),
          h('td', { key: 'new', className: 'c-diff-gutter' }, line.newLine || ''),
          h('td', { key: 'prefix', className: 'c-diff-prefix' }, prefix),
          h('td', { key: 'code', className: 'c-diff-code' }, line.text),
        ]);
      })
    )
  );
}

function SideBySideView({ diff }) {
  // Build left/right columns
  const left = [];
  const right = [];

  diff.forEach((line, i) => {
    if (line.type === 'equal') {
      left.push({ num: line.oldLine, text: line.text, type: 'equal' });
      right.push({ num: line.newLine, text: line.text, type: 'equal' });
    } else if (line.type === 'remove') {
      left.push({ num: line.oldLine, text: line.text, type: 'remove' });
      right.push({ num: '', text: '', type: 'empty' });
    } else {
      left.push({ num: '', text: '', type: 'empty' });
      right.push({ num: line.newLine, text: line.text, type: 'add' });
    }
  });

  return h('div', { className: 'c-diff-side-by-side' }, [
    h('table', { key: 'left', className: 'c-diff-table c-diff-table--left' },
      h('tbody', null,
        left.map((line, i) =>
          h('tr', { key: i, className: 'c-diff-line c-diff-line--' + line.type }, [
            h('td', { key: 'num', className: 'c-diff-gutter' }, line.num),
            h('td', { key: 'code', className: 'c-diff-code' }, line.text),
          ])
        )
      )
    ),
    h('table', { key: 'right', className: 'c-diff-table c-diff-table--right' },
      h('tbody', null,
        right.map((line, i) =>
          h('tr', { key: i, className: 'c-diff-line c-diff-line--' + line.type }, [
            h('td', { key: 'num', className: 'c-diff-gutter' }, line.num),
            h('td', { key: 'code', className: 'c-diff-code' }, line.text),
          ])
        )
      )
    ),
  ]);
}

export function Diff({ props }) {
  const { old_code = '', new_code = '', language = '', mode = 'unified' } = props;

  const diff = useMemo(() => {
    const oldLines = old_code.split('\n');
    const newLines = new_code.split('\n');
    return diffLines(oldLines, newLines);
  }, [old_code, new_code]);

  const stats = useMemo(() => {
    let added = 0, removed = 0;
    diff.forEach(l => { if (l.type === 'add') added++; if (l.type === 'remove') removed++; });
    return { added, removed };
  }, [diff]);

  return h('div', { className: 'c-diff' }, [
    h('div', { key: 'header', className: 'c-diff-header' }, [
      language && h('span', { key: 'lang', className: 'c-diff-lang' }, language),
      h('span', { key: 'stats', className: 'c-diff-stats' }, [
        stats.added > 0 && h('span', { key: 'add', className: 'c-diff-stat--add' }, '+' + stats.added),
        stats.removed > 0 && h('span', { key: 'rm', className: 'c-diff-stat--remove' }, '-' + stats.removed),
      ]),
    ]),
    h('div', { key: 'body', className: 'c-diff-body' },
      mode === 'side-by-side'
        ? h(SideBySideView, { diff })
        : h(UnifiedView, { diff, language })
    ),
  ]);
}
