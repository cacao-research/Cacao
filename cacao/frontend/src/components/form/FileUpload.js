/**
 * FileUpload - File upload component
 */

const { createElement: h, useRef } = React;

export function FileUpload({ props }) {
  const { label, accept, multiple = false, on_upload } = props;
  const inputRef = useRef(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleChange = (e) => {
    const files = Array.from(e.target.files || []);
    // Handle file upload event
    if (on_upload && files.length > 0) {
      // Would send to server via WebSocket
      console.log('Files selected:', files);
    }
  };

  return h('div', { className: 'c-upload-wrapper' }, [
    h('input', {
      ref: inputRef,
      type: 'file',
      accept,
      multiple,
      onChange: handleChange,
      style: { display: 'none' },
      key: 'input'
    }),
    h('button', {
      type: 'button',
      className: 'c-upload-button',
      onClick: handleClick,
      key: 'button'
    }, [
      h('span', { className: 'c-upload-icon', key: 'icon' }, '\u2191'),
      h('span', { key: 'label' }, label || 'Upload File')
    ])
  ]);
}
