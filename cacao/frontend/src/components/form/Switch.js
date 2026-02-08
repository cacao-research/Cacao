/**
 * Switch - Toggle switch component
 */

const { createElement: h, useState } = React;

export function Switch({ props }) {
  const { label, disabled = false, signal } = props;
  const [checked, setChecked] = useState(false);

  const handleChange = () => {
    if (!disabled) {
      setChecked(!checked);
    }
  };

  return h('label', { className: 'c-switch-wrapper' }, [
    h('span', { className: 'c-switch-label', key: 'label' }, label),
    h('button', {
      type: 'button',
      className: `c-switch ${checked ? 'active' : ''}`,
      disabled,
      onClick: handleChange,
      role: 'switch',
      'aria-checked': checked,
      key: 'switch'
    },
      h('span', { className: 'c-switch-thumb' })
    )
  ]);
}
