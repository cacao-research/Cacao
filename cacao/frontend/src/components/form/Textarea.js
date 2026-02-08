/**
 * Textarea - Multi-line text input with event handling
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function Textarea({ props }) {
  const {
    label,
    placeholder = '',
    rows = 4,
    disabled = false,
    signal,
    on_change,
  } = props;

  const [value, setValue] = useState('');

  const signalName = signal?.__signal__;

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

  return h('div', { className: 'c-textarea-wrapper' }, [
    label && h('label', { className: 'c-textarea-label', key: 'label' }, label),
    h('textarea', {
      className: 'c-textarea',
      placeholder,
      rows,
      disabled,
      value,
      onChange: handleChange,
      key: 'textarea'
    })
  ]);
}
