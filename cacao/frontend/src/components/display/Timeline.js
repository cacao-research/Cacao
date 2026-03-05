/**
 * Timeline - Vertical timeline for changelogs, events, history
 */

const { createElement: h } = React;
import { renderComponent } from '../renderer.js';
import { getIcon } from '../core/icons.js';

export function Timeline({ props, children }) {
  const { items, alternate = false } = props;

  // If items prop provided, render simple timeline
  if (items && items.length) {
    return h('div', { className: 'c-timeline' + (alternate ? ' c-timeline--alternate' : '') },
      items.map((item, i) =>
        h('div', { key: i, className: 'c-timeline-item' }, [
          h('div', { key: 'line', className: 'c-timeline-line' },
            h('div', { className: 'c-timeline-dot' + (item.color ? ' c-timeline-dot--' + item.color : '') },
              item.icon ? getIcon(item.icon) : null
            )
          ),
          h('div', { key: 'content', className: 'c-timeline-content' }, [
            h('div', { key: 'header', className: 'c-timeline-header' }, [
              h('div', { key: 'title', className: 'c-timeline-title' }, item.title),
              item.date && h('div', { key: 'date', className: 'c-timeline-date' }, item.date),
            ]),
            item.description && h('div', { key: 'desc', className: 'c-timeline-description' }, item.description),
          ]),
        ])
      )
    );
  }

  // Context manager mode
  return h('div', { className: 'c-timeline' + (alternate ? ' c-timeline--alternate' : '') }, children);
}

export function TimelineItem({ props, children }) {
  const { title, description, date, icon, color } = props;

  return h('div', { className: 'c-timeline-item' }, [
    h('div', { key: 'line', className: 'c-timeline-line' },
      h('div', { className: 'c-timeline-dot' + (color ? ' c-timeline-dot--' + color : '') },
        icon ? getIcon(icon) : null
      )
    ),
    h('div', { key: 'content', className: 'c-timeline-content' }, [
      h('div', { key: 'header', className: 'c-timeline-header' }, [
        title && h('div', { key: 'title', className: 'c-timeline-title' }, title),
        date && h('div', { key: 'date', className: 'c-timeline-date' }, date),
      ]),
      description && h('div', { key: 'desc', className: 'c-timeline-description' }, description),
      children && children.length > 0 && h('div', { key: 'body', className: 'c-timeline-body' }, children),
    ]),
  ]);
}
