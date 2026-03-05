/**
 * AppShell - Admin-style layout with sidebar navigation
 */

const { createElement: h, useEffect, useState, useCallback } = React;
import { getIcon } from '../core/icons.js';

export function AppShell({ props, children, setActiveTab, activeTab }) {
  const { brand, logo, themeDark, themeLight } = props;
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isDark, setIsDark] = useState(() => {
    const current = document.documentElement.getAttribute('data-theme') || '';
    // If themeLight is provided, check if current theme is NOT the light one
    if (themeLight) return current !== themeLight;
    return current === 'dark' || current.indexOf('light') === -1;
  });

  // Set default active tab on mount if not already set
  useEffect(() => {
    if (activeTab === null && props.default) {
      setActiveTab(props.default);
    }
  }, []);

  // Close mobile sidebar when navigation changes
  useEffect(() => {
    setSidebarOpen(false);
  }, [activeTab]);

  // Theme toggle handler
  const toggleTheme = useCallback(() => {
    if (!themeDark || !themeLight) return;
    const next = isDark ? themeLight : themeDark;
    if (window.Cacao?.setTheme) {
      window.Cacao.setTheme(next);
    }
    setIsDark(!isDark);
  }, [isDark, themeDark, themeLight]);

  // Find NavSidebar and ShellContent children
  const navSidebar = children.find(c => c?.props?.type === 'NavSidebar');
  const shellContent = children.find(c => c?.props?.type === 'ShellContent');
  const otherChildren = children.filter(c =>
    c?.props?.type !== 'NavSidebar' && c?.props?.type !== 'ShellContent'
  );

  const hasThemeToggle = themeDark && themeLight;

  return h('div', { className: 'app-shell' }, [
    // Hamburger button (visible on mobile only via CSS)
    h('button', {
      key: 'hamburger',
      className: 'app-shell-hamburger',
      onClick: () => setSidebarOpen(!sidebarOpen),
      'aria-label': sidebarOpen ? 'Close menu' : 'Open menu'
    }, sidebarOpen ? '\u2715' : '\u2630'),
    // Backdrop overlay (mobile only)
    h('div', {
      key: 'backdrop',
      className: 'app-shell-backdrop' + (sidebarOpen ? ' open' : ''),
      onClick: () => setSidebarOpen(false)
    }),
    // Left sidebar navigation
    h('aside', { className: 'app-shell-nav' + (sidebarOpen ? ' open' : ''), key: 'nav' }, [
      // Brand header
      (brand || logo || hasThemeToggle) && h('div', { className: 'app-shell-brand', key: 'brand' }, [
        logo && h('img', { src: logo, alt: brand || 'Logo', className: 'app-shell-logo', key: 'logo' }),
        brand && h('span', { className: 'app-shell-brand-text', key: 'brand-text' }, brand),
        // Theme toggle button in the brand bar
        hasThemeToggle && h('button', {
          key: 'theme-toggle',
          className: 'app-shell-theme-toggle',
          onClick: toggleTheme,
          'aria-label': isDark ? 'Switch to light mode' : 'Switch to dark mode',
          title: isDark ? 'Light mode' : 'Dark mode',
        }, getIcon(isDark ? 'sun' : 'moon'))
      ]),
      // Navigation content
      navSidebar
    ]),
    // Main content area
    h('main', { className: 'app-shell-content', key: 'content' }, [
      shellContent,
      ...otherChildren
    ])
  ]);
}
