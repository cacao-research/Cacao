/**
 * Code - Syntax highlighted code block with line numbers, language badge,
 * copy button, and signal support
 */

const { createElement: h, useState, useEffect, useCallback, useMemo } = React;
import { cacaoWs } from '../core/websocket.js';

// Basic syntax token patterns for common languages
const TOKEN_PATTERNS = {
  comment: /(?:\/\/.*$|\/\*[\s\S]*?\*\/|#.*$)/gm,
  string: /(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|`(?:[^`\\]|\\.)*`)/g,
  keyword: /\b(?:def|class|import|from|return|if|else|elif|for|while|try|except|finally|with|as|yield|async|await|raise|pass|break|continue|and|or|not|in|is|lambda|None|True|False|function|const|let|var|export|default|switch|case|new|this|typeof|instanceof|void|delete|throw|catch|extends|implements|interface|type|enum|public|private|static|abstract|super)\b/g,
  number: /\b(?:0[xXbBoO][\da-fA-F_]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b/g,
  builtin: /\b(?:print|len|range|str|int|float|list|dict|set|tuple|bool|map|filter|type|isinstance|hasattr|getattr|setattr|open|self|cls|console|document|window|Math|JSON|Array|Object|String|Number|Promise|Error)\b/g,
  decorator: /(?:^|\s)@[\w.]+/gm,
  operator: /(?:=>|===|!==|==|!=|<=|>=|&&|\|\||[+\-*/%&|^~<>]=?)/g,
};

function tokenize(code, language) {
  if (language === 'text' || language === 'plain') return [{ type: 'plain', text: code }];

  // Collect all token matches with positions
  const matches = [];
  for (const [type, pattern] of Object.entries(TOKEN_PATTERNS)) {
    const re = new RegExp(pattern.source, pattern.flags);
    let m;
    while ((m = re.exec(code)) !== null) {
      matches.push({ type, start: m.index, end: m.index + m[0].length, text: m[0] });
    }
  }

  // Sort by position, longer matches first for ties
  matches.sort((a, b) => a.start - b.start || b.end - a.end);

  // Build non-overlapping token list
  const tokens = [];
  let pos = 0;
  for (const m of matches) {
    if (m.start < pos) continue; // skip overlapping
    if (m.start > pos) {
      tokens.push({ type: 'plain', text: code.slice(pos, m.start) });
    }
    tokens.push(m);
    pos = m.end;
  }
  if (pos < code.length) {
    tokens.push({ type: 'plain', text: code.slice(pos) });
  }

  return tokens;
}

function renderTokens(tokens) {
  return tokens.map((t, i) => {
    if (t.type === 'plain') return t.text;
    return h('span', { key: i, className: 'c-code-token--' + t.type }, t.text);
  });
}

export function Code({ props }) {
  const {
    content,
    language = 'text',
    line_numbers = false,
    highlight_lines,
  } = props;

  const [copyText, setCopyText] = useState('Copy');

  // Check if content is a signal reference
  const signalName = content?.__signal__;
  const [displayContent, setDisplayContent] = useState(
    signalName ? '' : (content || '')
  );

  // Subscribe to signal updates
  useEffect(() => {
    if (signalName) {
      const unsubscribe = cacaoWs.subscribe((signals) => {
        if (signals[signalName] !== undefined) {
          setDisplayContent(signals[signalName]);
        }
      });
      const initial = cacaoWs.getSignal(signalName);
      if (initial !== undefined) {
        setDisplayContent(initial);
      }
      return unsubscribe;
    }
  }, [signalName]);

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(displayContent).then(() => {
      setCopyText('Copied!');
      setTimeout(() => setCopyText('Copy'), 1500);
    }).catch(() => {
      setCopyText('Failed');
      setTimeout(() => setCopyText('Copy'), 1500);
    });
  }, [displayContent]);

  // Parse highlighted line set
  const highlightSet = useMemo(() => {
    if (!highlight_lines) return null;
    const set = new Set();
    if (Array.isArray(highlight_lines)) {
      highlight_lines.forEach(n => set.add(n));
    } else if (typeof highlight_lines === 'string') {
      // Support "1,3,5-8"
      for (const part of highlight_lines.split(',')) {
        const range = part.trim().split('-');
        if (range.length === 2) {
          const start = parseInt(range[0]), end = parseInt(range[1]);
          for (let i = start; i <= end; i++) set.add(i);
        } else {
          set.add(parseInt(range[0]));
        }
      }
    }
    return set;
  }, [highlight_lines]);

  // Render with line numbers and syntax tokens
  const lines = displayContent.split('\n');
  const showLineNumbers = line_numbers || lines.length > 10;
  const tokens = useMemo(() => tokenize(displayContent, language), [displayContent, language]);

  const langLabel = language && language !== 'text' ? language : null;

  const codeContent = showLineNumbers
    ? h('table', { className: 'c-code-table' },
        h('tbody', null,
          lines.map((line, i) => {
            const lineNum = i + 1;
            const isHighlighted = highlightSet && highlightSet.has(lineNum);
            return h('tr', {
              key: i,
              className: isHighlighted ? 'c-code-line c-code-line--highlight' : 'c-code-line',
            }, [
              h('td', { key: 'num', className: 'c-code-line-number' }, lineNum),
              h('td', { key: 'code', className: 'c-code-line-content' },
                renderTokens(tokenize(line, language))
              ),
            ]);
          })
        )
      )
    : h('code', { key: 'code' }, renderTokens(tokens));

  return h('pre', { className: `c-code language-${language}` }, [
    langLabel && h('span', { key: 'lang', className: 'c-code-lang' }, langLabel),
    h('button', {
      key: 'copy',
      className: 'c-code-copy',
      onClick: handleCopy,
      'aria-label': 'Copy code'
    }, copyText),
    codeContent,
  ]);
}
