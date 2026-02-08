/**
 * Crypto/Hashing Handlers
 */

// Helper for HMAC computation
async function computeHmac(signals) {
  const msg = signals.get('hmac_msg') || '';
  const key = signals.get('hmac_key') || '';

  if (!msg || !key) {
    signals.set('hmac_out', 'Enter message and key');
    return;
  }

  try {
    const encoder = new TextEncoder();
    const keyData = encoder.encode(key);
    const msgData = encoder.encode(msg);

    const cryptoKey = await window.crypto.subtle.importKey(
      'raw',
      keyData,
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign']
    );

    const signature = await window.crypto.subtle.sign('HMAC', cryptoKey, msgData);
    const hmac = Array.from(new Uint8Array(signature))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');

    signals.set('hmac_out', 'HMAC-SHA256:\n' + hmac);
  } catch (e) {
    signals.set('hmac_out', 'Error: ' + e.message);
  }
}

export const crypto = {
  // Hash generator
  compute_hash: async (signals, data) => {
    const text = data.value || '';

    if (!text) {
      signals.set('hash_out', '');
      return;
    }

    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(text);

    try {
      const sha256Buffer = await window.crypto.subtle.digest('SHA-256', dataBuffer);
      const sha256 = Array.from(new Uint8Array(sha256Buffer))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');

      const sha1Buffer = await window.crypto.subtle.digest('SHA-1', dataBuffer);
      const sha1 = Array.from(new Uint8Array(sha1Buffer))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');

      const sha512Buffer = await window.crypto.subtle.digest('SHA-512', dataBuffer);
      const sha512 = Array.from(new Uint8Array(sha512Buffer))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');

      const results = [
        'MD5:     (not available in browser)',
        'SHA-1:   ' + sha1,
        'SHA-256: ' + sha256,
        'SHA-512: ' + sha512,
      ];

      signals.set('hash_out', results.join('\n'));
    } catch (e) {
      signals.set('hash_out', 'Error: ' + e.message);
    }
  },

  // HMAC
  set_hmac_msg: (signals, data) => {
    signals.set('hmac_msg', data.value || '');
    computeHmac(signals);
  },

  set_hmac_key: (signals, data) => {
    signals.set('hmac_key', data.value || '');
    computeHmac(signals);
  },
};
