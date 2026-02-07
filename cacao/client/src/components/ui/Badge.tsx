import { CSSProperties, ReactNode } from 'react'

export type BadgeVariant = 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info'
export type BadgeSize = 'sm' | 'md' | 'lg'

export interface BadgeProps {
  children?: ReactNode
  variant?: BadgeVariant
  size?: BadgeSize
  dot?: boolean
  outline?: boolean
  className?: string
  style?: CSSProperties
}

const variantStyles: Record<BadgeVariant, { bg: string; color: string; border: string }> = {
  default: { bg: 'rgba(255, 255, 255, 0.1)', color: '#ffffff', border: 'rgba(255, 255, 255, 0.2)' },
  primary: { bg: 'rgba(124, 58, 237, 0.2)', color: '#a78bfa', border: '#7c3aed' },
  secondary: { bg: 'rgba(75, 85, 99, 0.3)', color: '#9ca3af', border: '#4b5563' },
  success: { bg: 'rgba(16, 185, 129, 0.2)', color: '#34d399', border: '#10b981' },
  warning: { bg: 'rgba(245, 158, 11, 0.2)', color: '#fbbf24', border: '#f59e0b' },
  danger: { bg: 'rgba(239, 68, 68, 0.2)', color: '#f87171', border: '#ef4444' },
  info: { bg: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa', border: '#3b82f6' },
}

const sizeStyles: Record<BadgeSize, CSSProperties> = {
  sm: { fontSize: '10px', padding: '2px 6px', borderRadius: '4px' },
  md: { fontSize: '12px', padding: '3px 8px', borderRadius: '6px' },
  lg: { fontSize: '14px', padding: '4px 10px', borderRadius: '8px' },
}

export function Badge({
  children,
  variant = 'default',
  size = 'md',
  dot = false,
  outline = false,
  className,
  style,
}: BadgeProps) {
  const colors = variantStyles[variant]
  const sizing = sizeStyles[size]

  const badgeStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    fontWeight: 500,
    whiteSpace: 'nowrap',
    backgroundColor: outline ? 'transparent' : colors.bg,
    color: colors.color,
    border: outline ? `1px solid ${colors.border}` : 'none',
    ...sizing,
    ...style,
  }

  const dotSize = size === 'sm' ? 6 : size === 'md' ? 8 : 10

  return (
    <span className={className} style={badgeStyle}>
      {dot && (
        <span
          style={{
            width: dotSize,
            height: dotSize,
            borderRadius: '50%',
            backgroundColor: colors.color,
          }}
        />
      )}
      {children}
    </span>
  )
}
