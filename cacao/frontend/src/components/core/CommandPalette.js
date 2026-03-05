/**
 * Command Palette (Cmd+K)
 * Fuzzy-search overlay for navigating pages and running commands
 */

const { createElement: h, useState, useEffect, useRef, useCallback } = React;
import { registerShortcut } from './shortcuts.js';
import { getShortcuts } from './shortcuts.js';
import { toggleTheme, getTheme } from './ThemeToggle.js';

// Global state for the command palette
let _setOpen = null;
let _commands = [];

export function openCommandPalette() {
  if (_setOpen) _setOpen(true);
}

export function closeCommandPalette() {
  if (_setOpen) _setOpen(false);
}

export function registerCommand(id, label, handler, options = {}) {
  // Remove existing command with same id
  _commands = _commands.filter(c => c.id !== id);
  _commands.push({ id, label, handler, shortcut: options.shortcut || null, icon: options.icon || null });
}

// Register default commands
registerCommand('theme-toggle', 'Toggle Theme (Dark/Light)', () => {
  toggleTheme();
}, { shortcut: 'mod+shift+t' });

// Initialize Cmd+K shortcut
registerShortcut('mod+k', () => openCommandPalette(), 'Open command palette');
registerShortcut('mod+shift+t', () => toggleTheme(), 'Toggle theme');

function fuzzyMatch(query, text) {
  if (!query) return true;
  const q = query.toLowerCase();
  const t = text.toLowerCase();
  // Simple substring match
  return t.includes(q);
}

export function CommandPalette({ setActiveTab, pages }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef(null);
  const resultsRef = useRef(null);

  // Expose setOpen globally
  useEffect(() => {
    _setOpen = setOpen;
    return () => { _setOpen = null; };
  }, []);

  // Focus input when opened
  useEffect(() => {
    if (open) {
      setQuery('');
      setActiveIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [open]);

  // Focus trap + close on Escape
  useEffect(() => {
    if (!open) return;
    const handleKey = (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        setOpen(false);
        return;
      }
      // Focus trap: keep Tab within the palette
      if (e.key === 'Tab') {
        // Only the input is focusable inside the palette, so prevent Tab from leaving
        e.preventDefault();
      }
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [open]);

  // Build filtered results
  const allItems = useCallback(() => {
    const items = [];

    // Add page navigation commands
    if (pages) {
      const pageKeys = Object.keys(pages);
      pageKeys.forEach(key => {
        if (key === '/') return; // Skip root
        items.push({
          id: 'page:' + key,
          label: 'Go to ' + key,
          handler: () => {
            if (setActiveTab) setActiveTab(key);
          },
          icon: null,
          shortcut: null,
        });
      });
    }

    // Add registered commands
    items.push(..._commands);

    // Add registered shortcuts as commands
    const registeredShortcuts = getShortcuts();
    registeredShortcuts.forEach(({ combo, description }) => {
      // Avoid duplicates with already-registered commands
      if (!items.find(i => i.shortcut === combo)) {
        items.push({
          id: 'shortcut:' + combo,
          label: description,
          handler: null,
          icon: null,
          shortcut: combo,
        });
      }
    });

    return items;
  }, [pages, setActiveTab]);

  const filtered = allItems().filter(item => fuzzyMatch(query, item.label));

  // Clamp active index
  useEffect(() => {
    if (activeIndex >= filtered.length) {
      setActiveIndex(Math.max(0, filtered.length - 1));
    }
  }, [filtered.length, activeIndex]);

  // Scroll active item into view
  useEffect(() => {
    if (!resultsRef.current) return;
    const active = resultsRef.current.children[activeIndex];
    if (active) active.scrollIntoView({ block: 'nearest' });
  }, [activeIndex]);

  const handleKeyDown = useCallback((e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex(i => Math.min(i + 1, filtered.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (filtered[activeIndex]?.handler) {
          filtered[activeIndex].handler();
          setOpen(false);
        }
        break;
    }
  }, [filtered, activeIndex]);

  const handleSelect = useCallback((item) => {
    if (item.handler) {
      item.handler();
      setOpen(false);
    }
  }, []);

  if (!open) return null;

  return h('div', {
    className: 'cmd-palette-overlay',
    role: 'dialog',
    'aria-modal': 'true',
    'aria-label': 'Command palette',
    onClick: (e) => { if (e.target === e.currentTarget) setOpen(false); }
  },
    h('div', { className: 'cmd-palette' }, [
      h('input', {
        key: 'input',
        ref: inputRef,
        className: 'cmd-palette-input',
        placeholder: 'Search commands...',
        value: query,
        onChange: (e) => { setQuery(e.target.value); setActiveIndex(0); },
        onKeyDown: handleKeyDown,
        role: 'combobox',
        'aria-expanded': 'true',
        'aria-controls': 'cmd-palette-listbox',
        'aria-activedescendant': filtered[activeIndex] ? 'cmd-item-' + activeIndex : undefined,
        'aria-autocomplete': 'list',
      }),
      h('div', {
        key: 'results',
        className: 'cmd-palette-results',
        ref: resultsRef,
        id: 'cmd-palette-listbox',
        role: 'listbox',
      },
        filtered.length > 0
          ? filtered.map((item, i) =>
              h('div', {
                key: item.id,
                id: 'cmd-item-' + i,
                className: 'cmd-palette-item' + (i === activeIndex ? ' active' : ''),
                role: 'option',
                'aria-selected': i === activeIndex,
                onClick: () => handleSelect(item),
                onMouseEnter: () => setActiveIndex(i),
              }, [
                h('span', { key: 'label' }, item.label),
                item.shortcut && h('span', { key: 'shortcut', className: 'cmd-palette-shortcut' },
                  formatShortcut(item.shortcut)
                ),
              ])
            )
          : h('div', { className: 'cmd-palette-item', role: 'option' }, 'No results found')
      ),
    ])
  );
}

function formatShortcut(combo) {
  const isMac = navigator.platform.indexOf('Mac') !== -1;
  return combo
    .replace('mod', isMac ? '\u2318' : 'Ctrl')
    .replace('shift', isMac ? '\u21E7' : 'Shift')
    .replace('alt', isMac ? '\u2325' : 'Alt')
    .replace(/\+/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}
