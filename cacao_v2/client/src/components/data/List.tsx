import { CSSProperties, ReactNode } from 'react'
import { Box } from '../layout/Box'

export interface ListItem {
  key?: string
  title?: ReactNode
  description?: ReactNode
  avatar?: ReactNode
  extra?: ReactNode
  onClick?: () => void
}

export interface ListProps {
  items?: ListItem[]
  children?: ReactNode
  bordered?: boolean
  hoverable?: boolean
  size?: 'sm' | 'md' | 'lg'
  header?: ReactNode
  footer?: ReactNode
  loading?: boolean
  emptyText?: ReactNode
  split?: boolean
  className?: string
  style?: CSSProperties
}

const sizeStyles = {
  sm: { padding: '8px 12px', fontSize: '0.875rem' },
  md: { padding: '12px 16px', fontSize: '0.9375rem' },
  lg: { padding: '16px 20px', fontSize: '1rem' },
}

export function List({
  items,
  children,
  bordered = true,
  hoverable = true,
  size = 'md',
  header,
  footer,
  loading = false,
  emptyText = 'No items',
  split = true,
  className,
  style,
}: ListProps) {
  const containerStyle: CSSProperties = {
    backgroundColor: '#1e1e2e',
    borderRadius: '12px',
    border: bordered ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    overflow: 'hidden',
    ...style,
  }

  const headerStyle: CSSProperties = {
    ...sizeStyles[size],
    fontWeight: 600,
    color: 'rgba(255, 255, 255, 0.9)',
    borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
  }

  const footerStyle: CSSProperties = {
    ...sizeStyles[size],
    color: 'rgba(255, 255, 255, 0.6)',
    borderTop: '1px solid rgba(255, 255, 255, 0.1)',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
  }

  if (loading) {
    return (
      <Box className={className} style={containerStyle}>
        {header && <div style={headerStyle}>{header}</div>}
        <div style={{ padding: '40px', textAlign: 'center' }}>
          <LoadingSpinner />
        </div>
        {footer && <div style={footerStyle}>{footer}</div>}
      </Box>
    )
  }

  const hasItems = items && items.length > 0
  const hasChildren = !!children

  return (
    <Box className={className} style={containerStyle}>
      {header && <div style={headerStyle}>{header}</div>}

      {!hasItems && !hasChildren ? (
        <div style={{ padding: '40px', textAlign: 'center', color: 'rgba(255, 255, 255, 0.4)' }}>
          {emptyText}
        </div>
      ) : hasItems ? (
        items.map((item, index) => (
          <ListItemRow
            key={item.key ?? index}
            item={item}
            size={size}
            hoverable={hoverable}
            showBorder={split && index < items.length - 1}
          />
        ))
      ) : (
        children
      )}

      {footer && <div style={footerStyle}>{footer}</div>}
    </Box>
  )
}

interface ListItemRowProps {
  item: ListItem
  size: 'sm' | 'md' | 'lg'
  hoverable: boolean
  showBorder: boolean
}

function ListItemRow({ item, size, hoverable, showBorder }: ListItemRowProps) {
  const itemStyle: CSSProperties = {
    ...sizeStyles[size],
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    borderBottom: showBorder ? '1px solid rgba(255, 255, 255, 0.05)' : 'none',
    cursor: item.onClick ? 'pointer' : undefined,
    transition: 'background-color 0.15s',
  }

  return (
    <div
      style={itemStyle}
      onClick={item.onClick}
      onMouseEnter={(e) => {
        if (hoverable) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
        }
      }}
      onMouseLeave={(e) => {
        if (hoverable) {
          (e.currentTarget as HTMLElement).style.backgroundColor = ''
        }
      }}
    >
      {item.avatar && <div style={{ flexShrink: 0 }}>{item.avatar}</div>}

      <div style={{ flex: 1, minWidth: 0 }}>
        {item.title && (
          <div style={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 500 }}>
            {item.title}
          </div>
        )}
        {item.description && (
          <div style={{ color: 'rgba(255, 255, 255, 0.5)', fontSize: '0.875em', marginTop: '2px' }}>
            {item.description}
          </div>
        )}
      </div>

      {item.extra && <div style={{ flexShrink: 0 }}>{item.extra}</div>}
    </div>
  )
}

export interface ListItemProps {
  children?: ReactNode
  onClick?: () => void
  hoverable?: boolean
  className?: string
  style?: CSSProperties
}

export function ListItemComponent({
  children,
  onClick,
  hoverable = true,
  className,
  style,
}: ListItemProps) {
  const itemStyle: CSSProperties = {
    padding: '12px 16px',
    borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
    cursor: onClick ? 'pointer' : undefined,
    transition: 'background-color 0.15s',
    ...style,
  }

  return (
    <div
      className={className}
      style={itemStyle}
      onClick={onClick}
      onMouseEnter={(e) => {
        if (hoverable) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
        }
      }}
      onMouseLeave={(e) => {
        if (hoverable) {
          (e.currentTarget as HTMLElement).style.backgroundColor = ''
        }
      }}
    >
      {children}
    </div>
  )
}

List.Item = ListItemComponent

function LoadingSpinner() {
  return (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      style={{ animation: 'spin 1s linear infinite' }}
    >
      <style>
        {`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}
      </style>
      <circle cx="12" cy="12" r="10" stroke="rgba(167, 139, 250, 0.3)" strokeWidth="3" />
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="#a78bfa"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray="31.4 31.4"
        style={{ transform: 'rotate(-90deg)', transformOrigin: 'center' }}
      />
    </svg>
  )
}
