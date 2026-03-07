/**
 * Interface - Wraps a Python function into auto-generated input/output UI.
 *
 * Props:
 *   id            - Unique interface ID
 *   title         - Display title
 *   description   - Description text
 *   submit_label  - Submit button text
 *   layout        - "auto" | "horizontal" | "vertical"
 *   inputs        - Array of input component specs
 *   output_mode   - "text" | "metric" | "json" | "table" | "badge" | "code" | "markdown"
 *   exec_mode     - "simple" | "progress" | "stream"
 *   examples      - Array of example input arrays
 *   param_names   - Array of parameter names (matches examples ordering)
 *   live          - Auto-submit on input change
 *   flagging      - Show flag button
 */

const { createElement: h, useState, useEffect, useRef, useCallback, useMemo } = React;
import { cacaoWs } from '../core/websocket.js';
import { isStaticMode } from '../core/static-runtime.js';

// =============================================================================
// Helpers for advanced output types
// =============================================================================

function simpleMarkdown(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>');
}

function PlotlyOutput({ value }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current && window.Plotly) {
      try {
        const data = typeof value === 'string' ? JSON.parse(value) : value;
        window.Plotly.newPlot(containerRef.current, data.data || [], data.layout || {}, { responsive: true });
      } catch (e) {
        console.warn('Plotly render error:', e);
      }
    }
  }, [value]);

  if (!window.Plotly) {
    return h('div', { className: 'c-iface__result' },
      h('pre', { className: 'c-iface__json' }, typeof value === 'string' ? value : JSON.stringify(value, null, 2))
    );
  }

  return h('div', { className: 'c-iface__result c-iface__result--plotly', ref: containerRef });
}

export function Interface({ props }) {
  const {
    id,
    title,
    description,
    submit_label = 'Submit',
    layout = 'auto',
    inputs = [],
    output_mode = 'text',
    exec_mode = 'simple',
    examples,
    param_names = [],
    live = false,
    flagging = false,
  } = props;

  // Input values keyed by param_name
  const [values, setValues] = useState(() => {
    const initial = {};
    inputs.forEach(inp => {
      initial[inp.param_name] = inp.default != null ? inp.default : '';
    });
    return initial;
  });

  // Output state
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [streamText, setStreamText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState(null);
  const [showTraceback, setShowTraceback] = useState(false);
  const [cached, setCached] = useState(false);
  const [flagged, setFlagged] = useState(false);

  // Debounce timer for live mode
  const liveTimerRef = useRef(null);

  // Listen for interface messages from server
  useEffect(() => {
    const unsubWs = cacaoWs.subscribe(() => {});  // keep connection alive

    // Direct WebSocket message listener for interface protocol
    const handler = (event) => {
      let msg;
      try { msg = JSON.parse(event.data); } catch { return; }
      if (!msg.id || msg.id !== id) return;

      switch (msg.type) {
        case 'interface:result':
          setOutput(msg.output);
          setCached(!!msg.cached);
          setLoading(false);
          setProgress(0);
          break;
        case 'interface:error':
          setError({ error: msg.error, message: msg.message, traceback: msg.traceback });
          setLoading(false);
          setProgress(0);
          setIsStreaming(false);
          break;
        case 'interface:progress':
          setProgress(msg.value);
          break;
        case 'interface:stream':
          setStreamText(prev => prev + msg.token);
          break;
        case 'interface:stream_done':
          setIsStreaming(false);
          setLoading(false);
          // Move streamed text to output
          setStreamText(prev => {
            if (prev) {
              setOutput({ type: 'text', value: prev });
            }
            return '';
          });
          break;
        case 'interface:flagged':
          setFlagged(true);
          setTimeout(() => setFlagged(false), 2000);
          break;
      }
    };

    // Attach to raw WebSocket if available
    if (cacaoWs.ws) {
      cacaoWs.ws.addEventListener('message', handler);
      return () => {
        cacaoWs.ws?.removeEventListener('message', handler);
        unsubWs();
      };
    }

    return unsubWs;
  }, [id]);

  // Update a single input value
  const updateValue = useCallback((paramName, value) => {
    setValues(prev => {
      const next = { ...prev, [paramName]: value };

      // Live mode: debounced auto-submit
      if (live) {
        if (liveTimerRef.current) clearTimeout(liveTimerRef.current);
        liveTimerRef.current = setTimeout(() => {
          doSubmit(next);
        }, 300);
      }

      return next;
    });
  }, [live]);

  // Submit
  const doSubmit = useCallback((overrideValues) => {
    const submitValues = overrideValues || values;
    setError(null);
    setOutput(null);
    setCached(false);
    setStreamText('');
    setLoading(true);
    setProgress(0);

    if (exec_mode === 'stream') {
      setIsStreaming(true);
    }

    // Send via WebSocket
    if (cacaoWs.ws && cacaoWs.connected) {
      cacaoWs.ws.send(JSON.stringify({
        type: 'interface:submit',
        id,
        inputs: submitValues,
      }));
    }
  }, [values, id, exec_mode]);

  const handleSubmit = useCallback(() => {
    doSubmit(null);
  }, [doSubmit]);

  // Flag output
  const handleFlag = useCallback(() => {
    if (!output) return;
    if (cacaoWs.ws && cacaoWs.connected) {
      cacaoWs.ws.send(JSON.stringify({
        type: 'interface:flag',
        id,
        inputs: values,
        output: output,
      }));
    }
  }, [id, values, output]);

  // Load example
  const loadExample = useCallback((exampleValues) => {
    const newValues = {};
    param_names.forEach((name, i) => {
      newValues[name] = exampleValues[i] != null ? exampleValues[i] : '';
    });
    setValues(newValues);
    if (live) {
      setTimeout(() => doSubmit(newValues), 50);
    }
  }, [param_names, live, doSubmit]);

  // Determine layout class
  const layoutClass = layout === 'vertical'
    ? 'c-iface--vertical'
    : layout === 'horizontal'
      ? 'c-iface--horizontal'
      : 'c-iface--auto';

  return h('div', { className: `c-iface ${layoutClass}` }, [
    // Header
    (title || description) && h('div', { className: 'c-iface__header', key: 'header' }, [
      title && h('h3', { className: 'c-iface__title', key: 'title' }, title),
      description && h('p', { className: 'c-iface__desc', key: 'desc' }, description),
    ]),

    // Body: inputs + outputs
    h('div', { className: 'c-iface__body', key: 'body' }, [
      // Input panel
      h('div', { className: 'c-iface__inputs', key: 'inputs' }, [
        ...inputs.map((inp, i) =>
          h(InputField, {
            key: inp.param_name,
            spec: inp,
            value: values[inp.param_name],
            onChange: (val) => updateValue(inp.param_name, val),
          })
        ),

        // Examples
        examples && examples.length > 0 && h('div', { className: 'c-iface__examples', key: 'examples' }, [
          h('span', { className: 'c-iface__examples-label', key: 'label' }, 'Examples:'),
          ...examples.map((ex, i) =>
            h('button', {
              className: 'c-iface__example-btn',
              key: `ex-${i}`,
              onClick: () => loadExample(ex),
            }, `Example ${i + 1}`)
          ),
        ]),

        // Submit button (not shown in live mode)
        !live && !isStaticMode() && h('button', {
          className: 'btn btn-primary c-iface__submit',
          onClick: handleSubmit,
          disabled: loading,
          key: 'submit',
        }, loading
          ? h('span', { className: 'c-iface__spinner' })
          : submit_label
        ),

        // Static mode fallback
        !live && isStaticMode() && h('div', {
          className: 'c-iface__static-fallback',
          key: 'static-fallback',
        }, 'This interface requires a Python server. Run: cacao run app.py'),
      ]),

      // Output panel
      h('div', { className: 'c-iface__output', key: 'output' }, [
        // Loading states
        loading && exec_mode === 'progress' && h('div', { className: 'c-iface__progress', key: 'progress' }, [
          h('div', { className: 'c-iface__progress-bar', key: 'bar' },
            h('div', {
              className: 'c-iface__progress-fill',
              style: { width: `${Math.round(progress * 100)}%` },
            })
          ),
          h('span', { className: 'c-iface__progress-text', key: 'text' },
            `${Math.round(progress * 100)}%`
          ),
        ]),

        loading && exec_mode === 'simple' && !isStreaming && h('div', {
          className: 'c-iface__loading',
          key: 'loading',
        }, h('span', { className: 'c-iface__spinner c-iface__spinner--lg' })),

        // Streaming output
        isStreaming && streamText && h('div', {
          className: 'c-iface__result c-iface__result--streaming',
          key: 'stream',
        }, h('pre', { className: 'c-iface__text' }, streamText)),

        // Result output
        !loading && output && !isStreaming && h(OutputDisplay, {
          output,
          key: 'result',
        }),

        // Cached badge
        cached && h('span', { className: 'c-iface__badge c-iface__badge--cached', key: 'cached' }, 'Cached'),

        // Error display
        error && h('div', { className: 'c-iface__error', key: 'error' }, [
          h('div', { className: 'c-iface__error-header', key: 'header' }, [
            h('strong', { key: 'type' }, error.error),
            h('span', { key: 'msg' }, `: ${error.message}`),
          ]),
          error.traceback && h('button', {
            className: 'c-iface__error-toggle',
            onClick: () => setShowTraceback(!showTraceback),
            key: 'toggle',
          }, showTraceback ? 'Hide traceback' : 'Show traceback'),
          showTraceback && error.traceback && h('pre', {
            className: 'c-iface__traceback',
            key: 'tb',
          }, error.traceback),
        ]),

        // Empty state
        !loading && !output && !error && !isStreaming && h('div', {
          className: 'c-iface__empty',
          key: 'empty',
        }, 'Output will appear here'),

        // Flag button
        flagging && output && !loading && h('button', {
          className: `c-iface__flag ${flagged ? 'c-iface__flag--done' : ''}`,
          onClick: handleFlag,
          key: 'flag',
        }, flagged ? 'Flagged!' : 'Flag'),
      ]),
    ]),
  ]);
}

// =============================================================================
// Input Field Renderer
// =============================================================================

function InputField({ spec, value, onChange }) {
  const {
    component,
    label,
    description: desc,
    param_name,
    type: inputType,
    options,
    min,
    max,
    step,
    placeholder,
    monospace,
    accept,
    optional,
  } = spec;

  const inputId = `iface-${param_name}`;

  const wrapper = (children) =>
    h('div', { className: 'c-iface__field' }, [
      h('label', { className: 'c-input-label', htmlFor: inputId, key: 'label' }, [
        label,
        optional && h('span', { className: 'c-iface__optional', key: 'opt' }, ' (optional)'),
      ]),
      desc && h('span', { className: 'c-iface__field-desc', key: 'desc' }, desc),
      children,
    ]);

  switch (component) {
    case 'Checkbox':
      return wrapper(
        h('label', { className: 'c-iface__checkbox', key: 'input' }, [
          h('input', {
            type: 'checkbox',
            id: inputId,
            checked: !!value,
            onChange: (e) => onChange(e.target.checked),
            key: 'cb',
          }),
          h('span', { key: 'text' }, value ? 'Yes' : 'No'),
        ])
      );

    case 'Select':
      return wrapper(
        h('select', {
          className: 'c-input c-iface__select',
          id: inputId,
          value: value ?? '',
          onChange: (e) => onChange(e.target.value),
          key: 'input',
        }, (options || []).map(opt =>
          h('option', { value: opt, key: opt }, String(opt))
        ))
      );

    case 'Slider':
      return wrapper(
        h('div', { className: 'c-iface__slider-wrap', key: 'input' }, [
          h('input', {
            type: 'range',
            className: 'c-iface__slider',
            id: inputId,
            min: min ?? 0,
            max: max ?? 1,
            step: step ?? 0.01,
            value: value ?? 0.5,
            onChange: (e) => onChange(parseFloat(e.target.value)),
            key: 'slider',
          }),
          h('span', { className: 'c-iface__slider-value', key: 'val' },
            typeof value === 'number' ? value.toFixed(2) : String(value ?? 0.5)
          ),
        ])
      );

    case 'Textarea':
      return wrapper(
        h('textarea', {
          className: `c-input c-iface__textarea ${monospace ? 'c-iface__textarea--mono' : ''}`,
          id: inputId,
          placeholder: placeholder || '',
          value: value ?? '',
          rows: 4,
          onChange: (e) => onChange(e.target.value),
          key: 'input',
        })
      );

    case 'FileUpload':
      return wrapper(
        h('div', { className: 'c-iface__file-wrap', key: 'input' }, [
          h('input', {
            type: 'file',
            className: 'c-iface__file',
            id: inputId,
            accept: accept || undefined,
            onChange: (e) => {
              const file = e.target.files?.[0];
              if (file) {
                const reader = new FileReader();
                reader.onload = () => onChange(reader.result);
                reader.readAsDataURL(file);
              }
            },
            key: 'file-input',
          }),
          // Image preview
          value && accept && accept.startsWith('image') && h('img', {
            src: value,
            className: 'c-iface__file-preview',
            alt: 'Preview',
            key: 'preview',
          }),
          // Audio preview
          value && accept && accept.startsWith('audio') && h('audio', {
            src: value,
            controls: true,
            className: 'c-iface__audio-preview',
            key: 'audio-preview',
          }),
          // Video preview
          value && accept && accept.startsWith('video') && h('video', {
            src: value,
            controls: true,
            className: 'c-iface__video-preview',
            key: 'video-preview',
          }),
        ])
      );

    case 'Input':
    default:
      return wrapper(
        h('input', {
          type: inputType || 'text',
          className: 'c-input',
          id: inputId,
          placeholder: placeholder || '',
          value: value ?? '',
          onChange: (e) => onChange(inputType === 'number' ? e.target.value : e.target.value),
          key: 'input',
        })
      );
  }
}

// =============================================================================
// Output Display Renderer
// =============================================================================

function OutputDisplay({ output }) {
  if (!output) return null;

  const { type, value } = output;

  switch (type) {
    case 'text':
      return h('div', { className: 'c-iface__result' },
        h('pre', { className: 'c-iface__text' }, String(value))
      );

    case 'metric':
      return h('div', { className: 'c-iface__result c-iface__result--metric' },
        h('span', { className: 'c-iface__metric-value' }, String(value))
      );

    case 'badge':
      return h('div', { className: 'c-iface__result' },
        h('span', { className: `c-iface__badge c-iface__badge--${value === 'Yes' ? 'success' : 'muted'}` }, value)
      );

    case 'json':
      return h('div', { className: 'c-iface__result' },
        h('pre', { className: 'c-iface__json' }, JSON.stringify(value, null, 2))
      );

    case 'table':
      if (!Array.isArray(value) || value.length === 0) {
        return h('div', { className: 'c-iface__result' },
          h('span', { className: 'c-iface__empty' }, 'Empty result')
        );
      }
      const columns = Object.keys(value[0]);
      return h('div', { className: 'c-iface__result c-iface__result--table' },
        h('table', { className: 'c-iface__table' }, [
          h('thead', { key: 'head' },
            h('tr', null, columns.map(col =>
              h('th', { key: col }, col)
            ))
          ),
          h('tbody', { key: 'body' },
            value.map((row, i) =>
              h('tr', { key: i },
                columns.map(col =>
                  h('td', { key: col }, String(row[col] ?? ''))
                )
              )
            )
          ),
        ])
      );

    case 'code':
      return h('div', { className: 'c-iface__result' },
        h('pre', { className: 'c-iface__code' },
          h('code', null, String(value))
        )
      );

    case 'image':
      return h('div', { className: 'c-iface__result c-iface__result--image' },
        h('img', {
          src: value,
          className: 'c-iface__image',
          alt: 'Output image',
          loading: 'lazy',
        })
      );

    case 'audio':
      return h('div', { className: 'c-iface__result c-iface__result--audio' },
        h('audio', {
          src: value,
          controls: true,
          className: 'c-iface__audio',
        })
      );

    case 'video':
      return h('div', { className: 'c-iface__result c-iface__result--video' },
        h('video', {
          src: value,
          controls: true,
          className: 'c-iface__video',
        })
      );

    case 'file':
      return h('div', { className: 'c-iface__result c-iface__result--file' },
        h('a', {
          href: value,
          download: 'output',
          className: 'c-iface__file-download',
        }, 'Download file')
      );

    case 'plotly':
      return h(PlotlyOutput, { value });

    case 'markdown':
      return h('div', {
        className: 'c-iface__result c-iface__result--markdown',
        dangerouslySetInnerHTML: { __html: simpleMarkdown(value) },
      });

    case 'multi':
      return h('div', { className: 'c-iface__result c-iface__result--multi' },
        value.map((item, i) => h(OutputDisplay, { output: item, key: i }))
      );

    default:
      return h('div', { className: 'c-iface__result' },
        h('pre', { className: 'c-iface__text' }, String(value))
      );
  }
}
