/**
 * Text component with signal support
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function Text({ props }) {
  const { content, color, size, weight } = props;

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

  const classNames = [
    'text',
    color === 'muted' && 'text-muted',
    size === 'sm' && 'text-sm',
    size === 'lg' && 'text-lg',
  ].filter(Boolean).join(' ');

  const style = weight ? { fontWeight: weight } : undefined;

  return h('p', { className: classNames, style }, displayContent);
}
