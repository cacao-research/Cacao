import { CSSProperties, ReactNode } from 'react'
import { Box, BoxProps } from '../layout/Box'

export interface CardProps extends Omit<BoxProps, 'children'> {
  children?: ReactNode
  title?: ReactNode
  subtitle?: ReactNode
  extra?: ReactNode
  footer?: ReactNode
  hoverable?: boolean
  bordered?: boolean
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  padding?: number | 'none'
}

const shadowStyles = {
  none: 'none',
  sm: '0 1px 2px rgba(0, 0, 0, 0.1)',
  md: '0 4px 6px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px rgba(0, 0, 0, 0.2)',
}

export function Card({
  children,
  title,
  subtitle,
  extra,
  footer,
  hoverable = false,
  bordered = true,
  shadow = 'md',
  padding = 4,
  style,
  ...rest
}: CardProps) {
  const cardStyle: CSSProperties = {
    backgroundColor: '#1e1e2e',
    borderRadius: '12px',
    border: bordered ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    boxShadow: shadowStyles[shadow],
    overflow: 'hidden',
    transition: hoverable ? 'transform 0.2s, box-shadow 0.2s' : undefined,
    ...style,
  }

  const headerStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    padding: padding === 'none' ? 0 : `${Number(padding) * 4}px`,
    paddingBottom: children ? `${Number(padding) * 2}px` : undefined,
    borderBottom: children ? '1px solid rgba(255, 255, 255, 0.05)' : 'none',
  }

  const bodyStyle: CSSProperties = {
    padding: padding === 'none' ? 0 : `${Number(padding) * 4}px`,
  }

  const footerStyle: CSSProperties = {
    padding: padding === 'none' ? 0 : `${Number(padding) * 4}px`,
    paddingTop: `${Number(padding) * 2}px`,
    borderTop: '1px solid rgba(255, 255, 255, 0.05)',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
  }

  const hasHeader = title || subtitle || extra

  return (
    <Box style={cardStyle} {...rest}>
      {hasHeader && (
        <div style={headerStyle}>
          <div>
            {title && (
              <div style={{ fontSize: '1.125rem', fontWeight: 600, color: '#ffffff' }}>
                {title}
              </div>
            )}
            {subtitle && (
              <div style={{ fontSize: '0.875rem', color: 'rgba(255, 255, 255, 0.6)', marginTop: '4px' }}>
                {subtitle}
              </div>
            )}
          </div>
          {extra && <div>{extra}</div>}
        </div>
      )}
      {children && <div style={bodyStyle}>{children}</div>}
      {footer && <div style={footerStyle}>{footer}</div>}
    </Box>
  )
}

export interface CardSectionProps {
  children?: ReactNode
  title?: string
  className?: string
  style?: CSSProperties
}

export function CardSection({ children, title, className, style }: CardSectionProps) {
  return (
    <div className={className} style={{ marginTop: '16px', ...style }}>
      {title && (
        <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'rgba(255, 255, 255, 0.5)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          {title}
        </div>
      )}
      {children}
    </div>
  )
}
