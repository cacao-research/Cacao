/**
 * LinkCard - Clickable navigation card
 */

const { createElement: h } = React;
import { getIcon } from '../core/icons.js';

export function LinkCard({ props }) {
  const { title, description, href, icon } = props;

  const content = [
    h('div', { key: 'body', className: 'c-link-card-body' }, [
      icon && h('span', { key: 'icon', className: 'c-link-card-icon' }, getIcon(icon)),
      h('div', { key: 'text', className: 'c-link-card-text' }, [
        h('div', { key: 'title', className: 'c-link-card-title' }, title),
        description && h('div', { key: 'desc', className: 'c-link-card-description' }, description),
      ]),
    ]),
    h('span', { key: 'arrow', className: 'c-link-card-arrow' }, '\u2192'),
  ];

  if (href) {
    return h('a', { className: 'c-link-card', href }, content);
  }
  return h('div', { className: 'c-link-card' }, content);
}
