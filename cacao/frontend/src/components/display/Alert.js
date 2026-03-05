const { createElement: h, useState } = React;

export function Alert({ props }) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return h('div', { className: 'alert alert-' + (props.type || 'info'), role: 'alert' }, [
    props.title && h('strong', { key: 'title' }, props.title + ': '),
    h('span', { key: 'msg' }, props.message),
    props.closable && h('button', {
      key: 'close',
      className: 'alert-close',
      onClick: () => setDismissed(true),
      'aria-label': 'Dismiss alert'
    }, '\u00d7')
  ]);
}
