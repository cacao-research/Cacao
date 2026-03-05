const { createElement: h } = React;

export function Col({ props, children }) {
  const style = { gap: ((props.gap || 4) * 4) + 'px' };

  // Fixed width support (e.g. sidebar)
  if (props.width) {
    style.flex = '0 0 ' + props.width;
    style.width = props.width;
    style.minWidth = 0;
  }

  // Custom flex value (e.g. for split layouts)
  if (props.flex) {
    style.flex = props.flex;
  }

  // Max width (e.g. for centered layouts)
  if (props.max_width) {
    style.maxWidth = props.max_width;
  }

  // Height (e.g. for dashboard layouts)
  if (props.height) {
    style.height = props.height;
  }

  // Align items (cross-axis)
  if (props.align && props.align !== 'stretch') {
    style.alignItems = props.align === 'start' ? 'flex-start' :
                       props.align === 'end' ? 'flex-end' : props.align;
  }

  return h('div', {
    className: 'c-col' + (props.span ? ' col-span-' + props.span : ''),
    style,
  }, children);
}
