/**
 * Input - Text input field component with event handling
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function Input({ props }) {
  const {
    label,
    placeholder = '',
    type = 'text',
    disabled = false,
    signal,
    on_change,
  } = props;

  const [value, setValue] = useState('');

  // Get signal name if provided
  const signalName = signal?.__signal__;

  // Subscribe to signal updates
  useEffect(() => {
    if (signalName) {
      const unsubscribe = cacaoWs.subscribe((signals) => {
        if (signals[signalName] !== undefined) {
          setValue(signals[signalName]);
        }
      });
      // Get initial value
      const initial = cacaoWs.getSignal(signalName);
      if (initial !== undefined) {
        setValue(initial);
      }
      return unsubscribe;
    }
  }, [signalName]);

  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);

    // Emit change event
    const eventName = on_change?.__event__ || on_change;
    if (eventName) {
      cacaoWs.sendEvent(eventName, { value: newValue });
    }
  };

  return h('div', { className: 'c-input-wrapper' }, [
    label && h('label', { className: 'c-input-label', key: 'label' }, label),
    h('input', {
      type,
      className: 'c-input',
      placeholder,
      disabled,
      value,
      onChange: handleChange,
      key: 'input'
    })
  ]);
}
