/**
 * Theme Management for Cacao
 * Handles theme switching with localStorage persistence
 */

const STORAGE_KEY = 'cacao-theme';

export function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(STORAGE_KEY, theme);
}

export function getTheme() {
  return document.documentElement.getAttribute('data-theme') || 'dark';
}

export function initTheme() {
  // Only restore saved theme if the page doesn't specify one,
  // or if the saved theme belongs to the same theme family.
  // This prevents a tukuy session from overriding a dark/light app.
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) return;

  const serverTheme = document.documentElement.getAttribute('data-theme') || 'dark';
  const serverFamily = serverTheme.replace('-light', '');
  const savedFamily = saved.replace('-light', '');

  // Only apply saved theme if it's from the same family (e.g. dark/light or tukuy/tukuy-light)
  if (serverFamily === savedFamily) {
    setTheme(saved);
  }
}

export function toggleTheme() {
  const current = getTheme();
  const next = current === 'dark' ? 'light' : 'dark';
  setTheme(next);
  return next;
}
