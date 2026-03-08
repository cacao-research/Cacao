/**
 * Cacao Built-in Handlers
 *
 * These handlers provide client-side logic for static builds.
 * They're automatically available - users just reference them by name.
 *
 * Tukuy transformers are bridged in automatically — every Tukuy
 * transformer is available as `tukuy_<name>` (e.g. tukuy_slugify).
 * Chains are available via `tukuy_chain`.
 */

import { encoders } from './encoders.js';
import { generators } from './generators.js';
import { converters } from './converters.js';
import { text } from './text.js';
import { crypto } from './crypto.js';
import { tukuyHandlers } from './tukuy-bridge.js';

// Combine all built-in handlers
export const builtinHandlers = {
  ...encoders,
  ...generators,
  ...converters,
  ...text,
  ...crypto,
  ...tukuyHandlers,
};

// Export for use in static runtime
export { builtinHandlers as handlers };
