/**
 * NavGroup - Collapsible navigation group
 */

const { createElement: h, useState } = React;
import { getIcon } from '../core/icons.js';

export function NavGroup({ props, children }) {
  const { label, icon, defaultOpen = true } = props;
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const groupId = 'nav-group-' + label.toLowerCase().replace(/\s+/g, '-');

  return h('div', { className: 'nav-group' + (isOpen ? ' open' : ''), role: 'group', 'aria-label': label }, [
    h('button', {
      className: 'nav-group-header',
      key: 'header',
      onClick: () => setIsOpen(!isOpen),
      type: 'button',
      'aria-expanded': isOpen,
      'aria-controls': groupId,
    }, [
      icon && h('span', { className: 'nav-icon', key: 'icon', 'aria-hidden': 'true' }, getIcon(icon)),
      h('span', { className: 'nav-group-label', key: 'label' }, label),
      h('span', { className: 'nav-group-chevron', key: 'chevron', 'aria-hidden': 'true' },
        getIcon(isOpen ? 'chevron-down' : 'chevron-right'))
    ]),
    h('div', {
      className: 'nav-group-items',
      key: 'items',
      id: groupId,
      role: 'menu',
    }, children)
  ]);
}
