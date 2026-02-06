import { CSSProperties, ReactNode, forwardRef } from 'react'

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'ghost' | 'outline'
export type ButtonSize = 'sm' | 'md' | 'lg'

export interface ButtonProps {
  children?: ReactNode
  variant?: ButtonVariant
  size?: ButtonSize
  disabled?: boolean
  loading?: boolean
  fullWidth?: boolean
  leftIcon?: ReactNode
  rightIcon?: ReactNode
  className?: string
  style?: CSSProperties
  type?: 'button' | 'submit' | 'reset'
  onClick?: () => void
}

const variantStyles: Record<ButtonVariant, CSSProperties> = {
  primary: {
    backgroundColor: '#7c3aed',
    color: '#ffffff',
    border: 'none',
  },
  secondary: {
    backgroundColor: '#4b5563',
    color: '#ffffff',
    border: 'none',
  },
  danger: {
    backgroundColor: '#ef4444',
    color: '#ffffff',
    border: 'none',
  },
  success: {
    backgroundColor: '#10b981',
    color: '#ffffff',
    border: 'none',
  },
  warning: {
    backgroundColor: '#f59e0b',
    color: '#000000',
    border: 'none',
  },
  ghost: {
    backgroundColor: 'transparent',
    color: '#a78bfa',
    border: 'none',
  },
  outline: {
    backgroundColor: 'transparent',
    color: '#a78bfa',
    border: '1px solid #a78bfa',
  },
}

const sizeStyles: Record<ButtonSize, CSSProperties> = {
  sm: {
    padding: '6px 12px',
    fontSize: '14px',
    borderRadius: '6px',
  },
  md: {
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '8px',
  },
  lg: {
    padding: '14px 28px',
    fontSize: '18px',
    borderRadius: '10px',
  },
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      disabled = false,
      loading = false,
      fullWidth = false,
      leftIcon,
      rightIcon,
      className,
      style,
      type = 'button',
      onClick,
    },
    ref
  ) => {
    const isDisabled = disabled || loading

    const buttonStyle: CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px',
      fontWeight: 600,
      cursor: isDisabled ? 'not-allowed' : 'pointer',
      opacity: isDisabled ? 0.6 : 1,
      transition: 'all 0.2s ease',
      width: fullWidth ? '100%' : undefined,
      ...variantStyles[variant],
      ...sizeStyles[size],
      ...style,
    }

    return (
      <button
        ref={ref}
        type={type}
        className={className}
        style={buttonStyle}
        disabled={isDisabled}
        onClick={onClick}
      >
        {loading ? (
          <LoadingSpinner size={size} />
        ) : (
          <>
            {leftIcon}
            {children}
            {rightIcon}
          </>
        )}
      </button>
    )
  }
)

Button.displayName = 'Button'

function LoadingSpinner({ size }: { size: ButtonSize }) {
  const spinnerSize = size === 'sm' ? 14 : size === 'md' ? 18 : 22

  return (
    <svg
      width={spinnerSize}
      height={spinnerSize}
      viewBox="0 0 24 24"
      fill="none"
      style={{
        animation: 'spin 1s linear infinite',
      }}
    >
      <style>
        {`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}
      </style>
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray="31.4 31.4"
        opacity={0.25}
      />
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray="31.4 31.4"
        strokeDashoffset="62.8"
        style={{ transform: 'rotate(-90deg)', transformOrigin: 'center' }}
      />
    </svg>
  )
}
