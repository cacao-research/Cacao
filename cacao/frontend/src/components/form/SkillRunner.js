/**
 * SkillRunner - Interactive wrapper for a Tukuy @skill
 *
 * Auto-generates input fields from the skill's input schema and
 * displays results with timing, metadata, and error handling.
 *
 * Props:
 *   skill_name     - Tukuy skill name
 *   title          - Display title
 *   description    - Description text
 *   descriptor     - Full skill descriptor (schema, tags, etc.)
 *   show_metadata  - Show category, tags, risk level
 *   show_timing    - Show execution duration
 *   height         - Container height
 */

const { createElement: h, useState, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

function schemaToFields(schema) {
  if (!schema || !schema.properties) return [];
  const required = new Set(schema.required || []);
  return Object.entries(schema.properties).map(([name, prop]) => ({
    name,
    type: prop.type || 'string',
    description: prop.description || '',
    default: prop.default,
    required: required.has(name),
    enum: prop.enum || null,
  }));
}

function FieldInput({ field, value, onChange }) {
  const { name, type, description, required, enum: enumValues } = field;

  if (enumValues) {
    return h('select', {
      className: 'cacao-input',
      value: value || '',
      onChange: (e) => onChange(name, e.target.value),
    },
      h('option', { value: '' }, `Select ${name}...`),
      ...enumValues.map(v => h('option', { key: v, value: v }, v)),
    );
  }

  if (type === 'boolean') {
    return h('label', { className: 'cacao-skill-checkbox-label' },
      h('input', {
        type: 'checkbox',
        checked: !!value,
        onChange: (e) => onChange(name, e.target.checked),
      }),
      h('span', null, name),
    );
  }

  if (type === 'number' || type === 'integer') {
    return h('input', {
      className: 'cacao-input',
      type: 'number',
      value: value ?? '',
      placeholder: description || name,
      step: type === 'integer' ? 1 : 'any',
      onChange: (e) => onChange(name, e.target.value === '' ? '' : Number(e.target.value)),
    });
  }

  // Default: string input (use textarea for long text)
  if (type === 'string' && description && description.toLowerCase().includes('text')) {
    return h('textarea', {
      className: 'cacao-input cacao-skill-textarea',
      value: value || '',
      placeholder: description || name,
      rows: 3,
      onChange: (e) => onChange(name, e.target.value),
    });
  }

  return h('input', {
    className: 'cacao-input',
    type: 'text',
    value: value || '',
    placeholder: description || name,
    onChange: (e) => onChange(name, e.target.value),
  });
}

export function SkillRunner({ props }) {
  const {
    skill_name,
    title = 'Skill',
    description = '',
    descriptor = {},
    show_metadata = true,
    show_timing = true,
    height = 'auto',
  } = props;

  const fields = schemaToFields(descriptor.input_schema);
  const [values, setValues] = useState(() => {
    const initial = {};
    fields.forEach(f => { if (f.default !== undefined) initial[f.name] = f.default; });
    return initial;
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [duration, setDuration] = useState(null);
  const invokeId = useRef(`skill_${Date.now()}_${Math.random().toString(36).slice(2)}`);

  const handleChange = useCallback((name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));
  }, []);

  const handleInvoke = useCallback(() => {
    if (loading) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setDuration(null);

    const handler = (msg) => {
      if (msg.id !== invokeId.current) return;
      if (msg.type === 'skill:result') {
        setResult(msg.value);
        setDuration(msg.duration_ms);
        setLoading(false);
        if (!msg.success && msg.error) setError(msg.error);
        cacaoWs.removeListener(handler);
      } else if (msg.type === 'skill:error') {
        setError(msg.error);
        setLoading(false);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);

    cacaoWs.send({
      type: 'skill:invoke',
      id: invokeId.current,
      skill_name: skill_name,
      inputs: values,
    });

    // Update invoke ID for next call
    invokeId.current = `skill_${Date.now()}_${Math.random().toString(36).slice(2)}`;
  }, [loading, skill_name, values]);

  const riskColors = {
    SAFE: 'var(--success-color, #22c55e)',
    MODERATE: 'var(--warning-color, #f59e0b)',
    DANGEROUS: 'var(--error-color, #ef4444)',
    CRITICAL: 'var(--error-color, #ef4444)',
  };

  return h('div', { className: 'cacao-skill-runner', style: height !== 'auto' ? { height } : undefined },
    // Header
    h('div', { className: 'cacao-skill-runner-header' },
      h('div', { className: 'cacao-skill-runner-title-row' },
        h('h3', { className: 'cacao-skill-runner-title' }, title),
        descriptor.version && h('span', { className: 'cacao-badge' }, `v${descriptor.version}`),
        descriptor.risk_level && descriptor.risk_level !== 'AUTO' &&
          h('span', {
            className: 'cacao-badge',
            style: { background: riskColors[descriptor.risk_level] || 'var(--text-secondary)' },
          }, descriptor.risk_level),
      ),
      description && h('p', { className: 'cacao-skill-runner-description' }, description),
      // Metadata
      show_metadata && (descriptor.category || (descriptor.tags && descriptor.tags.length > 0)) &&
        h('div', { className: 'cacao-skill-runner-meta' },
          descriptor.category && h('span', { className: 'cacao-badge cacao-badge-outline' }, descriptor.category),
          ...(descriptor.tags || []).map(tag =>
            h('span', { key: tag, className: 'cacao-badge cacao-badge-outline cacao-badge-sm' }, tag)
          ),
          descriptor.requires_network && h('span', { className: 'cacao-badge cacao-badge-outline cacao-badge-sm' }, 'network'),
          descriptor.requires_filesystem && h('span', { className: 'cacao-badge cacao-badge-outline cacao-badge-sm' }, 'filesystem'),
        ),
    ),

    // Body
    h('div', { className: 'cacao-skill-runner-body' },
      // Input fields
      h('div', { className: 'cacao-skill-runner-inputs' },
        fields.length > 0
          ? fields.map(field =>
              h('div', { key: field.name, className: 'cacao-skill-runner-field' },
                h('label', { className: 'cacao-skill-runner-label' },
                  field.name,
                  field.required && h('span', { className: 'cacao-skill-required' }, ' *'),
                ),
                field.description && h('small', { className: 'cacao-skill-runner-hint' }, field.description),
                h(FieldInput, { field, value: values[field.name], onChange: handleChange }),
              )
            )
          : h('div', { className: 'cacao-skill-runner-no-inputs' }, 'This skill takes no inputs'),

        h('button', {
          className: 'cacao-btn cacao-btn-primary',
          onClick: handleInvoke,
          disabled: loading,
        }, loading ? 'Running...' : 'Run Skill'),
      ),

      // Output
      h('div', { className: 'cacao-skill-runner-output' },
        h('label', { className: 'cacao-skill-runner-label' }, 'Output'),
        error && h('div', { className: 'cacao-alert cacao-alert-error' }, error),
        result !== null && h('pre', { className: 'cacao-skill-runner-result' },
          typeof result === 'object' ? JSON.stringify(result, null, 2) : String(result),
        ),
        show_timing && duration !== null && h('div', { className: 'cacao-skill-runner-timing' },
          h('small', null, `Completed in ${duration.toFixed(1)}ms`),
        ),
        result === null && !error && !loading && h('div', { className: 'cacao-skill-runner-placeholder' },
          'Run the skill to see output',
        ),
      ),
    ),
  );
}
