const { createElement: h, useState, useEffect, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function BudgetGauge({ props }) {
  const {
    max_cost = null,
    max_tokens = null,
    warn_threshold = 0.8,
    title = 'Budget',
    show_breakdown = true,
    compact = false,
  } = props;

  const [summary, setSummary] = useState(null);
  const [pollInterval, setPollInterval] = useState(null);

  // Request budget summary
  const fetchBudget = useCallback(() => {
    cacaoWs.send({ type: 'budget:get' });
  }, []);

  useEffect(() => {
    const handler = (msg) => {
      if (msg.type === 'budget:summary') {
        setSummary(msg.summary);
      }
      // Also listen for agent budget updates
      if (msg.type === 'agent:budget_update' && msg.summary) {
        setSummary(msg.summary);
      }
      // Update on cost:summary too (from CostDashboard requests)
      if (msg.type === 'cost:summary' && msg.summary) {
        setSummary(msg.summary);
      }
    };

    cacaoWs.addListener(handler);

    // Initial fetch
    fetchBudget();

    // Poll every 5 seconds for live updates
    const interval = setInterval(fetchBudget, 5000);
    setPollInterval(interval);

    return () => {
      cacaoWs.removeListener(handler);
      clearInterval(interval);
    };
  }, [fetchBudget]);

  const totalCost = summary?.total_cost || 0;
  const totalTokens = summary?.total_tokens || 0;
  const callCount = summary?.call_count || 0;

  // Calculate gauge percentages
  const costPercent = max_cost ? Math.min((totalCost / max_cost) * 100, 100) : 0;
  const tokenPercent = max_tokens ? Math.min((totalTokens / max_tokens) * 100, 100) : 0;

  const getGaugeColor = (percent) => {
    if (percent >= 100) return 'var(--danger)';
    if (percent >= warn_threshold * 100) return '#ffb74d';
    return 'var(--success, #81c784)';
  };

  const renderGauge = (label, current, max, unit, percent) => {
    const color = getGaugeColor(percent);
    const displayCurrent =
      unit === '$' ? `$${current.toFixed(4)}` : current.toLocaleString();
    const displayMax =
      unit === '$' ? `$${max.toFixed(2)}` : max.toLocaleString();

    if (compact) {
      return h('div', { className: 'c-budget-gauge__compact-row', key: label }, [
        h('span', { className: 'c-budget-gauge__compact-label', key: 'lbl' }, label),
        h('div', { className: 'c-budget-gauge__compact-bar-wrap', key: 'bar' }, [
          h('div', {
            className: 'c-budget-gauge__compact-bar',
            style: { width: `${percent}%`, background: color },
            key: 'fill',
          }),
        ]),
        h(
          'span',
          { className: 'c-budget-gauge__compact-value', style: { color }, key: 'val' },
          `${displayCurrent} / ${displayMax}`
        ),
      ]);
    }

    return h('div', { className: 'c-budget-gauge__gauge', key: label }, [
      h('div', { className: 'c-budget-gauge__gauge-header', key: 'hdr' }, [
        h('span', { className: 'c-budget-gauge__gauge-label', key: 'lbl' }, label),
        h(
          'span',
          { className: 'c-budget-gauge__gauge-value', style: { color }, key: 'val' },
          `${displayCurrent} / ${displayMax}`
        ),
      ]),
      h('div', { className: 'c-budget-gauge__bar-track', key: 'track' }, [
        h('div', {
          className: 'c-budget-gauge__bar-fill',
          style: { width: `${percent}%`, background: color },
          key: 'fill',
        }),
        // Warn threshold marker
        h('div', {
          className: 'c-budget-gauge__threshold-mark',
          style: { left: `${warn_threshold * 100}%` },
          key: 'mark',
        }),
      ]),
      h(
        'div',
        { className: 'c-budget-gauge__gauge-percent', style: { color }, key: 'pct' },
        `${percent.toFixed(1)}%`
      ),
    ]);
  };

  // Alert states
  const costOverBudget = max_cost && totalCost >= max_cost;
  const tokenOverBudget = max_tokens && totalTokens >= max_tokens;
  const costWarning = max_cost && totalCost >= max_cost * warn_threshold && !costOverBudget;
  const tokenWarning = max_tokens && totalTokens >= max_tokens * warn_threshold && !tokenOverBudget;

  if (compact) {
    return h('div', { className: 'c-budget-gauge c-budget-gauge--compact' }, [
      title && h('span', { className: 'c-budget-gauge__compact-title', key: 'title' }, title),
      max_cost !== null && renderGauge('Cost', totalCost, max_cost, '$', costPercent),
      max_tokens !== null && renderGauge('Tokens', totalTokens, max_tokens, 'tok', tokenPercent),
      max_cost === null && max_tokens === null &&
        h('span', { className: 'c-budget-gauge__compact-usage', key: 'usage' },
          `$${totalCost.toFixed(4)} \u00B7 ${totalTokens.toLocaleString()} tokens \u00B7 ${callCount} calls`
        ),
    ]);
  }

  return h('div', { className: 'c-budget-gauge' }, [
    // Header
    h('div', { className: 'c-budget-gauge__header', key: 'header' }, [
      h('span', { className: 'c-budget-gauge__title', key: 'title' }, title),
      h('span', { className: 'c-budget-gauge__calls', key: 'calls' }, `${callCount} calls`),
    ]),

    // Alerts
    (costOverBudget || tokenOverBudget) &&
      h('div', { className: 'c-budget-gauge__alert c-budget-gauge__alert--danger', key: 'over' },
        'Budget exceeded! Requests may be blocked.'
      ),
    (costWarning || tokenWarning) &&
      h('div', { className: 'c-budget-gauge__alert c-budget-gauge__alert--warn', key: 'warn' },
        `Approaching budget limit (${(warn_threshold * 100).toFixed(0)}% threshold).`
      ),

    // Gauges
    h('div', { className: 'c-budget-gauge__gauges', key: 'gauges' }, [
      max_cost !== null && renderGauge('Cost', totalCost, max_cost, '$', costPercent),
      max_tokens !== null && renderGauge('Tokens', totalTokens, max_tokens, 'tok', tokenPercent),
    ]),

    // Usage summary when no limits set
    max_cost === null &&
      max_tokens === null &&
      h('div', { className: 'c-budget-gauge__usage', key: 'usage' }, [
        h('div', { className: 'c-budget-gauge__usage-item', key: 'cost' }, [
          h('span', { className: 'c-budget-gauge__usage-label', key: 'lbl' }, 'Total Cost'),
          h('span', { className: 'c-budget-gauge__usage-value', key: 'val' }, `$${totalCost.toFixed(4)}`),
        ]),
        h('div', { className: 'c-budget-gauge__usage-item', key: 'tokens' }, [
          h('span', { className: 'c-budget-gauge__usage-label', key: 'lbl' }, 'Total Tokens'),
          h('span', { className: 'c-budget-gauge__usage-value', key: 'val' }, totalTokens.toLocaleString()),
        ]),
      ]),

    // Breakdown table
    show_breakdown &&
      summary?.by_model &&
      summary.by_model.length > 0 &&
      h('div', { className: 'c-budget-gauge__breakdown', key: 'breakdown' }, [
        h('div', { className: 'c-budget-gauge__breakdown-title', key: 'title' }, 'Per-Model Breakdown'),
        h('table', { className: 'c-budget-gauge__table', key: 'table' }, [
          h('thead', { key: 'thead' },
            h('tr', null, [
              h('th', { key: 'model' }, 'Model'),
              h('th', { key: 'calls' }, 'Calls'),
              h('th', { key: 'tokens' }, 'Tokens'),
              h('th', { key: 'cost' }, 'Cost'),
            ])
          ),
          h('tbody', { key: 'tbody' },
            summary.by_model.map((entry, i) =>
              h('tr', { key: i }, [
                h('td', { key: 'model' }, `${entry.provider}/${entry.model}`),
                h('td', { key: 'calls' }, entry.calls),
                h('td', { key: 'tokens' }, entry.total_tokens.toLocaleString()),
                h('td', { key: 'cost' }, `$${entry.cost.toFixed(4)}`),
              ])
            )
          ),
        ]),
      ]),
  ]);
}
