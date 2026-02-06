/**
 * Utility functions for component rendering
 */

/**
 * Format a value for display
 * @param {*} v - Value to format
 * @returns {string} Formatted value
 */
export function formatValue(v) {
  if (v === null || v === undefined) return '-';
  if (typeof v === 'number') return v.toLocaleString();
  return String(v);
}
