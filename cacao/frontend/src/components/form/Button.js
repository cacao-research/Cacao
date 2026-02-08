/**
 * Button component with event handling
 */

const { createElement: h } = React;
import { cacaoWs } from '../core/websocket.js';

export function Button({ props, setActiveTab }) {
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
      // Handle navigation action (nav:tabKey)
      if (typeof eventName === 'string' && eventName.startsWith('nav:')) {
        const tabKey = eventName.slice(4); // Remove 'nav:' prefix
        if (setActiveTab) {
          setActiveTab(tabKey);
        }
        return;
      }

      // Handle external link action (link:url)
      if (typeof eventName === 'string' && eventName.startsWith('link:')) {
        const url = eventName.slice(5); // Remove 'link:' prefix
        window.open(url, '_blank', 'noopener,noreferrer');
        return;
      }

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
