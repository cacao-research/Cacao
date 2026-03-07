/**
 * Extract - Structured extraction UI component
 *
 * Paste text and extract structured data matching a JSON Schema.
 * Powered by Prompture on the backend.
 *
 * Props:
 *   schema          - JSON Schema for the desired output
 *   provider        - LLM provider name
 *   model           - Model name
 *   title           - Component title
 *   description     - Description text
 *   submit_label    - Submit button text
 *   height          - Container height
 *   result_signal   - Signal to store extraction results
 */

const { createElement: h, useState, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function Extract({ props }) {
  const {
    schema,
    pydantic_model_name,
    provider = 'openai',
    model = 'gpt-4o',
    title = 'Extract',
    description = '',
    submit_label = 'Extract',
    height = '400px',
  } = props;

  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [usage, setUsage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const extractId = useRef(`extract_${Date.now()}_${Math.random().toString(36).slice(2)}`);

  const handleSubmit = useCallback(() => {
    if (!inputText.trim() || loading) return;

    setLoading(true);
    setError(null);
    setResult(null);

    // Listen for result
    const handler = (msg) => {
      if (msg.type === 'extract:result' && msg.id === extractId.current) {
        setResult(msg.result);
        setUsage(msg.usage);
        setLoading(false);
        cacaoWs.removeListener(handler);
      } else if (msg.type === 'extract:error' && msg.id === extractId.current) {
        setError(msg.error);
        setLoading(false);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);

    cacaoWs.send({
      type: 'extract:submit',
      id: extractId.current,
      text: inputText,
      schema: schema,
      model: `${provider}/${model}`,
    });
  }, [inputText, loading, schema, provider, model]);

  return h('div', { className: 'cacao-extract', style: { height } },
    // Header
    h('div', { className: 'cacao-extract-header' },
      h('h3', { className: 'cacao-extract-title' }, title),
      description && h('p', { className: 'cacao-extract-description' }, description),
    ),

    // Main content
    h('div', { className: 'cacao-extract-body' },
      // Left: text input
      h('div', { className: 'cacao-extract-input' },
        h('label', { className: 'cacao-extract-label' }, 'Text to extract from'),
        h('textarea', {
          className: 'cacao-extract-textarea',
          value: inputText,
          onChange: (e) => setInputText(e.target.value),
          placeholder: 'Paste or type text here...',
        }),
        // Schema preview
        schema && h('div', { className: 'cacao-extract-schema' },
          h('details', null,
            h('summary', null, 'Schema ',
              pydantic_model_name && h('span', { className: 'cacao-badge' }, pydantic_model_name),
            ),
            h('pre', null, JSON.stringify(schema, null, 2)),
          ),
        ),
        h('button', {
          className: 'cacao-btn cacao-btn-primary',
          onClick: handleSubmit,
          disabled: loading || !inputText.trim(),
        }, loading ? 'Extracting...' : submit_label),
      ),

      // Right: result
      h('div', { className: 'cacao-extract-output' },
        h('label', { className: 'cacao-extract-label' }, 'Extracted Data'),
        error && h('div', { className: 'cacao-alert cacao-alert-error' }, error),
        result && h('pre', { className: 'cacao-extract-result' }, JSON.stringify(result, null, 2)),
        usage && Object.keys(usage).length > 0 && h('div', { className: 'cacao-extract-usage' },
          h('small', null,
            usage.total_tokens && `${usage.total_tokens} tokens`,
            usage.cost && ` · $${usage.cost.toFixed(4)}`,
          ),
        ),
        !result && !error && !loading && h('div', { className: 'cacao-extract-placeholder' },
          'Results will appear here',
        ),
      ),
    ),
  );
}
