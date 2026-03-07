/**
 * ModelPicker - Auto-detect available LLM providers/models
 *
 * Fetches models from Prompture's discovery system and displays
 * them in a searchable, grouped select component.
 *
 * Props:
 *   signal   - Signal to bind selected model string to
 *   label    - Label for the picker
 *   grouped  - Group models by provider
 *   default  - Default model selection
 */

const { createElement: h, useState, useEffect, useCallback, useMemo, useRef } = React;
import { cacaoWs } from '../core/websocket.js';

export function ModelPicker({ props }) {
  const {
    signal,
    label = 'Model',
    grouped = true,
  } = props;

  const [models, setModels] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [selectedModel, setSelectedModel] = useState(props.default || '');
  const dropdownRef = useRef(null);
  const signalName = signal?.__signal__;

  // Subscribe to signal updates
  useEffect(() => {
    if (!signalName) return;
    const handler = (msg) => {
      if (msg.type === 'update' && msg.signal === signalName) {
        setSelectedModel(msg.value || '');
      }
    };
    cacaoWs.addListener(handler);
    // Get initial value from signals
    if (cacaoWs.signals[signalName] !== undefined) {
      setSelectedModel(cacaoWs.signals[signalName] || '');
    }
    return () => cacaoWs.removeListener(handler);
  }, [signalName]);

  // Fetch models
  useEffect(() => {
    const handler = (msg) => {
      if (msg.type === 'models:result') {
        setModels(msg.models);
        setLoading(false);
        cacaoWs.removeListener(handler);
      } else if (msg.type === 'models:error') {
        setError(msg.error);
        setLoading(false);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);
    cacaoWs.send({ type: 'models:discover', grouped });

    return () => cacaoWs.removeListener(handler);
  }, [grouped]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleSelect = useCallback((modelStr) => {
    setSelectedModel(modelStr);
    setIsOpen(false);
    setSearch('');

    // Update signal
    if (signalName) {
      cacaoWs.send({
        type: 'event',
        name: `signal:set:${signalName}`,
        data: { value: modelStr },
      });
    }
  }, [signalName]);

  // Build filtered model list
  const filteredModels = useMemo(() => {
    if (!models) return [];

    const q = search.toLowerCase();

    if (grouped && typeof models === 'object' && !Array.isArray(models)) {
      // Grouped format: { provider: { display_name, models: [...] } }
      const result = [];
      for (const [provider, info] of Object.entries(models)) {
        const providerModels = (info.models || []).filter(m => {
          const name = typeof m === 'string' ? m : (m.model || m.id || '');
          return !q || name.toLowerCase().includes(q) || provider.toLowerCase().includes(q);
        });
        if (providerModels.length > 0) {
          result.push({
            provider,
            displayName: info.display_name || provider,
            models: providerModels,
          });
        }
      }
      return result;
    }

    // Flat list
    const list = Array.isArray(models) ? models : [];
    return list.filter(m => {
      const name = typeof m === 'string' ? m : (m.model || m.id || '');
      return !q || name.toLowerCase().includes(q);
    });
  }, [models, search, grouped]);

  if (loading) {
    return h('div', { className: 'cacao-model-picker' },
      h('label', { className: 'cacao-input-label' }, label),
      h('div', { className: 'cacao-model-picker-loading' }, 'Discovering models...'),
    );
  }

  if (error) {
    return h('div', { className: 'cacao-model-picker' },
      h('label', { className: 'cacao-input-label' }, label),
      h('div', { className: 'cacao-alert cacao-alert-error' }, error),
    );
  }

  return h('div', { className: 'cacao-model-picker', ref: dropdownRef },
    h('label', { className: 'cacao-input-label' }, label),
    h('div', {
      className: `cacao-model-picker-trigger ${isOpen ? 'open' : ''}`,
      onClick: () => setIsOpen(!isOpen),
    },
      h('span', null, selectedModel || 'Select a model...'),
      h('span', { className: 'cacao-model-picker-arrow' }, isOpen ? '▲' : '▼'),
    ),

    isOpen && h('div', { className: 'cacao-model-picker-dropdown' },
      h('input', {
        className: 'cacao-model-picker-search',
        type: 'text',
        placeholder: 'Search models...',
        value: search,
        onChange: (e) => setSearch(e.target.value),
        autoFocus: true,
      }),

      h('div', { className: 'cacao-model-picker-list' },
        grouped && Array.isArray(filteredModels) && filteredModels.map((group, gi) =>
          h('div', { key: gi, className: 'cacao-model-picker-group' },
            h('div', { className: 'cacao-model-picker-group-header' }, group.displayName),
            group.models.map((m, mi) => {
              const modelStr = typeof m === 'string' ? m : (m.model || m.id || '');
              return h('div', {
                key: mi,
                className: `cacao-model-picker-item ${modelStr === selectedModel ? 'selected' : ''}`,
                onClick: () => handleSelect(modelStr),
              }, modelStr);
            }),
          ),
        ),

        !grouped && Array.isArray(filteredModels) && filteredModels.map((m, i) => {
          const modelStr = typeof m === 'string' ? m : (m.model || m.id || '');
          return h('div', {
            key: i,
            className: `cacao-model-picker-item ${modelStr === selectedModel ? 'selected' : ''}`,
            onClick: () => handleSelect(modelStr),
          }, modelStr);
        }),

        filteredModels.length === 0 && h('div', { className: 'cacao-model-picker-empty' },
          'No models found',
        ),
      ),
    ),
  );
}
