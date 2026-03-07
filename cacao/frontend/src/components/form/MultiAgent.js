const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function MultiAgent({ props }) {
  const {
    multi_id,
    mode = 'debate',
    agent_names = [],
    rounds = 3,
    title,
    height = '600px',
  } = props;

  const [inputText, setInputText] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [turns, setTurns] = useState([]);
  const [streamingTexts, setStreamingTexts] = useState({});
  const [routingInfo, setRoutingInfo] = useState(null);
  const [error, setError] = useState(null);
  const [isDone, setIsDone] = useState(false);
  const [finalData, setFinalData] = useState(null);
  const contentEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const handler = (msg) => {
      if (msg.multi_id !== multi_id) return;

      switch (msg.type) {
        case 'multi_agent:started':
          setIsRunning(true);
          setTurns([]);
          setStreamingTexts({});
          setRoutingInfo(null);
          setError(null);
          setIsDone(false);
          setFinalData(null);
          break;

        case 'multi_agent:routing':
          setRoutingInfo(msg);
          break;

        case 'multi_agent:turn':
          if (msg.status === 'done') {
            setTurns((prev) => [
              ...prev,
              {
                agent_name: msg.agent_name,
                agent_index: msg.agent_index,
                round: msg.round,
                content: msg.content,
                pipeline_step: msg.pipeline_step,
                pipeline_total: msg.pipeline_total,
              },
            ]);
            setStreamingTexts((prev) => {
              const next = { ...prev };
              delete next[msg.agent_index];
              return next;
            });
          } else {
            // running
            setStreamingTexts((prev) => ({ ...prev, [msg.agent_index]: '' }));
          }
          break;

        case 'multi_agent:delta':
          setStreamingTexts((prev) => ({
            ...prev,
            [msg.agent_index]: (prev[msg.agent_index] || '') + msg.delta,
          }));
          break;

        case 'multi_agent:done':
          setIsRunning(false);
          setIsDone(true);
          setFinalData(msg);
          break;

        case 'multi_agent:error':
          setIsRunning(false);
          setError(msg.error);
          break;
      }
    };

    cacaoWs.addListener(handler);
    return () => cacaoWs.removeListener(handler);
  }, [multi_id]);

  useEffect(() => {
    if (contentEndRef.current) {
      contentEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [turns, streamingTexts]);

  const handleSend = useCallback(() => {
    const text = inputText.trim();
    if (!text || isRunning) return;

    cacaoWs.send({
      type: 'multi_agent:run',
      multi_id,
      text,
    });

    setInputText('');
    if (inputRef.current) inputRef.current.focus();
  }, [inputText, isRunning, multi_id]);

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  // Assign colors to agents
  const agentColors = [
    'var(--accent-primary)',
    '#e57373',
    '#81c784',
    '#ffb74d',
    '#64b5f6',
    '#ba68c8',
  ];
  const getAgentColor = (idx) => agentColors[idx % agentColors.length];

  const modeLabel =
    mode === 'debate' ? 'Debate' : mode === 'router' ? 'Router' : 'Pipeline';

  const renderTurn = (turn, index) => {
    const color = getAgentColor(turn.agent_index);
    return h(
      'div',
      { className: 'c-multi-agent__turn', key: index },
      [
        h('div', { className: 'c-multi-agent__turn-header', key: 'hdr' }, [
          h(
            'span',
            {
              className: 'c-multi-agent__agent-name',
              style: { color },
              key: 'name',
            },
            turn.agent_name
          ),
          turn.round &&
            h(
              'span',
              { className: 'c-multi-agent__round-badge', key: 'round' },
              `Round ${turn.round}`
            ),
          turn.pipeline_step &&
            h(
              'span',
              { className: 'c-multi-agent__round-badge', key: 'pipe' },
              `Step ${turn.pipeline_step}/${turn.pipeline_total}`
            ),
        ]),
        h(
          'div',
          {
            className: 'c-multi-agent__turn-content',
            style: { borderLeftColor: color },
            key: 'content',
          },
          turn.content
        ),
      ]
    );
  };

  const renderStreaming = () => {
    return Object.entries(streamingTexts).map(([idxStr, text]) => {
      const idx = parseInt(idxStr, 10);
      const name = agent_names[idx] || `Agent ${idx + 1}`;
      const color = getAgentColor(idx);
      return h(
        'div',
        { className: 'c-multi-agent__turn c-multi-agent__turn--streaming', key: `stream-${idx}` },
        [
          h('div', { className: 'c-multi-agent__turn-header', key: 'hdr' }, [
            h(
              'span',
              { className: 'c-multi-agent__agent-name', style: { color }, key: 'name' },
              name
            ),
            h('span', { className: 'c-multi-agent__streaming-dot', key: 'dot' }),
          ]),
          h(
            'div',
            {
              className: 'c-multi-agent__turn-content',
              style: { borderLeftColor: color },
              key: 'content',
            },
            text || '...'
          ),
        ]
      );
    });
  };

  return h('div', { className: 'c-multi-agent', style: { height } }, [
    // Header
    h('div', { className: 'c-multi-agent__header', key: 'header' }, [
      h(
        'span',
        { className: 'c-multi-agent__title', key: 'title' },
        title || `Multi-Agent (${modeLabel})`
      ),
      h('div', { className: 'c-multi-agent__badges', key: 'badges' }, [
        h(
          'span',
          { className: 'c-multi-agent__mode-badge', key: 'mode' },
          modeLabel
        ),
        h(
          'span',
          { className: 'c-multi-agent__count-badge', key: 'count' },
          `${agent_names.length} agents`
        ),
      ]),
    ]),

    // Agent list
    h('div', { className: 'c-multi-agent__agents', key: 'agents' },
      agent_names.map((name, i) =>
        h(
          'span',
          {
            className: 'c-multi-agent__agent-chip',
            style: { borderColor: getAgentColor(i), color: getAgentColor(i) },
            key: i,
          },
          name
        )
      )
    ),

    // Content area
    h('div', { className: 'c-multi-agent__content', key: 'content' }, [
      // Router info
      routingInfo &&
        h('div', { className: 'c-multi-agent__routing', key: 'routing' }, [
          h('div', { className: 'c-multi-agent__routing-label', key: 'lbl' },
            routingInfo.status === 'done'
              ? `Routed to: ${routingInfo.chosen_agent}`
              : 'Routing decision...'
          ),
          routingInfo.reason &&
            h('div', { className: 'c-multi-agent__routing-reason', key: 'reason' }, routingInfo.reason),
        ]),

      // Turns
      ...turns.map(renderTurn),

      // Streaming turns
      ...renderStreaming(),

      // Error
      error &&
        h('div', { className: 'c-multi-agent__error', key: 'error' }, error),

      // Empty state
      !isRunning &&
        turns.length === 0 &&
        !error &&
        h(
          'div',
          { className: 'c-multi-agent__empty', key: 'empty' },
          `Send a message to start the ${modeLabel.toLowerCase()}.`
        ),

      h('div', { ref: contentEndRef, key: 'anchor' }),
    ]),

    // Input area
    h('div', { className: 'c-multi-agent__input-area', key: 'input' }, [
      h('textarea', {
        ref: inputRef,
        className: 'c-multi-agent__input',
        placeholder: `Type a message for the ${modeLabel.toLowerCase()}...`,
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
          className: 'c-multi-agent__send',
          onClick: handleSend,
          disabled: !inputText.trim() || isRunning,
          key: 'send',
        },
        isRunning
          ? h('span', { className: 'c-multi-agent__send-spinner' })
          : '\u25B6'
      ),
    ]),
  ]);
}
