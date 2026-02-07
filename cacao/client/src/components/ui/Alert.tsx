import { CSSProperties, ReactNode } from 'react'

export type AlertVariant = 'info' | 'success' | 'warning' | 'error'

export interface AlertProps {
  children?: ReactNode
  variant?: AlertVariant
  title?: string
  icon?: ReactNode
  closable?: boolean
  onClose?: () => void
  className?: string
  style?: CSSProperties
}

const variantStyles: Record<AlertVariant, { bg: string; border: string; color: string; icon: string }> = {
  info: {
    bg: 'rgba(59, 130, 246, 0.1)',
    border: 'rgba(59, 130, 246, 0.3)',
    color: '#60a5fa',
    icon: 'ℹ',
  },
  success: {
    bg: 'rgba(16, 185, 129, 0.1)',
    border: 'rgba(16, 185, 129, 0.3)',
    color: '#34d399',
    icon: '✓',
  },
  warning: {
    bg: 'rgba(245, 158, 11, 0.1)',
    border: 'rgba(245, 158, 11, 0.3)',
    color: '#fbbf24',
    icon: '⚠',
  },
  error: {
    bg: 'rgba(239, 68, 68, 0.1)',
    border: 'rgba(239, 68, 68, 0.3)',
    color: '#f87171',
    icon: '✕',
  },
}

export function Alert({
  children,
  variant = 'info',
  title,
  icon,
  closable = false,
  onClose,
  className,
  style,
}: AlertProps) {
  const colors = variantStyles[variant]

  const alertStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '12px',
    padding: '12px 16px',
    borderRadius: '8px',
    backgroundColor: colors.bg,
    border: `1px solid ${colors.border}`,
    color: '#ffffff',
    ...style,
  }

  const iconStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '20px',
    height: '20px',
    borderRadius: '50%',
    backgroundColor: colors.color,
    color: '#000000',
    fontSize: '12px',
    fontWeight: 700,
    flexShrink: 0,
  }

  const closeButtonStyle: CSSProperties = {
    background: 'none',
    border: 'none',
    color: 'rgba(255, 255, 255, 0.5)',
    cursor: 'pointer',
    padding: '4px',
    fontSize: '16px',
    lineHeight: 1,
    marginLeft: 'auto',
  }

  return (
    <div className={className} style={alertStyle} role="alert">
      <div style={iconStyle}>{icon ?? colors.icon}</div>
      <div style={{ flex: 1 }}>
        {title && (
          <div style={{ fontWeight: 600, marginBottom: children ? '4px' : 0, color: colors.color }}>
            {title}
          </div>
        )}
        {children && <div style={{ fontSize: '0.875rem', opacity: 0.9 }}>{children}</div>}
      </div>
      {closable && (
        <button style={closeButtonStyle} onClick={onClose} aria-label="Close">
          ×
        </button>
      )}
    </div>
  )
}
