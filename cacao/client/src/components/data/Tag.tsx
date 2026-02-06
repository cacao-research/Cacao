import { CSSProperties, ReactNode } from 'react'

export type TagColor = 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'

export interface TagProps {
  children?: ReactNode
  color?: TagColor
  size?: 'sm' | 'md' | 'lg'
  closable?: boolean
  onClose?: () => void
  icon?: ReactNode
  bordered?: boolean
  className?: string
  style?: CSSProperties
}

const colorStyles: Record<TagColor, { bg: string; color: string; border: string }> = {
  default: {
    bg: 'rgba(255, 255, 255, 0.1)',
    color: 'rgba(255, 255, 255, 0.8)',
    border: 'rgba(255, 255, 255, 0.2)',
  },
  primary: {
    bg: 'rgba(124, 58, 237, 0.2)',
    color: '#a78bfa',
    border: 'rgba(124, 58, 237, 0.4)',
  },
  success: {
    bg: 'rgba(16, 185, 129, 0.2)',
    color: '#34d399',
    border: 'rgba(16, 185, 129, 0.4)',
  },
  warning: {
    bg: 'rgba(245, 158, 11, 0.2)',
    color: '#fbbf24',
    border: 'rgba(245, 158, 11, 0.4)',
  },
  danger: {
    bg: 'rgba(239, 68, 68, 0.2)',
    color: '#f87171',
    border: 'rgba(239, 68, 68, 0.4)',
  },
  info: {
    bg: 'rgba(59, 130, 246, 0.2)',
    color: '#60a5fa',
    border: 'rgba(59, 130, 246, 0.4)',
  },
}

const sizeStyles = {
  sm: { padding: '2px 6px', fontSize: '0.75rem', borderRadius: '4px' },
  md: { padding: '4px 10px', fontSize: '0.8125rem', borderRadius: '6px' },
  lg: { padding: '6px 12px', fontSize: '0.875rem', borderRadius: '8px' },
}

export function Tag({
  children,
  color = 'default',
  size = 'md',
  closable = false,
  onClose,
  icon,
  bordered = true,
  className,
  style,
}: TagProps) {
  const colors = colorStyles[color]
  const sizes = sizeStyles[size]

  const tagStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    fontWeight: 500,
    whiteSpace: 'nowrap',
    backgroundColor: colors.bg,
    color: colors.color,
    border: bordered ? `1px solid ${colors.border}` : 'none',
    ...sizes,
    ...style,
  }

  const closeButtonStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: '2px',
    padding: '2px',
    borderRadius: '2px',
    cursor: 'pointer',
    opacity: 0.7,
    transition: 'opacity 0.15s',
  }

  return (
    <span className={className} style={tagStyle}>
      {icon && <span style={{ display: 'inline-flex' }}>{icon}</span>}
      {children}
      {closable && (
        <span
          style={closeButtonStyle}
          onClick={(e) => {
            e.stopPropagation()
            onClose?.()
          }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLElement).style.opacity = '1'
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLElement).style.opacity = '0.7'
          }}
        >
          <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
            <path d="M3.5 3.5L8.5 8.5M8.5 3.5L3.5 8.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </span>
      )}
    </span>
  )
}

export interface TagGroupProps {
  children?: ReactNode
  wrap?: boolean
  gap?: number
  className?: string
  style?: CSSProperties
}

export function TagGroup({
  children,
  wrap = true,
  gap = 8,
  className,
  style,
}: TagGroupProps) {
  const groupStyle: CSSProperties = {
    display: 'flex',
    flexWrap: wrap ? 'wrap' : 'nowrap',
    gap: `${gap}px`,
    ...style,
  }

  return (
    <div className={className} style={groupStyle}>
      {children}
    </div>
  )
}
