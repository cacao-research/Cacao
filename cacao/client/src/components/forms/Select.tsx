import { CSSProperties, forwardRef, SelectHTMLAttributes } from 'react'

export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

export interface SelectProps extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string
  error?: string
  hint?: string
  options: SelectOption[]
  placeholder?: string
  inputSize?: 'sm' | 'md' | 'lg'
  fullWidth?: boolean
}

const sizeStyles: Record<'sm' | 'md' | 'lg', CSSProperties> = {
  sm: { padding: '6px 10px', fontSize: '14px', borderRadius: '6px' },
  md: { padding: '10px 14px', fontSize: '16px', borderRadius: '8px' },
  lg: { padding: '14px 18px', fontSize: '18px', borderRadius: '10px' },
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      label,
      error,
      hint,
      options,
      placeholder,
      inputSize = 'md',
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

    const selectStyle: CSSProperties = {
      width: '100%',
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
      border: `1px solid ${hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.1)'}`,
      color: '#ffffff',
      outline: 'none',
      transition: 'border-color 0.2s, box-shadow 0.2s',
      appearance: 'none',
      backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E")`,
      backgroundRepeat: 'no-repeat',
      backgroundPosition: 'right 10px center',
      backgroundSize: '16px',
      paddingRight: '36px',
      opacity: disabled ? 0.5 : 1,
      cursor: disabled ? 'not-allowed' : 'pointer',
      ...sizeStyles[inputSize],
      ...style,
    }

    const hintStyle: CSSProperties = {
      fontSize: '12px',
      color: hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.5)',
    }

    return (
      <div className={className} style={containerStyle}>
        {label && <label style={labelStyle}>{label}</label>}
        <select
          ref={ref}
          disabled={disabled}
          style={selectStyle}
          onFocus={(e) => {
            e.target.style.borderColor = hasError ? '#ef4444' : '#7c3aed'
            e.target.style.boxShadow = `0 0 0 3px ${hasError ? 'rgba(239, 68, 68, 0.2)' : 'rgba(124, 58, 237, 0.2)'}`
          }}
          onBlur={(e) => {
            e.target.style.borderColor = hasError ? '#ef4444' : 'rgba(255, 255, 255, 0.1)'
            e.target.style.boxShadow = 'none'
          }}
          {...rest}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option key={option.value} value={option.value} disabled={option.disabled}>
              {option.label}
            </option>
          ))}
        </select>
        {(error || hint) && <span style={hintStyle}>{error || hint}</span>}
      </div>
    )
  }
)

Select.displayName = 'Select'
