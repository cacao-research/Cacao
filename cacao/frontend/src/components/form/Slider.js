/**
 * Slider component with event handling
 */

const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function Slider({ props }) {
  const {
    label,
    min = 0,
    max = 100,
    step = 1,
    value: initialValue,
    signal,
    on_change,
  } = props;

  const [value, setValue] = useState(initialValue || min);

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
    const newValue = parseFloat(e.target.value);
    setValue(newValue);

    const eventName = on_change?.__event__ || on_change;
    if (eventName) {
      cacaoWs.sendEvent(eventName, { value: newValue });
    }
  };

  return h('div', { className: 'slider-container' }, [
    h('label', { className: 'slider-label', key: 'label' }, `${label}: ${value}`),
    h('input', {
      type: 'range',
      className: 'slider',
      min,
      max,
      step,
      value,
      onChange: handleChange,
      key: 'input'
    })
  ]);
}
