/**
 * CostDashboard - Per-session token/cost tracking dashboard
 *
 * Shows real-time metrics: total cost, total tokens, call count,
 * per-model breakdown, and budget gauge.
 *
 * Props:
 *   title          - Dashboard title
 *   show_budget    - Show budget gauge
 *   show_breakdown - Show per-model breakdown table
 *   compact        - Compact layout mode
 *   cost_signal    - Signal holding cost summary data
 */

const { createElement: h, useState, useEffect, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function CostDashboard({ props }) {
  const {
    title = 'Usage & Costs',
    show_budget = true,
    show_breakdown = true,
    compact = false,
  } = props;

  const [summary, setSummary] = useState(null);

  const fetchCosts = useCallback(() => {
    cacaoWs.send({ type: 'cost:get' });
  }, []);

  useEffect(() => {
    const handler = (msg) => {
      if (msg.type === 'cost:summary') {
        setSummary(msg.summary);
      }
    };
    cacaoWs.addListener(handler);

    // Fetch initial data
    fetchCosts();

    // Poll every 5 seconds
    const interval = setInterval(fetchCosts, 5000);

    return () => {
      cacaoWs.removeListener(handler);
      clearInterval(interval);
    };
  }, [fetchCosts]);

  if (!summary) {
    return h('div', { className: 'cacao-cost-dashboard cacao-cost-empty' },
      h('h3', null, title),
      h('p', null, 'No usage data yet'),
    );
  }

  const { total_cost, total_tokens, call_count, by_model, budget } = summary;

  const formatCost = (c) => c < 0.01 ? `$${c.toFixed(4)}` : `$${c.toFixed(2)}`;
  const formatTokens = (t) => t >= 1000 ? `${(t / 1000).toFixed(1)}k` : `${t}`;

  // Budget percentage
  const budgetPct = budget.max_cost
    ? Math.min(100, (total_cost / budget.max_cost) * 100)
    : budget.max_tokens
      ? Math.min(100, (total_tokens / budget.max_tokens) * 100)
      : null;

  return h('div', { className: `cacao-cost-dashboard ${compact ? 'cacao-cost-compact' : ''}` },
    h('h3', { className: 'cacao-cost-title' }, title),

    // Metrics row
    h('div', { className: 'cacao-cost-metrics' },
      h('div', { className: 'cacao-cost-metric' },
        h('div', { className: 'cacao-cost-metric-value' }, formatCost(total_cost)),
        h('div', { className: 'cacao-cost-metric-label' }, 'Total Cost'),
      ),
      h('div', { className: 'cacao-cost-metric' },
        h('div', { className: 'cacao-cost-metric-value' }, formatTokens(total_tokens)),
        h('div', { className: 'cacao-cost-metric-label' }, 'Tokens'),
      ),
      h('div', { className: 'cacao-cost-metric' },
        h('div', { className: 'cacao-cost-metric-value' }, String(call_count)),
        h('div', { className: 'cacao-cost-metric-label' }, 'API Calls'),
      ),
    ),

    // Budget gauge
    show_budget && budgetPct !== null && h('div', { className: 'cacao-cost-budget' },
      h('div', { className: 'cacao-cost-budget-header' },
        h('span', null, 'Budget'),
        h('span', null,
          budget.max_cost ? `${formatCost(total_cost)} / ${formatCost(budget.max_cost)}`
            : `${formatTokens(total_tokens)} / ${formatTokens(budget.max_tokens)}`
        ),
      ),
      h('div', { className: 'cacao-cost-budget-bar' },
        h('div', {
          className: `cacao-cost-budget-fill ${
            budget.over_budget ? 'over' : budget.degraded ? 'warning' : ''
          }`,
          style: { width: `${budgetPct}%` },
        }),
      ),
      budget.degraded && !budget.over_budget && h('div', { className: 'cacao-cost-budget-note' },
        'Auto-degraded to cheaper model (80% threshold)',
      ),
      budget.over_budget && h('div', { className: 'cacao-cost-budget-note cacao-cost-budget-over' },
        'Budget exceeded — requests blocked',
      ),
    ),

    // Per-model breakdown
    show_breakdown && by_model && by_model.length > 0 && !compact && h('div', { className: 'cacao-cost-breakdown' },
      h('table', { className: 'cacao-cost-table' },
        h('thead', null,
          h('tr', null,
            h('th', null, 'Model'),
            h('th', null, 'Calls'),
            h('th', null, 'Tokens'),
            h('th', null, 'Cost'),
          ),
        ),
        h('tbody', null,
          by_model.map((m, i) =>
            h('tr', { key: i },
              h('td', null, `${m.provider}/${m.model}`),
              h('td', null, String(m.calls)),
              h('td', null, formatTokens(m.total_tokens)),
              h('td', null, formatCost(m.cost)),
            ),
          ),
        ),
      ),
    ),
  );
}
