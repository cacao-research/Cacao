/**
 * AppShell - Admin-style layout with sidebar navigation
 */

const { createElement: h, useEffect } = React;

export function AppShell({ props, children, setActiveTab, activeTab }) {
  const { brand, logo } = props;

  // Set default active tab on mount if not already set
  useEffect(() => {
    if (activeTab === null && props.default) {
      setActiveTab(props.default);
    }
  }, []);

  // Find NavSidebar and ShellContent children
  const navSidebar = children.find(c => c?.props?.type === 'NavSidebar');
  const shellContent = children.find(c => c?.props?.type === 'ShellContent');
  const otherChildren = children.filter(c =>
    c?.props?.type !== 'NavSidebar' && c?.props?.type !== 'ShellContent'
  );

  return h('div', { className: 'app-shell' }, [
    // Left sidebar navigation
    h('aside', { className: 'app-shell-nav', key: 'nav' }, [
      // Brand header
      (brand || logo) && h('div', { className: 'app-shell-brand', key: 'brand' }, [
        logo && h('img', { src: logo, alt: brand || 'Logo', className: 'app-shell-logo', key: 'logo' }),
        brand && h('span', { className: 'app-shell-brand-text', key: 'brand-text' }, brand)
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
