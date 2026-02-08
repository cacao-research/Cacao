/**
 * Button component with event handling
 */

const { createElement: h } = React;
import { cacaoWs } from '../core/websocket.js';

export function Button({ props }) {
  const {
    label,
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    icon,
    on_click,
  } = props;

  const handleClick = () => {
    if (disabled || loading) return;

    // Get the event name from on_click prop
    const eventName = on_click?.__event__ || on_click;

    if (eventName) {
      cacaoWs.sendEvent(eventName, {});
    }
  };

  const className = `btn btn-${variant} btn-${size}${disabled ? ' disabled' : ''}${loading ? ' loading' : ''}`;

  return h('button', {
    className,
    onClick: handleClick,
    disabled: disabled || loading,
    type: 'button'
  }, [
    icon && h('span', { className: 'btn-icon', key: 'icon' }, icon),
    h('span', { key: 'label' }, label)
  ]);
}
