/**
 * Series - Chain multiple interfaces, output of each feeds into the next.
 *
 * Props:
 *   interfaces    - Array of interface specs (each with id, title, inputs, output_mode, exec_mode, param_names)
 *   submit_label  - Submit button text
 */

const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';
import { isStaticMode } from '../core/static-runtime.js';

export function Series({ props }) {
  const {
    interfaces = [],
    submit_label = 'Run',
  } = props;

  // Track current step and outputs per step
  const [currentStep, setCurrentStep] = useState(0);
  const [stepOutputs, setStepOutputs] = useState({});
  const [stepErrors, setStepErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [values, setValues] = useState(() => {
    if (!interfaces[0]) return {};
    const initial = {};
    interfaces[0].inputs.forEach(inp => {
      initial[inp.param_name] = inp.default != null ? inp.default : '';
    });
    return initial;
  });

  // Listen for results from all interfaces in the chain
  useEffect(() => {
    if (!cacaoWs.ws) return;

    const handler = (event) => {
      let msg;
      try { msg = JSON.parse(event.data); } catch { return; }

      // Find which interface this message belongs to
      const stepIndex = interfaces.findIndex(iface => iface.id === msg.id);
      if (stepIndex === -1) return;

      if (msg.type === 'interface:result') {
        setStepOutputs(prev => ({ ...prev, [stepIndex]: msg.output }));

        // If there's a next step, auto-submit with this output as input
        if (stepIndex < interfaces.length - 1) {
          const nextIface = interfaces[stepIndex + 1];
          const nextInputs = {};

          // Map the output value to the next function's first parameter
          if (msg.output && nextIface.param_names.length > 0) {
            const outputVal = msg.output.value;
            // If output is a dict and next fn has matching param names, map them
            if (typeof outputVal === 'object' && outputVal !== null && !Array.isArray(outputVal)) {
              nextIface.param_names.forEach(name => {
                nextInputs[name] = outputVal[name] !== undefined ? outputVal[name] : '';
              });
            } else {
              // Pass output as first parameter
              nextInputs[nextIface.param_names[0]] = typeof outputVal === 'string' ? outputVal : JSON.stringify(outputVal);
            }
          }

          setCurrentStep(stepIndex + 1);

          // Submit to next interface
          if (cacaoWs.ws && cacaoWs.connected) {
            cacaoWs.ws.send(JSON.stringify({
              type: 'interface:submit',
              id: nextIface.id,
              inputs: nextInputs,
            }));
          }
        } else {
          // Last step done
          setLoading(false);
          setCurrentStep(stepIndex);
        }
      } else if (msg.type === 'interface:error') {
        setStepErrors(prev => ({ ...prev, [stepIndex]: msg }));
        setLoading(false);
      }
    };

    cacaoWs.ws.addEventListener('message', handler);
    return () => cacaoWs.ws?.removeEventListener('message', handler);
  }, [interfaces]);

  const updateValue = useCallback((paramName, val) => {
    setValues(prev => ({ ...prev, [paramName]: val }));
  }, []);

  const handleSubmit = useCallback(() => {
    setStepOutputs({});
    setStepErrors({});
    setCurrentStep(0);
    setLoading(true);

    // Submit to first interface
    if (cacaoWs.ws && cacaoWs.connected && interfaces[0]) {
      cacaoWs.ws.send(JSON.stringify({
        type: 'interface:submit',
        id: interfaces[0].id,
        inputs: values,
      }));
    }
  }, [values, interfaces]);

  return h('div', { className: 'c-series' }, [
    // Header with step indicators
    h('div', { className: 'c-series__steps', key: 'steps' },
      interfaces.map((iface, i) =>
        h('div', {
          className: `c-series__step ${i === currentStep ? 'c-series__step--active' : ''} ${stepOutputs[i] ? 'c-series__step--done' : ''} ${stepErrors[i] ? 'c-series__step--error' : ''}`,
          key: i,
        }, [
          h('span', { className: 'c-series__step-num', key: 'num' }, String(i + 1)),
          h('span', { className: 'c-series__step-title', key: 'title' }, iface.title || `Step ${i + 1}`),
          i < interfaces.length - 1 && h('span', { className: 'c-series__step-arrow', key: 'arrow' }, '\u2192'),
        ])
      )
    ),

    // Input panel (only for first function)
    h('div', { className: 'c-series__input', key: 'input' }, [
      ...interfaces[0].inputs.map(inp =>
        h(SeriesInputField, {
          key: inp.param_name,
          spec: inp,
          value: values[inp.param_name],
          onChange: (val) => updateValue(inp.param_name, val),
        })
      ),
      !isStaticMode() && h('button', {
        className: 'btn btn-primary c-series__submit',
        onClick: handleSubmit,
        disabled: loading,
        key: 'submit',
      }, loading ? 'Running...' : submit_label),
    ]),

    // Output panels for each step
    h('div', { className: 'c-series__outputs', key: 'outputs' },
      interfaces.map((iface, i) =>
        h('div', {
          className: `c-series__output ${stepOutputs[i] ? 'c-series__output--has-result' : ''}`,
          key: i,
        }, [
          h('div', { className: 'c-series__output-header', key: 'header' }, iface.title || `Step ${i + 1}`),
          stepOutputs[i]
            ? h(SeriesOutputDisplay, { output: stepOutputs[i], key: 'result' })
            : stepErrors[i]
              ? h('div', { className: 'c-iface__error', key: 'error' }, [
                  h('strong', { key: 'type' }, stepErrors[i].error),
                  h('span', { key: 'msg' }, `: ${stepErrors[i].message}`),
                ])
              : (loading && i <= currentStep)
                ? h('div', { className: 'c-iface__loading', key: 'loading' },
                    h('span', { className: 'c-iface__spinner c-iface__spinner--lg' }))
                : h('div', { className: 'c-iface__empty', key: 'empty' }, 'Waiting...'),
        ])
      )
    ),
  ]);
}

// Simple input field for series (reuses interface styling)
function SeriesInputField({ spec, value, onChange }) {
  const { component, label, param_name, type: inputType, options, min, max, step, placeholder } = spec;
  const inputId = `series-${param_name}`;

  const wrapper = (children) =>
    h('div', { className: 'c-iface__field' }, [
      h('label', { className: 'c-input-label', htmlFor: inputId, key: 'label' }, label),
      children,
    ]);

  switch (component) {
    case 'Checkbox':
      return wrapper(h('input', { type: 'checkbox', id: inputId, checked: !!value, onChange: (e) => onChange(e.target.checked), key: 'input' }));
    case 'Select':
      return wrapper(h('select', { className: 'c-input', id: inputId, value: value ?? '', onChange: (e) => onChange(e.target.value), key: 'input' },
        (options || []).map(opt => h('option', { value: opt, key: opt }, String(opt)))
      ));
    case 'Textarea':
      return wrapper(h('textarea', { className: 'c-input', id: inputId, value: value ?? '', rows: 3, onChange: (e) => onChange(e.target.value), key: 'input' }));
    default:
      return wrapper(h('input', { type: inputType || 'text', className: 'c-input', id: inputId, value: value ?? '', placeholder: placeholder || '', onChange: (e) => onChange(e.target.value), key: 'input' }));
  }
}

// Simple output display for series (subset of Interface's OutputDisplay)
function SeriesOutputDisplay({ output }) {
  if (!output) return null;
  const { type, value } = output;

  switch (type) {
    case 'text': return h('pre', { className: 'c-iface__text' }, String(value));
    case 'metric': return h('span', { className: 'c-iface__metric-value', style: { fontSize: '1.5rem' } }, String(value));
    case 'json': return h('pre', { className: 'c-iface__json' }, JSON.stringify(value, null, 2));
    case 'image': return h('img', { src: value, className: 'c-iface__image', alt: 'Output' });
    case 'table':
      if (!Array.isArray(value) || !value.length) return h('span', null, 'Empty');
      const cols = Object.keys(value[0]);
      return h('table', { className: 'c-iface__table' }, [
        h('thead', { key: 'h' }, h('tr', null, cols.map(c => h('th', { key: c }, c)))),
        h('tbody', { key: 'b' }, value.slice(0, 20).map((row, i) => h('tr', { key: i }, cols.map(c => h('td', { key: c }, String(row[c] ?? '')))))),
      ]);
    default: return h('pre', { className: 'c-iface__text' }, String(value));
  }
}
