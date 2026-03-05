const { createElement: h } = React;

export function Row({ props, children }) {
  const style = { gap: ((props.gap || 4) * 4) + 'px' };

  // Allow disabling wrap for fixed layouts (e.g. sidebar + content)
  if (props.wrap === false) {
    style.flexWrap = 'nowrap';
  }

  // Support explicit height
  if (props.height) {
    style.height = props.height;
  }

  // Justify content
  if (props.justify && props.justify !== 'start') {
    const justifyMap = {
      center: 'center',
      end: 'flex-end',
      between: 'space-between',
      around: 'space-around',
    };
    style.justifyContent = justifyMap[props.justify] || props.justify;
  }

  const classNames = ['c-row'];
  if (props.justify === 'between') classNames.push('justify-between');

  return h('div', {
    className: classNames.join(' '),
    style,
  }, children);
}
