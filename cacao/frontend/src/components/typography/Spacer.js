const { createElement: h } = React;

export function Spacer({ props }) {
  return h('div', { style: { height: (props.size || 4) * 4 } });
}
