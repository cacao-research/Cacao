const { createElement: h } = React;

export function Tabs({ props, children, setActiveTab, activeTab }) {
  const tabs = children.filter(c => c && c.props && c.props.type === 'Tab');
  const current = activeTab || props.default || (tabs[0]?.props?.props?.tabKey);

  return h('div', null, [
    h('div', { className: 'tabs', key: 'tabs' }, tabs.map(t =>
      h('div', {
        className: 'tab ' + (t.props.props.tabKey === current ? 'active' : ''),
        key: t.props.props.tabKey,
        onClick: () => setActiveTab(t.props.props.tabKey)
      }, t.props.props.label)
    )),
    tabs.find(t => t.props.props.tabKey === current)
  ]);
}

export function Tab({ props, children }) {
  return h('div', null, children);
}
