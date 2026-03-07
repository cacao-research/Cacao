const { createElement: h, useState, useEffect } = React;
import { cacaoWs } from '../core/websocket.js';

export function ToolTimeline({ props }) {
  const {
    agent_id = null,
    title = 'Tool Call Timeline',
    height = '400px',
    show_args = true,
    show_results = true,
    show_cost = true,
    compact = false,
  } = props;

  const [steps, setSteps] = useState([]);
  const [expandedSteps, setExpandedSteps] = useState(new Set());

  useEffect(() => {
    const handler = (msg) => {
      // Filter by agent_id if specified
      if (agent_id && msg.agent_id !== agent_id) return;

      if (msg.type === 'agent:started') {
        setSteps([]);
        setExpandedSteps(new Set());
      } else if (msg.type === 'agent:step') {
        setSteps((prev) => {
          const existing = prev.findIndex((s) => s.id === msg.step.id);
          if (existing >= 0) {
            const updated = [...prev];
            updated[existing] = { ...msg.step, status: msg.status };
            return updated;
          }
          return [...prev, { ...msg.step, status: msg.status }];
        });
      }
    };

    cacaoWs.addListener(handler);
    return () => cacaoWs.removeListener(handler);
  }, [agent_id]);

  const toggleExpand = (stepId) => {
    setExpandedSteps((prev) => {
      const next = new Set(prev);
      if (next.has(stepId)) next.delete(stepId);
      else next.add(stepId);
      return next;
    });
  };

  const getStepColor = (type) => {
    switch (type) {
      case 'think':
        return 'var(--accent-primary)';
      case 'tool_call':
        return '#ffb74d';
      case 'response':
        return '#81c784';
      case 'error':
        return 'var(--danger)';
      default:
        return 'var(--text-muted)';
    }
  };

  const getStepLabel = (step) => {
    switch (step.type) {
      case 'think':
        return 'Reasoning';
      case 'tool_call':
        return `Tool: ${step.tool_name || 'unknown'}`;
      case 'response':
        return 'Final Response';
      case 'error':
        return 'Error';
      default:
        return step.type;
    }
  };

  const formatDuration = (d) => {
    if (!d || d <= 0) return '';
    if (d < 1) return `${(d * 1000).toFixed(0)}ms`;
    return `${d.toFixed(1)}s`;
  };

  const renderStep = (step, index) => {
    const isExpanded = expandedSteps.has(step.id);
    const isActive = step.status === 'running';
    const color = getStepColor(step.type);
    const hasExpandable =
      (show_args && step.tool_args) ||
      (show_results && step.tool_result) ||
      (step.type === 'think' && step.content) ||
      (step.type === 'response' && step.content);

    return h(
      'div',
      {
        className: `c-tool-timeline__step ${isActive ? 'c-tool-timeline__step--active' : ''} ${compact ? 'c-tool-timeline__step--compact' : ''}`,
        key: step.id || index,
      },
      [
        // Timeline connector
        h('div', { className: 'c-tool-timeline__connector', key: 'conn' }, [
          h('div', {
            className: 'c-tool-timeline__dot',
            style: { borderColor: color, background: isActive ? color : 'transparent' },
            key: 'dot',
          }),
          index < steps.length - 1 &&
            h('div', { className: 'c-tool-timeline__line', key: 'line' }),
        ]),

        // Step content
        h(
          'div',
          {
            className: 'c-tool-timeline__step-body',
            onClick: hasExpandable ? () => toggleExpand(step.id) : undefined,
            style: hasExpandable ? { cursor: 'pointer' } : undefined,
            key: 'body',
          },
          [
            h('div', { className: 'c-tool-timeline__step-header', key: 'hdr' }, [
              h(
                'span',
                { className: 'c-tool-timeline__step-label', style: { color }, key: 'lbl' },
                getStepLabel(step)
              ),
              h('div', { className: 'c-tool-timeline__step-meta', key: 'meta' }, [
                step.duration > 0 &&
                  h(
                    'span',
                    { className: 'c-tool-timeline__duration', key: 'dur' },
                    formatDuration(step.duration)
                  ),
                show_cost &&
                  step.tokens > 0 &&
                  h(
                    'span',
                    { className: 'c-tool-timeline__tokens', key: 'tok' },
                    `${step.tokens.toLocaleString()} tok`
                  ),
                show_cost &&
                  step.cost > 0 &&
                  h(
                    'span',
                    { className: 'c-tool-timeline__cost', key: 'cost' },
                    `$${step.cost.toFixed(4)}`
                  ),
                isActive &&
                  h('span', { className: 'c-tool-timeline__spinner', key: 'spin' }),
                hasExpandable &&
                  h(
                    'span',
                    { className: 'c-tool-timeline__expand-icon', key: 'expand' },
                    isExpanded ? '\u25BC' : '\u25B6'
                  ),
              ]),
            ]),

            // Expandable details
            isExpanded &&
              h('div', { className: 'c-tool-timeline__details', key: 'details' }, [
                show_args &&
                  step.tool_args &&
                  h('div', { className: 'c-tool-timeline__detail-section', key: 'args' }, [
                    h('div', { className: 'c-tool-timeline__detail-label', key: 'lbl' }, 'Arguments'),
                    h('pre', { className: 'c-tool-timeline__detail-code', key: 'code' },
                      JSON.stringify(step.tool_args, null, 2)
                    ),
                  ]),
                show_results &&
                  step.tool_result &&
                  h('div', { className: 'c-tool-timeline__detail-section', key: 'result' }, [
                    h('div', { className: 'c-tool-timeline__detail-label', key: 'lbl' }, 'Result'),
                    h('pre', { className: 'c-tool-timeline__detail-code', key: 'code' }, step.tool_result),
                  ]),
                (step.type === 'think' || step.type === 'response') &&
                  step.content &&
                  h('div', { className: 'c-tool-timeline__detail-section', key: 'text' }, [
                    h('div', { className: 'c-tool-timeline__detail-label', key: 'lbl' }, 'Content'),
                    h('div', { className: 'c-tool-timeline__detail-text', key: 'txt' }, step.content),
                  ]),
              ]),
          ]
        ),
      ]
    );
  };

  return h('div', { className: 'c-tool-timeline', style: { height } }, [
    // Header
    title &&
      h('div', { className: 'c-tool-timeline__header', key: 'header' }, title),

    // Steps
    h('div', { className: 'c-tool-timeline__steps', key: 'steps' }, [
      steps.length === 0 &&
        h(
          'div',
          { className: 'c-tool-timeline__empty', key: 'empty' },
          'No agent steps yet.'
        ),
      ...steps.map(renderStep),
    ]),
  ]);
}
