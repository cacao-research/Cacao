/**
 * NavItem - Navigation item (link/button)
 */

const { createElement: h } = React;
import { getIcon } from '../core/icons.js';

export function NavItem({ props, setActiveTab, activeTab }) {
  const { label, itemKey, icon, badge } = props;
  const isActive = activeTab === itemKey;

  return h('button', {
    className: 'nav-item' + (isActive ? ' active' : ''),
    onClick: () => setActiveTab(itemKey),
    type: 'button',
    role: 'menuitem',
    'aria-current': isActive ? 'page' : undefined,
  }, [
    icon && h('span', { className: 'nav-icon', key: 'icon', 'aria-hidden': 'true' }, getIcon(icon)),
    h('span', { className: 'nav-item-label', key: 'label' }, label),
    badge && h('span', { className: 'nav-item-badge', key: 'badge' }, badge)
  ]);
}
