const { createElement: h, useRef, useState } = React;

export function Tabs({ props, children }) {
  const tabs = children.filter(c => c && c.props && c.props.type === 'Tab');
  const defaultTab = props.default || (tabs[0]?.props?.props?.tabKey);
  const [localTab, setLocalTab] = useState(defaultTab);
  const current = localTab || defaultTab;
  const tabListRef = useRef(null);

  const handleKeyDown = (e) => {
    const tabKeys = tabs.map(t => t.props.props.tabKey);
    const currentIdx = tabKeys.indexOf(current);
    let nextIdx;

    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      nextIdx = (currentIdx + 1) % tabKeys.length;
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      nextIdx = (currentIdx - 1 + tabKeys.length) % tabKeys.length;
    } else if (e.key === 'Home') {
      e.preventDefault();
      nextIdx = 0;
    } else if (e.key === 'End') {
      e.preventDefault();
      nextIdx = tabKeys.length - 1;
    } else {
      return;
    }

    setLocalTab(tabKeys[nextIdx]);
    if (tabListRef.current) {
      const buttons = tabListRef.current.querySelectorAll('[role="tab"]');
      if (buttons[nextIdx]) buttons[nextIdx].focus();
    }
  };

  return h('div', null, [
    h('div', { className: 'tabs', key: 'tabs', role: 'tablist', ref: tabListRef }, tabs.map(t =>
      h('button', {
        className: 'tab ' + (t.props.props.tabKey === current ? 'active' : ''),
        key: t.props.props.tabKey,
        role: 'tab',
        'aria-selected': t.props.props.tabKey === current,
        tabIndex: t.props.props.tabKey === current ? 0 : -1,
        onClick: () => setLocalTab(t.props.props.tabKey),
        onKeyDown: handleKeyDown
      }, t.props.props.label)
    )),
    h('div', { key: 'content', className: 'tab-content', role: 'tabpanel' },
      tabs.find(t => t.props.props.tabKey === current)
    )
  ]);
}

export function Tab({ props, children }) {
  return h('div', null, children);
}
