/**
 * Keyboard Shortcut Registry
 * Manages global keyboard shortcuts for Cacao apps
 */

const shortcuts = {};

export function registerShortcut(combo, handler, description) {
  shortcuts[combo] = { handler, description };
}

export function unregisterShortcut(combo) {
  delete shortcuts[combo];
}

export function initShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Don't trigger shortcuts when typing in inputs
    const tag = e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') {
      // Allow mod+k even in inputs (command palette)
      const combo = buildCombo(e);
      if (combo !== 'mod+k') return;
    }

    const combo = buildCombo(e);
    if (shortcuts[combo]) {
      e.preventDefault();
      shortcuts[combo].handler();
    }
  });
}

function buildCombo(e) {
  const parts = [];
  if (e.metaKey || e.ctrlKey) parts.push('mod');
  if (e.shiftKey) parts.push('shift');
  if (e.altKey) parts.push('alt');
  parts.push(e.key.toLowerCase());
  return parts.join('+');
}

export function getShortcuts() {
  return Object.entries(shortcuts).map(([combo, { description }]) => ({
    combo, description
  }));
}
