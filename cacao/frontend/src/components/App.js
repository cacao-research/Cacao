/**
 * Main App component (was Dashboard)
 */

const { createElement: h, useState, useEffect } = React;
import { renderComponent } from './renderer.js';

export function App({ renderers }) {
  const [pages, setPages] = useState(null);
  const [currentPage, setCurrentPage] = useState('/');
  const [activeTab, setActiveTab] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/pages')
      .then(r => r.json())
      .then(data => setPages(data))
      .catch(e => setError(e.message));
  }, []);

  if (error) return h('div', { className: 'loading', style: { color: 'var(--danger)' } }, 'Error: ' + error);
  if (!pages) return h('div', { className: 'loading' }, 'Loading...');

  const pageData = pages.pages || {};
  const components = pageData[currentPage] || [];

  const sidebarIdx = components.findIndex(c => c.type === 'Sidebar');
  const sidebar = sidebarIdx >= 0 ? components[sidebarIdx] : null;
  const mainComponents = sidebarIdx >= 0 ? [...components.slice(0, sidebarIdx), ...components.slice(sidebarIdx + 1)] : components;

  const render = (comp, key) => renderComponent(comp, key, setActiveTab, activeTab, renderers);

  return h('div', { className: 'app-container' }, [
    h('div', { className: 'main-content', key: 'main' }, mainComponents.map((c, i) => render(c, i))),
    sidebar && h('div', { className: 'sidebar', key: 'sidebar' }, (sidebar.children || []).map((c, i) => render(c, i)))
  ]);
}
