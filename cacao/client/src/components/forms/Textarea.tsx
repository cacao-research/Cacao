import { CSSProperties, forwardRef, TextareaHTMLAttributes } from 'react'

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  hint?: string
  fullWidth?: boolean
  resize?: 'none' | 'vertical' | 'horizontal' | 'both'
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      label,
      error,
      hint,
      fullWidth = false,
      resize = 'vertical',
      disabled,
      className,
      style,
      rows = 4,
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

    const textareaStyle: CSSProperties = {
      width: '100%',
      padding: '10px 14px',
      fontSize: '16px',
      borderRadius: '8px',
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
      border: `1px solid ${hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.1)'}`,
      color: '#ffffff',
      outline: 'none',
      transition: 'border-color 0.2s, box-shadow 0.2s',
      resize,
      opacity: disabled ? 0.5 : 1,
      cursor: disabled ? 'not-allowed' : 'text',
      fontFamily: 'inherit',
      ...style,
    }

    const hintStyle: CSSProperties = {
      fontSize: '12px',
      color: hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.5)',
    }

    return (
      <div className={className} style={containerStyle}>
        {label && <label style={labelStyle}>{label}</label>}
        <textarea
          ref={ref}
          rows={rows}
          disabled={disabled}
          style={textareaStyle}
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
        {(error || hint) && <span style={hintStyle}>{error || hint}</span>}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'
