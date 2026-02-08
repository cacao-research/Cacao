/**
 * DatePicker - Date selection component
 */

const { createElement: h, useState } = React;

export function DatePicker({ props }) {
  const { label, placeholder = 'Select date', disabled = false, signal } = props;
  const [value, setValue] = useState('');

  const handleChange = (e) => {
    setValue(e.target.value);
  };

  return h('div', { className: 'c-datepicker-wrapper' }, [
    label && h('label', { className: 'c-datepicker-label', key: 'label' }, label),
    h('input', {
      type: 'date',
      className: 'c-datepicker',
      placeholder,
      disabled,
      value,
      onChange: handleChange,
      key: 'input'
    })
  ]);
}
