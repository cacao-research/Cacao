/**
 * Converter Handlers
 */

export const converters = {
  // JSON to YAML
  convert_yaml: (signals, data) => {
    const text = (data.value || '').trim();

    if (!text) {
      signals.set('yaml_out', '');
      return;
    }

    const toYaml = (obj, indent = 0) => {
      const prefix = '  '.repeat(indent);
      const lines = [];

      if (Array.isArray(obj)) {
        obj.forEach(item => {
          if (typeof item === 'object' && item !== null) {
            lines.push(prefix + '-');
            lines.push(toYaml(item, indent + 1));
          } else {
            lines.push(prefix + '- ' + item);
          }
        });
      } else if (typeof obj === 'object' && obj !== null) {
        Object.entries(obj).forEach(([key, value]) => {
          if (typeof value === 'object' && value !== null) {
            lines.push(prefix + key + ':');
            lines.push(toYaml(value, indent + 1));
          } else {
            lines.push(prefix + key + ': ' + value);
          }
        });
      }

      return lines.join('\n');
    };

    try {
      const parsed = JSON.parse(text);
      signals.set('yaml_out', toYaml(parsed));
    } catch (e) {
      signals.set('yaml_out', 'Error: ' + e.message);
    }
  },

  // Case converter
  convert_case: (signals, data) => {
    const text = data.value || '';

    if (!text) {
      signals.set('case_out', '');
      return;
    }

    const words = text.replace(/-/g, ' ').replace(/_/g, ' ').split(/\s+/).filter(w => w);

    const results = [
      'lowercase:     ' + text.toLowerCase(),
      'UPPERCASE:     ' + text.toUpperCase(),
      'Title Case:    ' + text.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' '),
      'camelCase:     ' + (words.length ? words[0].toLowerCase() + words.slice(1).map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join('') : ''),
      'PascalCase:    ' + words.map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(''),
      'snake_case:    ' + words.map(w => w.toLowerCase()).join('_'),
      'kebab-case:    ' + words.map(w => w.toLowerCase()).join('-'),
      'CONSTANT_CASE: ' + words.map(w => w.toUpperCase()).join('_'),
    ];

    signals.set('case_out', results.join('\n'));
  },

  // Number base converter
  convert_base: (signals, data) => {
    const value = (data.value || '').trim();

    if (!value) {
      signals.set('base_out', '');
      return;
    }

    try {
      const num = parseInt(value, 10);
      if (isNaN(num)) {
        throw new Error('Invalid decimal number');
      }

      const results = [
        'Binary:      ' + num.toString(2),
        'Octal:       ' + num.toString(8),
        'Decimal:     ' + num.toString(10),
        'Hexadecimal: ' + num.toString(16).toUpperCase(),
      ];

      signals.set('base_out', results.join('\n'));
    } catch (e) {
      signals.set('base_out', 'Error: ' + e.message);
    }
  },
};
