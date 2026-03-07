const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function Agent({ props }) {
  const {
    agent_id,
    title,
    placeholder = 'Ask the agent...',
    height = '600px',
    show_steps = true,
    show_cost = true,
    has_tools = false,
    model = '',
    provider = '',
  } = props;

  const [inputText, setInputText] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [steps, setSteps] = useState([]);
  const [streamingText, setStreamingText] = useState('');
  const [finalResponse, setFinalResponse] = useState('');
  const [error, setError] = useState(null);
  const [totalCost, setTotalCost] = useState(0);
  const [totalTokens, setTotalTokens] = useState(0);
  const [iterations, setIterations] = useState(0);
  const stepsEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const handler = (msg) => {
      if (msg.agent_id !== agent_id) return;

      switch (msg.type) {
        case 'agent:started':
          setIsRunning(true);
          setSteps([]);
          setStreamingText('');
          setFinalResponse('');
          setError(null);
          break;

        case 'agent:step':
          if (msg.status === 'done') {
            setSteps((prev) => {
              const existing = prev.findIndex((s) => s.id === msg.step.id);
              if (existing >= 0) {
                const updated = [...prev];
                updated[existing] = { ...msg.step, status: 'done' };
                return updated;
              }
              return [...prev, { ...msg.step, status: 'done' }];
            });
            setStreamingText('');
          } else {
            setSteps((prev) => {
              const existing = prev.findIndex((s) => s.id === msg.step.id);
              if (existing >= 0) return prev;
              return [...prev, { ...msg.step, status: 'running' }];
            });
          }
          break;

        case 'agent:delta':
          setStreamingText((prev) => prev + msg.delta);
          break;

        case 'agent:done':
          setIsRunning(false);
          setTotalCost(msg.total_cost || 0);
          setTotalTokens(msg.total_tokens || 0);
          setIterations(msg.iterations || 0);
          // Find the last response step
          if (msg.steps && msg.steps.length > 0) {
            const lastResponse = [...msg.steps].reverse().find((s) => s.type === 'response');
            if (lastResponse) setFinalResponse(lastResponse.content);
          }
          break;

        case 'agent:error':
          setIsRunning(false);
          setError(msg.error);
          break;

        case 'agent:budget_update':
          if (msg.summary) {
            setTotalCost(msg.summary.total_cost || 0);
            setTotalTokens(msg.summary.total_tokens || 0);
          }
          break;
      }
    };

    cacaoWs.addListener(handler);
    return () => cacaoWs.removeListener(handler);
  }, [agent_id]);

  useEffect(() => {
    if (stepsEndRef.current) {
      stepsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [steps, streamingText]);

  const handleSend = useCallback(() => {
    const text = inputText.trim();
    if (!text || isRunning) return;

    cacaoWs.send({
      type: 'agent:run',
      agent_id,
      text,
    });

    setInputText('');
    if (inputRef.current) inputRef.current.focus();
  }, [inputText, isRunning, agent_id]);

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  const renderStepIcon = (step) => {
    switch (step.type) {
      case 'think':
        return '\u{1F9E0}';
      case 'tool_call':
        return '\u2699\uFE0F';
      case 'response':
        return '\u2705';
      case 'error':
        return '\u274C';
      default:
        return '\u25CF';
    }
  };

  const renderStep = (step, index) => {
    const isActive = step.status === 'running';

    return h(
      'div',
      {
        className: `c-agent-step c-agent-step--${step.type} ${isActive ? 'c-agent-step--active' : ''}`,
        key: step.id || index,
      },
      [
        h('div', { className: 'c-agent-step__header', key: 'hdr' }, [
          h('span', { className: 'c-agent-step__icon', key: 'icon' }, renderStepIcon(step)),
          h(
            'span',
            { className: 'c-agent-step__type', key: 'type' },
            step.type === 'tool_call' ? `Tool: ${step.tool_name || 'unknown'}` : step.type
          ),
          step.duration > 0 &&
            h('span', { className: 'c-agent-step__duration', key: 'dur' }, `${step.duration.toFixed(1)}s`),
          show_cost &&
            step.cost > 0 &&
            h('span', { className: 'c-agent-step__cost', key: 'cost' }, `$${step.cost.toFixed(4)}`),
          isActive &&
            h('span', { className: 'c-agent-step__spinner', key: 'spin' }),
        ]),
        // Tool args
        step.tool_args &&
          h(
            'div',
            { className: 'c-agent-step__args', key: 'args' },
            h('pre', null, JSON.stringify(step.tool_args, null, 2))
          ),
        // Tool result
        step.tool_result &&
          h('div', { className: 'c-agent-step__result', key: 'result' }, [
            h('span', { className: 'c-agent-step__result-label', key: 'lbl' }, 'Result:'),
            h('pre', { key: 'pre' }, step.tool_result),
          ]),
        // Think/response content
        step.type !== 'tool_call' &&
          step.content &&
          step.status === 'done' &&
          h(
            'div',
            { className: 'c-agent-step__content', key: 'content' },
            step.content
          ),
      ]
    );
  };

  return h('div', { className: 'c-agent', style: { height } }, [
    // Header
    h('div', { className: 'c-agent__header', key: 'header' }, [
      h(
        'span',
        { className: 'c-agent__title', key: 'title' },
        title || 'Agent'
      ),
      h('div', { className: 'c-agent__meta', key: 'meta' }, [
        h('span', { className: 'c-agent__badge', key: 'model' }, `${provider}/${model}`),
        has_tools && h('span', { className: 'c-agent__badge c-agent__badge--tools', key: 'tools' }, 'Tools'),
      ]),
    ]),

    // Main content area
    h('div', { className: 'c-agent__body', key: 'body' }, [
      // Steps panel
      show_steps &&
        (steps.length > 0 || isRunning) &&
        h('div', { className: 'c-agent__steps', key: 'steps' }, [
          h('div', { className: 'c-agent__steps-header', key: 'shdr' }, 'ReAct Trace'),
          h('div', { className: 'c-agent__steps-list', key: 'slist' }, [
            ...steps.map(renderStep),
            // Streaming text for current think step
            isRunning &&
              streamingText &&
              h(
                'div',
                { className: 'c-agent-step c-agent-step--think c-agent-step--active', key: 'streaming' },
                [
                  h('div', { className: 'c-agent-step__content', key: 'content' }, streamingText),
                ]
              ),
            h('div', { ref: stepsEndRef, key: 'anchor' }),
          ]),
        ]),

      // Final response
      finalResponse &&
        !isRunning &&
        h('div', { className: 'c-agent__response', key: 'response' }, [
          h('div', { className: 'c-agent__response-label', key: 'lbl' }, 'Response'),
          h('div', { className: 'c-agent__response-content', key: 'content' }, finalResponse),
        ]),

      // Error
      error &&
        h('div', { className: 'c-agent__error', key: 'error' }, error),

      // Cost summary
      show_cost &&
        (totalCost > 0 || totalTokens > 0) &&
        !isRunning &&
        h('div', { className: 'c-agent__cost-summary', key: 'cost' }, [
          totalCost > 0 &&
            h('span', { key: 'cost' }, `Cost: $${totalCost.toFixed(4)}`),
          totalTokens > 0 &&
            h('span', { key: 'tokens' }, `Tokens: ${totalTokens.toLocaleString()}`),
          iterations > 0 &&
            h('span', { key: 'iter' }, `Iterations: ${iterations}`),
        ]),

      // Empty state
      !isRunning &&
        steps.length === 0 &&
        !finalResponse &&
        !error &&
        h('div', { className: 'c-agent__empty', key: 'empty' }, 'Send a message to start the agent.'),
    ]),

    // Input area
    h('div', { className: 'c-agent__input-area', key: 'input' }, [
      h('textarea', {
        ref: inputRef,
        className: 'c-agent__input',
        placeholder,
        value: inputText,
        rows: 1,
        disabled: isRunning,
        onChange: (e) => setInputText(e.target.value),
        onKeyDown: handleKeyDown,
        key: 'textarea',
      }),
      h(
        'button',
        {
          className: 'c-agent__send',
          onClick: handleSend,
          disabled: !inputText.trim() || isRunning,
          title: 'Run agent',
          key: 'send',
        },
        isRunning
          ? h('span', { className: 'c-agent__send-spinner' })
          : h(
              'svg',
              {
                width: 18,
                height: 18,
                viewBox: '0 0 24 24',
                fill: 'none',
                stroke: 'currentColor',
                strokeWidth: 2,
                strokeLinecap: 'round',
                strokeLinejoin: 'round',
              },
              [
                h('line', { x1: 22, y1: 2, x2: 11, y2: 13, key: 'l1' }),
                h('polygon', { points: '22 2 15 22 11 13 2 9 22 2', key: 'p1' }),
              ]
            )
      ),
    ]),
  ]);
}
