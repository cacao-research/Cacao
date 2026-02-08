/**
 * Text Utility Handlers
 */

// Helper for regex testing
function testRegex(signals) {
  const pattern = signals.get('regex_pattern') || '';
  const text = signals.get('regex_text') || '';

  if (!pattern || !text) {
    signals.set('regex_out', 'Enter a pattern and test text');
    return;
  }

  try {
    const regex = new RegExp(pattern, 'g');
    const matches = [...text.matchAll(regex)];

    if (matches.length === 0) {
      signals.set('regex_out', 'No matches found');
      return;
    }

    const lines = [`Found ${matches.length} match(es):`, ''];
    matches.forEach((m, i) => {
      lines.push(`Match ${i + 1}: "${m[0]}"`);
      lines.push(`  Position: ${m.index}-${m.index + m[0].length}`);
      if (m.length > 1) {
        for (let j = 1; j < m.length; j++) {
          lines.push(`  Group ${j}: "${m[j]}"`);
        }
      }
      lines.push('');
    });

    signals.set('regex_out', lines.join('\n'));
  } catch (e) {
    signals.set('regex_out', 'Invalid regex: ' + e.message);
  }
}

export const text = {
  // Text statistics
  analyze_text: (signals, data) => {
    const text = data.value || '';

    if (!text) {
      signals.set('stats_out', '');
      return;
    }

    const chars = text.length;
    const charsNoSpaces = text.replace(/\s/g, '').length;
    const words = text.split(/\s+/).filter(w => w.length > 0).length;
    const lines = text.split('\n').length;
    const sentences = Math.max(0, text.split(/[.!?]+/).filter(s => s.trim().length > 0).length);
    const avgWord = words > 0 ? (charsNoSpaces / words).toFixed(2) : 0;
    const readingTime = Math.max(1, Math.floor(words / 200));

    const output = `Characters:           ${chars.toLocaleString()}
Characters (no space): ${charsNoSpaces.toLocaleString()}
Words:                ${words.toLocaleString()}
Lines:                ${lines.toLocaleString()}
Sentences:            ${sentences.toLocaleString()}
Avg word length:      ${avgWord}
Reading time:         ~${readingTime} min`;

    signals.set('stats_out', output);
  },

  // Regex tester
  set_regex_pattern: (signals, data) => {
    signals.set('regex_pattern', data.value || '');
    testRegex(signals);
  },

  set_regex_text: (signals, data) => {
    signals.set('regex_text', data.value || '');
    testRegex(signals);
  },
};
