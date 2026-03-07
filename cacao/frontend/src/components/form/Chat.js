/**
 * Chat - Interactive chat component with streaming and LLM support
 *
 * Renders a message list with user/assistant bubbles, a text input,
 * and handles real-time streaming of assistant responses via WebSocket.
 *
 * Props:
 *   signal       - Signal holding the message array [{role, content}]
 *   on_send      - Event name fired when user sends a message
 *   placeholder  - Input placeholder text
 *   title        - Optional header title
 *   height       - Container height (default: "500px")
 *   show_clear   - Show clear conversation button
 *   on_clear     - Event name fired when user clears chat
 *   persist      - Enable localStorage persistence for chat messages
 *   llm_enabled  - Whether LLM backend is active (sends chat:send instead of event)
 */

const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function Chat({ props }) {
  const {
    signal,
    on_send,
    on_clear,
    placeholder = 'Type a message...',
    title,
    height = '500px',
    show_clear = false,
    persist = false,
    llm_enabled = false,
  } = props;

  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [streamingText, setStreamingText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const signalName = signal?.__signal__;
  const storageKey = persist && signalName ? `cacao-chat-${signalName}` : null;

  // Load from localStorage on mount (before signal subscription)
  useEffect(() => {
    if (storageKey) {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) {
          const parsed = JSON.parse(saved);
          if (Array.isArray(parsed) && parsed.length > 0) {
            setMessages(parsed);
          }
        }
      } catch { /* ignore parse errors */ }
    }
  }, [storageKey]);

  // Subscribe to signal for message history
  useEffect(() => {
    if (signalName) {
      const unsubscribe = cacaoWs.subscribe((signals) => {
        if (signals[signalName] !== undefined) {
          const newMsgs = signals[signalName];
          setMessages(newMsgs);
          // Persist to localStorage
          if (storageKey && Array.isArray(newMsgs)) {
            try { localStorage.setItem(storageKey, JSON.stringify(newMsgs)); } catch {}
          }
        }
      });
      const initial = cacaoWs.getSignal(signalName);
      if (initial !== undefined && Array.isArray(initial) && initial.length > 0) {
        setMessages(initial);
      }
      return unsubscribe;
    }
  }, [signalName, storageKey]);

  // Listen for chat_delta and chat_done messages (WebSocket or static mode)
  useEffect(() => {
    if (!signalName) return;

    const unsubscribe = cacaoWs.subscribeChatStream((msg) => {
      if (msg.signal !== signalName) return;

      if (msg.type === 'chat_delta') {
        setIsStreaming(true);
        setStreamingText((prev) => prev + msg.delta);
      } else if (msg.type === 'chat_done') {
        setStreamingText('');
        setIsStreaming(false);
      }
    });

    return unsubscribe;
  }, [signalName]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, streamingText]);

  const handleSend = useCallback(() => {
    const text = inputText.trim();
    if (!text || isStreaming) return;

    if (llm_enabled && signalName) {
      // LLM mode: send via chat:send protocol
      cacaoWs.sendChatMessage(signalName, text);
    } else {
      // Manual mode: fire event
      const eventName = on_send?.__event__ || on_send;
      if (eventName) {
        cacaoWs.sendEvent(eventName, { text });
      }
    }

    setInputText('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [inputText, isStreaming, on_send, llm_enabled, signalName]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  const handleClear = useCallback(() => {
    const eventName = on_clear?.__event__ || on_clear;
    if (eventName) {
      cacaoWs.sendEvent(eventName, {});
    }
    // Clear localStorage too
    if (storageKey) {
      try { localStorage.removeItem(storageKey); } catch {}
    }
  }, [on_clear, storageKey]);

  // Render tool calls inline
  const renderToolCalls = (toolCalls) => {
    if (!toolCalls || !toolCalls.length) return null;
    return toolCalls.map((tc, i) => {
      let args = tc.arguments;
      try {
        args = JSON.stringify(JSON.parse(tc.arguments), null, 2);
      } catch { /* keep as-is */ }

      return h('div', { className: 'c-chat-tool-call', key: `tc-${i}` }, [
        h('div', { className: 'c-chat-tool-call__header', key: 'hdr' }, [
          h('span', { className: 'c-chat-tool-call__icon', key: 'icon' }, '\u2699'),
          h('span', { className: 'c-chat-tool-call__name', key: 'name' }, tc.name),
        ]),
        h('pre', { className: 'c-chat-tool-call__args', key: 'args' }, args),
      ]);
    });
  };

  // Render a single message bubble
  const renderMessage = (msg, index) => {
    const isUser = msg.role === 'user';
    const isError = msg.role === 'error';
    const isTool = msg.role === 'tool';

    // Tool result messages
    if (isTool) {
      return h('div', {
        className: 'c-chat-message c-chat-message--tool',
        key: index,
      }, [
        h('div', { className: 'c-chat-message__role', key: 'role' },
          `\u2699 ${msg.name || 'Tool'}`
        ),
        h('div', { className: 'c-chat-message__content', key: 'content' }, msg.content),
      ]);
    }

    return h('div', {
      className: `c-chat-message c-chat-message--${isError ? 'error' : isUser ? 'user' : 'assistant'}`,
      key: index,
    }, [
      h('div', { className: 'c-chat-message__role', key: 'role' },
        isError ? 'Error' : isUser ? 'You' : 'Assistant'
      ),
      // Tool calls (shown before text content for assistant messages)
      msg.tool_calls && renderToolCalls(msg.tool_calls),
      h('div', { className: 'c-chat-message__content', key: 'content' }, msg.content),
    ]);
  };

  // Build the message list including streaming message
  const allMessages = [...messages];

  return h('div', { className: 'c-chat', style: { height } }, [
    // Header
    title && h('div', { className: 'c-chat__header', key: 'header' }, [
      h('span', { className: 'c-chat__title', key: 'title' }, title),
      show_clear && h('button', {
        className: 'c-chat__clear',
        onClick: handleClear,
        title: 'Clear conversation',
        key: 'clear',
      }, '\u00D7'),
    ]),

    // Messages area
    h('div', { className: 'c-chat__messages', key: 'messages' }, [
      // Empty state
      allMessages.length === 0 && !isStreaming && h('div', {
        className: 'c-chat__empty',
        key: 'empty',
      }, 'Start a conversation...'),

      // Message bubbles
      ...allMessages.map(renderMessage),

      // Streaming message (in progress)
      isStreaming && streamingText && h('div', {
        className: 'c-chat-message c-chat-message--assistant c-chat-message--streaming',
        key: 'streaming',
      }, [
        h('div', { className: 'c-chat-message__role', key: 'role' }, 'Assistant'),
        h('div', { className: 'c-chat-message__content', key: 'content' }, streamingText),
      ]),

      // Streaming indicator (waiting for first chunk)
      isStreaming && !streamingText && h('div', {
        className: 'c-chat-message c-chat-message--assistant c-chat-message--streaming',
        key: 'thinking',
      }, [
        h('div', { className: 'c-chat-message__role', key: 'role' }, 'Assistant'),
        h('div', { className: 'c-chat-message__content c-chat-message__typing', key: 'content' },
          h('span', { className: 'c-chat__dots' }, [
            h('span', { key: 'd1' }, '.'),
            h('span', { key: 'd2' }, '.'),
            h('span', { key: 'd3' }, '.'),
          ])
        ),
      ]),

      // Scroll anchor
      h('div', { ref: messagesEndRef, key: 'anchor' }),
    ]),

    // Input area
    h('div', { className: 'c-chat__input-area', key: 'input' }, [
      h('textarea', {
        ref: inputRef,
        className: 'c-chat__input',
        placeholder,
        value: inputText,
        rows: 1,
        disabled: isStreaming,
        onChange: (e) => setInputText(e.target.value),
        onKeyDown: handleKeyDown,
        key: 'textarea',
      }),
      h('button', {
        className: 'c-chat__send',
        onClick: handleSend,
        disabled: !inputText.trim() || isStreaming,
        title: 'Send message',
        key: 'send',
      }, h('svg', {
        width: 18, height: 18, viewBox: '0 0 24 24',
        fill: 'none', stroke: 'currentColor', strokeWidth: 2,
        strokeLinecap: 'round', strokeLinejoin: 'round',
      }, [
        h('line', { x1: 22, y1: 2, x2: 11, y2: 13, key: 'l1' }),
        h('polygon', { points: '22 2 15 22 11 13 2 9 22 2', key: 'p1' }),
      ])),
    ]),
  ]);
}
