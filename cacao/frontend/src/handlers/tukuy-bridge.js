/**
 * Tukuy Bridge — auto-generates Cacao handlers from Tukuy transformers
 *
 * Instead of duplicating Tukuy's transformers as Cacao handlers,
 * this bridge imports the Tukuy JS engine and wraps every registered
 * transformer into Cacao's `handler(signals, data)` pattern.
 *
 * Single source of truth: add a transformer to Tukuy, it appears here.
 *
 * Tukuy is an optional dependency — when not installed (e.g. CI),
 * the bridge exports an empty handler map and the build succeeds.
 */

import { tukuy } from 'tukuy';

/**
 * Build Cacao handlers from all registered Tukuy transformers.
 *
 * Each transformer becomes a handler named `tukuy_<name>`.
 * Input comes from `data.value`, options from `data.options`.
 * Output goes to the signal named `data.output || 'tukuy_out'`.
 */
function buildTransformHandlers() {
  if (!tukuy) return {};
  const handlers = {};

  for (const meta of tukuy.getMetadata()) {
    handlers[`tukuy_${meta.name}`] = async (signals, data) => {
      const input = data.value !== undefined ? data.value : '';
      const outputSignal = data.output || 'tukuy_out';

      try {
        const result = await tukuy.transform(meta.name, input, data.options || {});
        const formatted = (typeof result === 'object' && result !== null)
          ? JSON.stringify(result, null, 2)
          : String(result);
        signals.set(outputSignal, formatted);
      } catch (e) {
        signals.set(outputSignal, 'Error: ' + e.message);
      }
    };
  }

  return handlers;
}

/**
 * Chain handler — execute a Tukuy chain from a step array.
 *
 * Steps can be strings ("slugify") or objects ({name: "truncate", options: {length: 20}}).
 * Steps come from `data.steps` or the `tukuy_chain_steps` signal (JSON string).
 */
function buildChainHandler() {
  if (!tukuy) return {};
  return {
    tukuy_chain: async (signals, data) => {
      const input = data.value !== undefined ? data.value : '';
      const outputSignal = data.output || 'tukuy_out';

      let steps;
      if (data.steps) {
        steps = data.steps;
      } else {
        const raw = signals.get('tukuy_chain_steps');
        if (!raw) {
          signals.set(outputSignal, 'Error: No chain steps provided');
          return;
        }
        try { steps = JSON.parse(raw); }
        catch { signals.set(outputSignal, 'Error: Invalid chain steps JSON'); return; }
      }

      if (!Array.isArray(steps) || steps.length === 0) {
        signals.set(outputSignal, 'Error: Chain steps must be a non-empty array');
        return;
      }

      try {
        const { output } = await tukuy.chain(steps, input);
        const formatted = (typeof output === 'object' && output !== null)
          ? JSON.stringify(output, null, 2)
          : String(output);
        signals.set(outputSignal, formatted);
      } catch (e) {
        signals.set(outputSignal, 'Error: ' + e.message);
      }
    },
  };
}

/**
 * Browse handler — list available transformers (for discovery UIs).
 */
function buildBrowseHandlers() {
  if (!tukuy) return {};
  return {
    tukuy_browse: (signals) => {
      const byCategory = tukuy.getMetadataByCategory();
      const lines = [];
      for (const [cat, items] of Object.entries(byCategory)) {
        lines.push(`── ${cat} (${ items.length}) ──`);
        for (const item of items) {
          const paramStr = item.params.length > 0
            ? ` (${item.params.map(p => p.name).join(', ')})`
            : '';
          lines.push(`  ${item.name}${paramStr} — ${item.description}`);
        }
        lines.push('');
      }
      signals.set('tukuy_out', lines.join('\n'));
    },

    tukuy_list: (signals) => {
      signals.set('tukuy_out', JSON.stringify(tukuy.getMetadataByCategory(), null, 2));
    },
  };
}

// Build everything and export as a flat handler map
export const tukuyHandlers = {
  ...buildTransformHandlers(),
  ...buildChainHandler(),
  ...buildBrowseHandlers(),
};

// Also export the raw registry for advanced use
export { tukuy };
