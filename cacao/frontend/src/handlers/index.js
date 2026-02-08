/**
 * Cacao Built-in Handlers
 *
 * These handlers provide client-side logic for static builds.
 * They're automatically available - users just reference them by name.
 */

import { encoders } from './encoders.js';
import { generators } from './generators.js';
import { converters } from './converters.js';
import { text } from './text.js';
import { crypto } from './crypto.js';

// Combine all built-in handlers
export const builtinHandlers = {
  ...encoders,
  ...generators,
  ...converters,
  ...text,
  ...crypto,
};

// Export for use in static runtime
export { builtinHandlers as handlers };
