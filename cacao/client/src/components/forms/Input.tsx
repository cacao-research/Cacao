import { CSSProperties, forwardRef, InputHTMLAttributes } from 'react'

export type InputSize = 'sm' | 'md' | 'lg'

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string
  error?: string
  hint?: string
  inputSize?: InputSize
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
}

const sizeStyles: Record<InputSize, CSSProperties> = {
  sm: { padding: '6px 10px', fontSize: '14px', borderRadius: '6px' },
  md: { padding: '10px 14px', fontSize: '16px', borderRadius: '8px' },
  lg: { padding: '14px 18px', fontSize: '18px', borderRadius: '10px' },
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      hint,
      inputSize = 'md',
      leftIcon,
      rightIcon,
      fullWidth = false,
      disabled,
      className,
      style,
      ...rest
    },
    ref
  ) => {
    const hasError = Boolean(error)

    const containerStyle: CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      gap: '6px',
      width: fullWidth ? '100%' : undefined,
    }

    const labelStyle: CSSProperties = {
      fontSize: '14px',
      fontWeight: 500,
      color: 'rgba(255, 255, 255, 0.8)',
    }

    const inputWrapperStyle: CSSProperties = {
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
    }

    const inputStyle: CSSProperties = {
      width: '100%',
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
      border: `1px solid ${hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.1)'}`,
      color: '#ffffff',
      outline: 'none',
      transition: 'border-color 0.2s, box-shadow 0.2s',
      paddingLeft: leftIcon ? '40px' : undefined,
      paddingRight: rightIcon ? '40px' : undefined,
      opacity: disabled ? 0.5 : 1,
      cursor: disabled ? 'not-allowed' : 'text',
      ...sizeStyles[inputSize],
      ...style,
    }

    const iconStyle: CSSProperties = {
      position: 'absolute',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'rgba(255, 255, 255, 0.4)',
      pointerEvents: 'none',
    }

    const hintStyle: CSSProperties = {
      fontSize: '12px',
      color: hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.5)',
    }

    return (
      <div className={className} style={containerStyle}>
        {label && <label style={labelStyle}>{label}</label>}
        <div style={inputWrapperStyle}>
          {leftIcon && <span style={{ ...iconStyle, left: '12px' }}>{leftIcon}</span>}
          <input
            ref={ref}
            disabled={disabled}
            style={inputStyle}
            onFocus={(e) => {
              e.target.style.borderColor = hasError ? '#ef4444' : '#7c3aed'
              e.target.style.boxShadow = `0 0 0 3px ${hasError ? 'rgba(239, 68, 68, 0.2)' : 'rgba(124, 58, 237, 0.2)'}`
            }}
            onBlur={(e) => {
              e.target.style.borderColor = hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.1)'
              e.target.style.boxShadow = 'none'
            }}
            {...rest}
          />
          {rightIcon && <span style={{ ...iconStyle, right: '12px' }}>{rightIcon}</span>}
        </div>
        {(error || hint) && <span style={hintStyle}>{error || hint}</span>}
      </div>
    )
  }
)

Input.displayName = 'Input'
