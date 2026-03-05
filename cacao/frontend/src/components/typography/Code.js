/**
 * Code - Syntax highlighted code block component with signal support
 */

const { createElement: h, useState, useEffect, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function Code({ props }) {
  const { content, language = 'text' } = props;
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
      // Get initial value
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

  return h('pre', { className: `c-code language-${language}` }, [
    h('button', {
      key: 'copy',
      className: 'c-code-copy',
      onClick: handleCopy,
      'aria-label': 'Copy code'
    }, copyText),
    h('code', { key: 'code' }, displayContent)
  ]);
}
