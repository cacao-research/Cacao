---
name: cacao-handler
description: Add JavaScript handlers for Cacao static builds. Use when implementing client-side logic for events like encoding, generating, converting, or any operation that needs to work without a Python server.
---

# Cacao Handler Development

Handlers provide client-side JavaScript logic for static builds. When users run `cacao build`, their app works without a Python server because handlers execute in the browser.

## Architecture

```
Python: c.button("Encode", on_click="base64_encode")
                                        ↓
Static Build: Event fires → Handler executes → Signal updates → UI re-renders
```

## Handler Location

```
cacao/frontend/src/handlers/
├── index.js        # Exports all handlers
├── encoders.js     # base64, url, html, jwt
├── generators.js   # uuid, password, lorem
├── converters.js   # yaml, case, number base
├── text.js         # stats, regex
└── crypto.js       # hash, hmac
```

## Adding a New Handler

### 1. Choose or Create Category File

Pick existing file or create new one in `handlers/`:

```javascript
// handlers/my-category.js

export const myHandlers = {
  // handlers go here
};
```

### 2. Write the Handler

Handler signature: `(signals, data) => void`

```javascript
export const myHandlers = {
  // Simple handler - just updates a signal
  my_action: (signals, data) => {
    signals.set('output_signal', 'new value');
  },

  // Handler with input data
  process_input: (signals, data) => {
    const input = data.value || '';  // data comes from event
    const result = input.toUpperCase();
    signals.set('result', result);
  },

  // Handler that reads other signals
  compute_total: (signals, data) => {
    const a = signals.get('value_a') || 0;
    const b = signals.get('value_b') || 0;
    signals.set('total', a + b);
  },

  // Async handler (for crypto, fetch, etc.)
  async fetch_data: (signals, data) => {
    try {
      const response = await fetch(data.url);
      const json = await response.json();
      signals.set('api_result', JSON.stringify(json, null, 2));
    } catch (e) {
      signals.set('api_result', 'Error: ' + e.message);
    }
  },

  // Mode toggle pattern (common for encode/decode)
  set_encode_mode: (signals) => {
    signals.set('mode', 'encode');
  },

  set_decode_mode: (signals) => {
    signals.set('mode', 'decode');
  },

  process_with_mode: (signals, data) => {
    const text = data.value || '';
    const mode = signals.get('mode') || 'encode';

    if (mode === 'encode') {
      signals.set('output', encode(text));
    } else {
      signals.set('output', decode(text));
    }
  },
};
```

### 3. Export from index.js

```javascript
// handlers/index.js
import { encoders } from './encoders.js';
import { generators } from './generators.js';
import { myHandlers } from './my-category.js';  // Add import

export const builtinHandlers = {
  ...encoders,
  ...generators,
  ...myHandlers,  // Spread into exports
};

export { builtinHandlers as handlers };
```

### 4. Rebuild Frontend

```bash
cd cacao/frontend
npm run build
```

## Signals API

The `signals` object passed to handlers:

```javascript
// Get a signal value
const value = signals.get('signal_name');

// Set a signal value (triggers UI update)
signals.set('signal_name', newValue);

// Get all signals
const all = signals.getAll();
```

## Event Data

The `data` object contains what the component sent:

| Component | Event | Data |
|-----------|-------|------|
| `button` | `on_click` | `{}` |
| `input` | `on_change` | `{ value: "text" }` |
| `textarea` | `on_change` | `{ value: "text" }` |
| `select` | `on_change` | `{ value: "selected" }` |
| `slider` | `on_change` | `{ value: 50 }` |
| `checkbox` | `on_change` | `{ checked: true }` |

## Common Patterns

### Encoder/Decoder Pattern

```javascript
export const encoders = {
  // Mode toggles
  base64_encode: (signals) => signals.set('base64_mode', 'encode'),
  base64_decode: (signals) => signals.set('base64_mode', 'decode'),

  // Process based on mode
  base64_process: (signals, data) => {
    const text = data.value || '';
    const mode = signals.get('base64_mode') || 'encode';

    if (!text) {
      signals.set('base64_out', '');
      return;
    }

    try {
      if (mode === 'encode') {
        signals.set('base64_out', btoa(text));
      } else {
        signals.set('base64_out', atob(text));
      }
    } catch (e) {
      signals.set('base64_out', 'Error: ' + e.message);
    }
  },
};
```

### Generator Pattern

```javascript
export const generators = {
  gen_uuid: (signals) => {
    const uuid = crypto.randomUUID();
    signals.set('uuid_result', uuid);
  },

  gen_random: (signals) => {
    const length = signals.get('random_length') || 16;
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const array = new Uint32Array(length);
    crypto.getRandomValues(array);
    for (let i = 0; i < length; i++) {
      result += chars[array[i] % chars.length];
    }
    signals.set('random_result', result);
  },
};
```

### Validator Pattern

```javascript
export const validators = {
  validate_email: (signals, data) => {
    const email = data.value || '';
    const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    signals.set('email_valid', valid);
    signals.set('email_error', valid ? '' : 'Invalid email format');
  },

  validate_form: (signals) => {
    const name = signals.get('form_name') || '';
    const email = signals.get('form_email') || '';

    const errors = [];
    if (!name) errors.push('Name is required');
    if (!email) errors.push('Email is required');

    signals.set('form_errors', errors.join(', '));
    signals.set('form_valid', errors.length === 0);
  },
};
```

### Dependent Update Pattern

```javascript
// When one signal changes, update related signals
export const computed = {
  update_price: (signals, data) => {
    const quantity = parseInt(data.value) || 0;
    const unitPrice = signals.get('unit_price') || 10;
    const subtotal = quantity * unitPrice;
    const tax = subtotal * 0.1;

    signals.set('quantity', quantity);
    signals.set('subtotal', subtotal.toFixed(2));
    signals.set('tax', tax.toFixed(2));
    signals.set('total', (subtotal + tax).toFixed(2));
  },
};
```

## Browser APIs Available

```javascript
// Crypto
crypto.randomUUID()
crypto.getRandomValues(array)
crypto.subtle.digest('SHA-256', data)
crypto.subtle.importKey(...)
crypto.subtle.sign(...)

// Encoding
btoa(string)  // Base64 encode
atob(string)  // Base64 decode
encodeURIComponent(string)
decodeURIComponent(string)

// Text
new TextEncoder().encode(string)
new TextDecoder().decode(buffer)

// DOM (for HTML encoding)
document.createElement('div')
element.textContent = text  // Encode
element.innerHTML = html    // Decode
```

## Testing Handlers

```bash
# Build
cd cacao/frontend && npm run build

# Create test app
cat > /tmp/test.py << 'EOF'
import cacao as c

c.config(title="Handler Test")

output = c.signal("", name="output")

with c.card():
    c.textarea(label="Input", on_change="my_handler")
    c.code(output)
EOF

# Run
cacao run /tmp/test.py

# Or build static and test
cacao build /tmp/test.py
python -m http.server -d dist
```

## Checklist

- [ ] Handler function in category file
- [ ] Exported from `handlers/index.js`
- [ ] Signal names match Python signal names
- [ ] Error handling with try/catch
- [ ] `npm run build` succeeds
- [ ] Works in dynamic mode (`cacao run`)
- [ ] Works in static mode (`cacao build`)
