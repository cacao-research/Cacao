/**
 * Select dropdown with event handling
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function Select({ props }) {
  const {
    label,
    options = [],
    placeholder = 'Select...',
    signal,
    on_change,
    disabled = false,
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

    const eventName = on_change?.__event__ || on_change;
    if (eventName) {
      cacaoWs.sendEvent(eventName, { value: newValue });
    }
  };

  return h('div', { className: 'select-container' }, [
    label && h('label', { className: 'select-label', key: 'label' }, label),
    h('select', {
      className: 'select',
      value,
      onChange: handleChange,
      disabled,
      key: 'select'
    }, [
      h('option', { value: '', disabled: true, key: 'placeholder' }, placeholder),
      ...options.map((o, i) => h('option', {
        key: i,
        value: o.value || o.label || o
      }, o.label || o))
    ])
  ]);
}
