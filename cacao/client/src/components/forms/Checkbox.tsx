import { CSSProperties, forwardRef, InputHTMLAttributes } from 'react'

export interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type' | 'size'> {
  label?: string
  description?: string
  error?: string
  inputSize?: 'sm' | 'md' | 'lg'
}

const sizeMap = {
  sm: { box: 16, check: 10, fontSize: '14px' },
  md: { box: 20, check: 12, fontSize: '16px' },
  lg: { box: 24, check: 14, fontSize: '18px' },
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, description, error, inputSize = 'md', disabled, className, style, checked, ...rest }, ref) => {
    const sizes = sizeMap[inputSize]
    const hasError = Boolean(error)

    const containerStyle: CSSProperties = {
      display: 'flex',
      alignItems: 'flex-start',
      gap: '10px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      ...style,
    }

    const checkboxWrapperStyle: CSSProperties = {
      position: 'relative',
      width: sizes.box,
      height: sizes.box,
      flexShrink: 0,
    }

    const inputStyle: CSSProperties = {
      position: 'absolute',
      opacity: 0,
      width: '100%',
      height: '100%',
      cursor: disabled ? 'not-allowed' : 'pointer',
      margin: 0,
    }

    const customCheckboxStyle: CSSProperties = {
      width: sizes.box,
      height: sizes.box,
      borderRadius: '4px',
      border: `2px solid ${hasError ? '#ef4444' : checked ? '#7c3aed' : 'rgba(255, 255, 255, 0.3)'}`,
      backgroundColor: checked ? '#7c3aed' : 'transparent',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'all 0.2s',
    }

    const labelContainerStyle: CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      gap: '2px',
    }

    const labelStyle: CSSProperties = {
      fontSize: sizes.fontSize,
      color: '#ffffff',
      fontWeight: 500,
    }

    const descriptionStyle: CSSProperties = {
      fontSize: '12px',
      color: 'rgba(255, 255, 255, 0.5)',
    }

    const errorStyle: CSSProperties = {
      fontSize: '12px',
      color: '#ef4444',
      marginTop: '4px',
    }

    return (
      <div className={className}>
        <label style={containerStyle}>
          <div style={checkboxWrapperStyle}>
            <input ref={ref} type="checkbox" disabled={disabled} checked={checked} style={inputStyle} {...rest} />
            <div style={customCheckboxStyle}>
              {checked && (
                <svg
                  width={sizes.check}
                  height={sizes.check}
                  viewBox="0 0 12 12"
                  fill="none"
                  stroke="#ffffff"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M2 6l3 3 5-6" />
                </svg>
              )}
            </div>
          </div>
          {(label || description) && (
            <div style={labelContainerStyle}>
              {label && <span style={labelStyle}>{label}</span>}
              {description && <span style={descriptionStyle}>{description}</span>}
            </div>
          )}
        </label>
        {error && <div style={errorStyle}>{error}</div>}
      </div>
    )
  }
)

Checkbox.displayName = 'Checkbox'
