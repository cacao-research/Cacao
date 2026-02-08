/**
 * NavGroup - Collapsible navigation group
 */

const { createElement: h, useState } = React;

// Simple icon mapping for common icons
const ICONS = {
  code: '\u2039\u203a',
  wrench: '\u2692',
  hash: '#',
  text: 'T',
  lock: '\u26bf',
  shuffle: '\u21c4',
  home: '\u2302',
  cog: '\u2699',
  folder: '\u2750',
  file: '\u2b1a',
  chevron: '\u276f',
};

function getIcon(iconName) {
  return ICONS[iconName] || iconName?.charAt(0)?.toUpperCase() || '\u25cf';
}

export function NavGroup({ props, children }) {
  const { label, icon, defaultOpen = true } = props;
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return h('div', { className: 'nav-group' + (isOpen ? ' open' : '') }, [
    h('button', {
      className: 'nav-group-header',
      key: 'header',
      onClick: () => setIsOpen(!isOpen),
      type: 'button'
    }, [
      icon && h('span', { className: 'nav-icon', key: 'icon' }, getIcon(icon)),
      h('span', { className: 'nav-group-label', key: 'label' }, label),
      h('span', { className: 'nav-group-chevron', key: 'chevron' }, isOpen ? '\u25bc' : '\u25b6')
    ]),
    isOpen && h('div', { className: 'nav-group-items', key: 'items' }, children)
  ]);
}
