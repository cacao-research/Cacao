/**
 * Encoder/Decoder Handlers
 */

export const encoders = {
  // Base64
  base64_encode: (signals) => {
    signals.set('base64_mode', 'encode');
  },

  base64_decode: (signals) => {
    signals.set('base64_mode', 'decode');
  },

  base64_process: (signals, data) => {
    const text = data.value || '';
    const mode = signals.get('base64_mode') || 'encode';

    if (!text) {
      signals.set('base64_out', '');
      return;
    }

    try {
      if (mode === 'encode') {
        signals.set('base64_out', btoa(unescape(encodeURIComponent(text))));
      } else {
        signals.set('base64_out', decodeURIComponent(escape(atob(text))));
      }
    } catch (e) {
      signals.set('base64_out', 'Error: ' + e.message);
    }
  },

  // URL encoding
  url_encode: (signals) => {
    signals.set('url_mode', 'encode');
  },

  url_decode: (signals) => {
    signals.set('url_mode', 'decode');
  },

  url_process: (signals, data) => {
    const text = data.value || '';
    const mode = signals.get('url_mode') || 'encode';

    if (!text) {
      signals.set('url_out', '');
      return;
    }

    try {
      if (mode === 'encode') {
        signals.set('url_out', encodeURIComponent(text));
      } else {
        signals.set('url_out', decodeURIComponent(text));
      }
    } catch (e) {
      signals.set('url_out', 'Error: ' + e.message);
    }
  },

  // HTML entities
  html_encode: (signals) => {
    signals.set('html_mode', 'encode');
  },

  html_decode: (signals) => {
    signals.set('html_mode', 'decode');
  },

  html_process: (signals, data) => {
    const text = data.value || '';
    const mode = signals.get('html_mode') || 'encode';

    if (!text) {
      signals.set('html_out', '');
      return;
    }

    try {
      if (mode === 'encode') {
        const div = document.createElement('div');
        div.textContent = text;
        signals.set('html_out', div.innerHTML);
      } else {
        const div = document.createElement('div');
        div.innerHTML = text;
        signals.set('html_out', div.textContent);
      }
    } catch (e) {
      signals.set('html_out', 'Error: ' + e.message);
    }
  },

  // JWT decoder
  jwt_decode: (signals, data) => {
    const token = (data.value || '').trim();

    if (!token) {
      signals.set('jwt_header', '{}');
      signals.set('jwt_payload', '{}');
      return;
    }

    try {
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid JWT format - expected 3 parts');
      }

      const header = JSON.parse(atob(parts[0].replace(/-/g, '+').replace(/_/g, '/')));
      signals.set('jwt_header', JSON.stringify(header, null, 2));

      const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
      signals.set('jwt_payload', JSON.stringify(payload, null, 2));
    } catch (e) {
      signals.set('jwt_header', 'Error: ' + e.message);
      signals.set('jwt_payload', '');
    }
  },
};
