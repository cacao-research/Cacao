/**
 * Tooltip - Hover/focus tooltip wrapper
 */

const { createElement: h, useState, useRef } = React;

export function Tooltip({ props, children }) {
  const { text, position = 'top', delay = 200 } = props;
  const [show, setShow] = useState(false);
  const timeoutRef = useRef(null);

  const handleEnter = () => {
    timeoutRef.current = setTimeout(() => setShow(true), delay);
  };

  const handleLeave = () => {
    clearTimeout(timeoutRef.current);
    setShow(false);
  };

  return h('div', {
    className: 'c-tooltip-wrapper',
    onMouseEnter: handleEnter,
    onMouseLeave: handleLeave,
    onFocus: handleEnter,
    onBlur: handleLeave,
  }, [
    ...children,
    show && h('div', {
      key: 'tip',
      className: 'c-tooltip c-tooltip--' + position,
      role: 'tooltip',
    }, text),
  ]);
}
