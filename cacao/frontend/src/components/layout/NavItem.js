/**
 * NavItem - Navigation item (link/button)
 */

const { createElement: h } = React;

// Simple icon mapping
const ICONS = {
  code: '\u2039\u203a',
  link: '\u26d3',
  html: '\u2039/\u203a',
  key: '\u26bf',
  hash: '#',
  dice: '\u2684',
  lock: '\u26bf',
  text: 'T',
  shuffle: '\u21c4',
  binary: '01',
  search: '\u26b2',
  regex: '.*',
  hash2: '#',
  shield: '\u26e8',
};

function getIcon(iconName) {
  return ICONS[iconName] || iconName?.charAt(0)?.toUpperCase() || '';
}

export function NavItem({ props, setActiveTab, activeTab }) {
  const { label, itemKey, icon, badge } = props;
  const isActive = activeTab === itemKey;

  return h('button', {
    className: 'nav-item' + (isActive ? ' active' : ''),
    onClick: () => setActiveTab(itemKey),
    type: 'button'
  }, [
    icon && h('span', { className: 'nav-icon', key: 'icon' }, getIcon(icon)),
    h('span', { className: 'nav-item-label', key: 'label' }, label),
    badge && h('span', { className: 'nav-item-badge', key: 'badge' }, badge)
  ]);
}
