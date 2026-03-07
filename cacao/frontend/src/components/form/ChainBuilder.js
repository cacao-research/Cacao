/**
 * ChainBuilder - Visual chain builder for Tukuy Chain/Branch/Parallel
 *
 * Drag-and-drop interface for composing skills and transformers into
 * processing chains. Supports sequential chains, conditional branches,
 * and parallel fan-out.
 *
 * Props:
 *   title          - Widget title
 *   initial_steps  - Pre-configured chain steps
 *   show_output    - Show output panel
 *   height         - Container height
 */

const { createElement: h, useState, useEffect, useCallback, useRef } = React;
import { cacaoWs } from '../core/websocket.js';

const STEP_TYPES = [
  { value: 'transformer', label: 'Transformer', icon: '⚙' },
  { value: 'skill', label: 'Skill', icon: '🔧' },
  { value: 'branch', label: 'Branch', icon: '⑂' },
  { value: 'parallel', label: 'Parallel', icon: '⫽' },
];

function StepCard({ step, index, onRemove, onUpdate, onMoveUp, onMoveDown, isFirst, isLast }) {
  const [expanded, setExpanded] = useState(false);
  const typeInfo = STEP_TYPES.find(t => t.value === step.type) || STEP_TYPES[0];

  return h('div', {
    className: `cacao-chain-step cacao-chain-step-${step.type}`,
    draggable: true,
    onDragStart: (e) => {
      e.dataTransfer.setData('text/plain', String(index));
      e.dataTransfer.effectAllowed = 'move';
    },
  },
    // Step header
    h('div', { className: 'cacao-chain-step-header' },
      h('span', { className: 'cacao-chain-step-icon' }, typeInfo.icon),
      h('span', { className: 'cacao-chain-step-type' }, typeInfo.label),
      h('span', { className: 'cacao-chain-step-name' }, step.name || '(unnamed)'),
      h('div', { className: 'cacao-chain-step-actions' },
        !isFirst && h('button', {
          className: 'cacao-chain-step-btn',
          onClick: () => onMoveUp(index),
          title: 'Move up',
        }, '↑'),
        !isLast && h('button', {
          className: 'cacao-chain-step-btn',
          onClick: () => onMoveDown(index),
          title: 'Move down',
        }, '↓'),
        h('button', {
          className: 'cacao-chain-step-btn',
          onClick: () => setExpanded(!expanded),
          title: expanded ? 'Collapse' : 'Expand',
        }, expanded ? '−' : '+'),
        h('button', {
          className: 'cacao-chain-step-btn cacao-chain-step-btn-remove',
          onClick: () => onRemove(index),
          title: 'Remove',
        }, '×'),
      ),
    ),

    // Step details (expanded)
    expanded && h('div', { className: 'cacao-chain-step-body' },
      h('div', { className: 'cacao-chain-step-field' },
        h('label', null, 'Name'),
        h('input', {
          className: 'cacao-input',
          value: step.name || '',
          placeholder: step.type === 'transformer' ? 'e.g., strip, lowercase' : 'Skill or step name',
          onChange: (e) => onUpdate(index, { ...step, name: e.target.value }),
        }),
      ),

      // Transformer params
      step.type === 'transformer' && h('div', { className: 'cacao-chain-step-field' },
        h('label', null, 'Parameters (JSON)'),
        h('textarea', {
          className: 'cacao-input',
          rows: 2,
          value: step.params ? JSON.stringify(step.params) : '',
          placeholder: '{"key": "value"}',
          onChange: (e) => {
            try {
              const params = e.target.value ? JSON.parse(e.target.value) : null;
              onUpdate(index, { ...step, params });
            } catch { /* invalid JSON, ignore */ }
          },
        }),
      ),

      // Branch condition
      step.type === 'branch' && h('div', { className: 'cacao-chain-step-field' },
        h('label', null, 'Condition (Python expression using "v")'),
        h('input', {
          className: 'cacao-input',
          value: step.condition || '',
          placeholder: 'e.g., "@" in v',
          onChange: (e) => onUpdate(index, { ...step, condition: e.target.value }),
        }),
      ),

      // Parallel merge strategy
      step.type === 'parallel' && h('div', { className: 'cacao-chain-step-field' },
        h('label', null, 'Merge strategy'),
        h('select', {
          className: 'cacao-input',
          value: step.merge || 'dict',
          onChange: (e) => onUpdate(index, { ...step, merge: e.target.value }),
        },
          h('option', { value: 'dict' }, 'Dict (key → result)'),
          h('option', { value: 'list' }, 'List'),
          h('option', { value: 'first' }, 'First success'),
        ),
      ),
    ),
  );
}

export function ChainBuilder({ props }) {
  const {
    title = 'Chain Builder',
    initial_steps = [],
    show_output = true,
    height = '600px',
  } = props;

  const [steps, setSteps] = useState(initial_steps.length > 0 ? initial_steps : []);
  const [inputValue, setInputValue] = useState('');
  const [output, setOutput] = useState(null);
  const [stepResults, setStepResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [addType, setAddType] = useState('transformer');
  const chainId = useRef(`chain_${Date.now()}_${Math.random().toString(36).slice(2)}`);
  const dropRef = useRef(null);

  const addStep = useCallback(() => {
    setSteps(prev => [...prev, { type: addType, name: '', params: null }]);
  }, [addType]);

  const removeStep = useCallback((index) => {
    setSteps(prev => prev.filter((_, i) => i !== index));
  }, []);

  const updateStep = useCallback((index, newStep) => {
    setSteps(prev => prev.map((s, i) => i === index ? newStep : s));
  }, []);

  const moveStep = useCallback((from, to) => {
    setSteps(prev => {
      const arr = [...prev];
      const [item] = arr.splice(from, 1);
      arr.splice(to, 0, item);
      return arr;
    });
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const fromIndex = parseInt(e.dataTransfer.getData('text/plain'), 10);
    if (isNaN(fromIndex)) return;

    // Calculate drop position
    const rect = dropRef.current.getBoundingClientRect();
    const y = e.clientY - rect.top;
    const stepHeight = rect.height / (steps.length || 1);
    let toIndex = Math.round(y / stepHeight);
    toIndex = Math.max(0, Math.min(toIndex, steps.length - 1));

    if (fromIndex !== toIndex) moveStep(fromIndex, toIndex);
  }, [steps.length, moveStep]);

  const runChain = useCallback(() => {
    if (steps.length === 0 || loading) return;

    setLoading(true);
    setError(null);
    setOutput(null);
    setStepResults([]);

    const id = `chain_${Date.now()}_${Math.random().toString(36).slice(2)}`;
    chainId.current = id;

    const handler = (msg) => {
      if (msg.id !== id) return;

      switch (msg.type) {
        case 'chain:step_result':
          setStepResults(prev => [...prev, {
            index: msg.step_index,
            name: msg.step_name,
            value: msg.value,
            success: msg.success,
            error: msg.error,
          }]);
          break;
        case 'chain:result':
          setOutput(msg.value);
          setLoading(false);
          cacaoWs.removeListener(handler);
          break;
        case 'chain:error':
          setError(msg.error);
          setLoading(false);
          cacaoWs.removeListener(handler);
          break;
      }
    };
    cacaoWs.addListener(handler);

    cacaoWs.send({
      type: 'chain:run',
      id,
      steps: steps.filter(s => s.name), // Only named steps
      input: inputValue,
    });
  }, [steps, inputValue, loading]);

  return h('div', { className: 'cacao-chain-builder', style: { height } },
    // Header
    h('div', { className: 'cacao-chain-builder-header' },
      h('h3', { className: 'cacao-chain-builder-title' }, title),
      h('span', { className: 'cacao-badge' }, `${steps.length} steps`),
    ),

    h('div', { className: 'cacao-chain-builder-content' },
      // Left: chain editor
      h('div', { className: 'cacao-chain-builder-editor' },
        // Add step controls
        h('div', { className: 'cacao-chain-builder-add' },
          h('select', {
            className: 'cacao-input',
            value: addType,
            onChange: (e) => setAddType(e.target.value),
          },
            ...STEP_TYPES.map(t =>
              h('option', { key: t.value, value: t.value }, `${t.icon} ${t.label}`)
            ),
          ),
          h('button', {
            className: 'cacao-btn cacao-btn-secondary',
            onClick: addStep,
          }, '+ Add Step'),
        ),

        // Steps list (droppable)
        h('div', {
          ref: dropRef,
          className: 'cacao-chain-builder-steps',
          onDragOver: (e) => e.preventDefault(),
          onDrop: handleDrop,
        },
          steps.length === 0
            ? h('div', { className: 'cacao-chain-builder-empty' },
                'Add steps to build your chain',
              )
            : steps.map((step, i) =>
                h('div', { key: i },
                  i > 0 && h('div', { className: 'cacao-chain-builder-connector' }, '↓'),
                  h(StepCard, {
                    step,
                    index: i,
                    onRemove: removeStep,
                    onUpdate: updateStep,
                    onMoveUp: (idx) => moveStep(idx, idx - 1),
                    onMoveDown: (idx) => moveStep(idx, idx + 1),
                    isFirst: i === 0,
                    isLast: i === steps.length - 1,
                  }),
                )
              ),
        ),
      ),

      // Right: input/output
      show_output && h('div', { className: 'cacao-chain-builder-io' },
        // Input
        h('div', { className: 'cacao-chain-builder-input' },
          h('label', { className: 'cacao-chain-builder-label' }, 'Input'),
          h('textarea', {
            className: 'cacao-input',
            rows: 4,
            value: inputValue,
            placeholder: 'Enter input value...',
            onChange: (e) => setInputValue(e.target.value),
          }),
          h('button', {
            className: 'cacao-btn cacao-btn-primary',
            onClick: runChain,
            disabled: loading || steps.length === 0,
          }, loading ? 'Running...' : 'Run Chain'),
        ),

        // Step results
        stepResults.length > 0 && h('div', { className: 'cacao-chain-builder-step-results' },
          h('label', { className: 'cacao-chain-builder-label' }, 'Step Results'),
          ...stepResults.map((r, i) =>
            h('div', {
              key: i,
              className: `cacao-chain-builder-step-result ${r.success ? '' : 'cacao-chain-builder-step-error'}`,
            },
              h('span', { className: 'cacao-chain-builder-step-name' }, r.name || `Step ${r.index}`),
              h('span', { className: 'cacao-chain-builder-step-value' },
                r.success
                  ? (typeof r.value === 'object' ? JSON.stringify(r.value) : String(r.value ?? ''))
                  : r.error,
              ),
            )
          ),
        ),

        // Final output
        h('div', { className: 'cacao-chain-builder-output' },
          h('label', { className: 'cacao-chain-builder-label' }, 'Output'),
          error && h('div', { className: 'cacao-alert cacao-alert-error' }, error),
          output !== null && h('pre', { className: 'cacao-chain-builder-result' },
            typeof output === 'object' ? JSON.stringify(output, null, 2) : String(output),
          ),
          output === null && !error && !loading && h('div', { className: 'cacao-chain-builder-placeholder' },
            'Run the chain to see output',
          ),
        ),
      ),
    ),
  );
}
