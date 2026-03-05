/**
 * Breadcrumb - Navigation breadcrumb trail
 */

const { createElement: h } = React;
import { getIcon } from '../core/icons.js';

export function Breadcrumb({ props }) {
  const { items = [], separator = '/' } = props;

  return h('nav', { className: 'c-breadcrumb', 'aria-label': 'Breadcrumb' },
    h('ol', { className: 'c-breadcrumb-list' },
      items.map((item, i) => {
        const isLast = i === items.length - 1;
        return h('li', { key: i, className: 'c-breadcrumb-item' + (isLast ? ' c-breadcrumb-item--active' : '') }, [
          i > 0 && h('span', { key: 'sep', className: 'c-breadcrumb-separator', 'aria-hidden': true }, separator),
          item.icon && h('span', { key: 'icon', className: 'c-breadcrumb-icon' }, getIcon(item.icon)),
          isLast
            ? h('span', { key: 'label', 'aria-current': 'page' }, item.label)
            : item.href
              ? h('a', { key: 'label', href: item.href, className: 'c-breadcrumb-link' }, item.label)
              : h('span', { key: 'label' }, item.label),
        ]);
      })
    )
  );
}
