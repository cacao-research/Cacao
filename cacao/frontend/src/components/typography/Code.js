/**
 * Code - Syntax highlighted code block component with signal support
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function Code({ props }) {
  const { content, language = 'text' } = props;

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

  return h('pre', { className: `c-code language-${language}` },
    h('code', null, displayContent)
  );
}
