/**
 * Compare - Shared inputs, run through multiple functions, compare outputs side-by-side.
 *
 * Props:
 *   functions     - Array of { id, title, output_mode, exec_mode }
 *   inputs        - Array of input specs (shared across all functions)
 *   param_names   - Array of parameter names
 *   submit_label  - Submit button text
 */

const { createElement: h, useState, useEffect, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';
import { isStaticMode } from '../core/static-runtime.js';

export function Compare({ props }) {
  const {
    functions = [],
    inputs = [],
    param_names = [],
    submit_label = 'Compare',
  } = props;

  const [values, setValues] = useState(() => {
    const initial = {};
    inputs.forEach(inp => {
      initial[inp.param_name] = inp.default != null ? inp.default : '';
    });
    return initial;
  });

  const [outputs, setOutputs] = useState({});
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState({});

  // Listen for results from all functions
  useEffect(() => {
    if (!cacaoWs.ws) return;

    const handler = (event) => {
      let msg;
      try { msg = JSON.parse(event.data); } catch { return; }

      const fnIndex = functions.findIndex(fn => fn.id === msg.id);
      if (fnIndex === -1) return;

      if (msg.type === 'interface:result') {
        setOutputs(prev => ({ ...prev, [fnIndex]: msg.output }));
        setLoading(prev => ({ ...prev, [fnIndex]: false }));
      } else if (msg.type === 'interface:error') {
        setErrors(prev => ({ ...prev, [fnIndex]: msg }));
        setLoading(prev => ({ ...prev, [fnIndex]: false }));
      }
    };

    cacaoWs.ws.addEventListener('message', handler);
    return () => cacaoWs.ws?.removeEventListener('message', handler);
  }, [functions]);

  const updateValue = useCallback((paramName, val) => {
    setValues(prev => ({ ...prev, [paramName]: val }));
  }, []);

  const handleSubmit = useCallback(() => {
    setOutputs({});
    setErrors({});

    const newLoading = {};
    functions.forEach((_, i) => { newLoading[i] = true; });
    setLoading(newLoading);

    // Submit same inputs to all functions
    functions.forEach(fn => {
      if (cacaoWs.ws && cacaoWs.connected) {
        cacaoWs.ws.send(JSON.stringify({
          type: 'interface:submit',
          id: fn.id,
          inputs: values,
        }));
      }
    });
  }, [values, functions]);

  return h('div', { className: 'c-compare' }, [
    // Shared inputs panel
    h('div', { className: 'c-compare__inputs', key: 'inputs' }, [
      ...inputs.map(inp =>
        h(CompareInputField, {
          key: inp.param_name,
          spec: inp,
          value: values[inp.param_name],
          onChange: (val) => updateValue(inp.param_name, val),
        })
      ),
      !isStaticMode() && h('button', {
        className: 'btn btn-primary c-compare__submit',
        onClick: handleSubmit,
        disabled: Object.values(loading).some(Boolean),
        key: 'submit',
      }, Object.values(loading).some(Boolean) ? 'Running...' : submit_label),
    ]),

    // Side-by-side output panels
    h('div', { className: 'c-compare__outputs', key: 'outputs' },
      functions.map((fn, i) =>
        h('div', { className: 'c-compare__output', key: i }, [
          h('div', { className: 'c-compare__output-title', key: 'title' }, fn.title),
          loading[i]
            ? h('div', { className: 'c-iface__loading', key: 'loading' },
                h('span', { className: 'c-iface__spinner c-iface__spinner--lg' }))
            : outputs[i]
              ? h(CompareOutputDisplay, { output: outputs[i], key: 'result' })
              : errors[i]
                ? h('div', { className: 'c-iface__error', key: 'error' }, [
                    h('strong', { key: 'type' }, errors[i].error),
                    h('span', { key: 'msg' }, `: ${errors[i].message}`),
                  ])
                : h('div', { className: 'c-iface__empty', key: 'empty' }, 'Output will appear here'),
        ])
      )
    ),
  ]);
}

// Input field (reuses interface styling)
function CompareInputField({ spec, value, onChange }) {
  const { component, label, param_name, type: inputType, options, min, max, step, placeholder } = spec;
  const inputId = `compare-${param_name}`;

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
    case 'Slider':
      return wrapper(h('div', { className: 'c-iface__slider-wrap', key: 'input' }, [
        h('input', { type: 'range', className: 'c-iface__slider', id: inputId, min: min ?? 0, max: max ?? 1, step: step ?? 0.01, value: value ?? 0.5, onChange: (e) => onChange(parseFloat(e.target.value)), key: 'slider' }),
        h('span', { className: 'c-iface__slider-value', key: 'val' }, typeof value === 'number' ? value.toFixed(2) : String(value ?? 0.5)),
      ]));
    default:
      return wrapper(h('input', { type: inputType || 'text', className: 'c-input', id: inputId, value: value ?? '', placeholder: placeholder || '', onChange: (e) => onChange(e.target.value), key: 'input' }));
  }
}

// Output display (subset of Interface's OutputDisplay)
function CompareOutputDisplay({ output }) {
  if (!output) return null;
  const { type, value } = output;

  switch (type) {
    case 'text': return h('div', { className: 'c-iface__result' }, h('pre', { className: 'c-iface__text' }, String(value)));
    case 'metric': return h('div', { className: 'c-iface__result c-iface__result--metric' }, h('span', { className: 'c-iface__metric-value' }, String(value)));
    case 'json': return h('div', { className: 'c-iface__result' }, h('pre', { className: 'c-iface__json' }, JSON.stringify(value, null, 2)));
    case 'image': return h('div', { className: 'c-iface__result' }, h('img', { src: value, className: 'c-iface__image', alt: 'Output' }));
    case 'badge': return h('div', { className: 'c-iface__result' }, h('span', { className: `c-iface__badge c-iface__badge--${value === 'Yes' ? 'success' : 'muted'}` }, value));
    case 'table':
      if (!Array.isArray(value) || !value.length) return h('div', { className: 'c-iface__result' }, 'Empty');
      const cols = Object.keys(value[0]);
      return h('div', { className: 'c-iface__result c-iface__result--table' },
        h('table', { className: 'c-iface__table' }, [
          h('thead', { key: 'h' }, h('tr', null, cols.map(c => h('th', { key: c }, c)))),
          h('tbody', { key: 'b' }, value.slice(0, 50).map((row, i) => h('tr', { key: i }, cols.map(c => h('td', { key: c }, String(row[c] ?? '')))))),
        ])
      );
    default: return h('div', { className: 'c-iface__result' }, h('pre', { className: 'c-iface__text' }, String(value)));
  }
}
