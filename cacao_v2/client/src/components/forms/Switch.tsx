import { CSSProperties, forwardRef, InputHTMLAttributes } from 'react'

export interface SwitchProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type' | 'size'> {
  label?: string
  description?: string
  inputSize?: 'sm' | 'md' | 'lg'
}

const sizeMap = {
  sm: { width: 36, height: 20, thumb: 16 },
  md: { width: 44, height: 24, thumb: 20 },
  lg: { width: 52, height: 28, thumb: 24 },
}

export const Switch = forwardRef<HTMLInputElement, SwitchProps>(
  ({ label, description, inputSize = 'md', disabled, className, style, checked, ...rest }, ref) => {
    const sizes = sizeMap[inputSize]

    const containerStyle: CSSProperties = {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      ...style,
    }

    const switchWrapperStyle: CSSProperties = {
      position: 'relative',
      width: sizes.width,
      height: sizes.height,
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

    const trackStyle: CSSProperties = {
      width: sizes.width,
      height: sizes.height,
      borderRadius: sizes.height / 2,
      backgroundColor: checked ? '#7c3aed' : 'rgba(255, 255, 255, 0.2)',
      transition: 'background-color 0.2s',
      position: 'relative',
    }

    const thumbStyle: CSSProperties = {
      position: 'absolute',
      top: (sizes.height - sizes.thumb) / 2,
      left: checked ? sizes.width - sizes.thumb - (sizes.height - sizes.thumb) / 2 : (sizes.height - sizes.thumb) / 2,
      width: sizes.thumb,
      height: sizes.thumb,
      borderRadius: '50%',
      backgroundColor: '#ffffff',
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
      transition: 'left 0.2s',
    }

    const labelContainerStyle: CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      gap: '2px',
    }

    const labelStyle: CSSProperties = {
      fontSize: inputSize === 'sm' ? '14px' : inputSize === 'md' ? '16px' : '18px',
      color: '#ffffff',
      fontWeight: 500,
    }

    const descriptionStyle: CSSProperties = {
      fontSize: '12px',
      color: 'rgba(255, 255, 255, 0.5)',
    }

    return (
      <label className={className} style={containerStyle}>
        <div style={switchWrapperStyle}>
          <input ref={ref} type="checkbox" disabled={disabled} checked={checked} style={inputStyle} {...rest} />
          <div style={trackStyle}>
            <div style={thumbStyle} />
          </div>
        </div>
        {(label || description) && (
          <div style={labelContainerStyle}>
            {label && <span style={labelStyle}>{label}</span>}
            {description && <span style={descriptionStyle}>{description}</span>}
          </div>
        )}
      </label>
    )
  }
)

Switch.displayName = 'Switch'
