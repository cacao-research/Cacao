/**
 * Stack - Vertical or horizontal stack with optional dividers
 */

const { createElement: h } = React;

export function Stack({ props, children }) {
  const { direction = 'vertical', gap = 4, divider = false, align, justify } = props;
  const isHorizontal = direction === 'horizontal';

  const style = {
    gap: divider ? '0px' : (gap * 4) + 'px',
  };

  if (align) {
    const alignMap = { start: 'flex-start', end: 'flex-end', center: 'center', stretch: 'stretch' };
    style.alignItems = alignMap[align] || align;
  }

  if (justify) {
    const justifyMap = { start: 'flex-start', end: 'flex-end', center: 'center', between: 'space-between', around: 'space-around' };
    style.justifyContent = justifyMap[justify] || justify;
  }

  const className = 'c-stack c-stack--' + direction + (divider ? ' c-stack--divider' : '');

  if (!divider) {
    return h('div', { className, style }, children);
  }

  // Insert dividers between children
  const items = [];
  children.forEach((child, i) => {
    if (i > 0) {
      items.push(h('div', {
        key: 'd' + i,
        className: 'c-stack-divider',
        style: isHorizontal
          ? { margin: '0 ' + (gap * 4) + 'px' }
          : { margin: (gap * 4) + 'px 0' },
      }));
    }
    items.push(child);
  });

  return h('div', { className, style }, items);
}
