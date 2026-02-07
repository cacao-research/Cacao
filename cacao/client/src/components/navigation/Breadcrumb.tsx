import { CSSProperties, ReactNode } from 'react'

export interface BreadcrumbItem {
  key?: string
  label: ReactNode
  href?: string
  icon?: ReactNode
  onClick?: () => void
}

export interface BreadcrumbProps {
  items: BreadcrumbItem[]
  separator?: ReactNode
  maxItems?: number
  size?: 'sm' | 'md' | 'lg'
  className?: string
  style?: CSSProperties
}

const sizeStyles = {
  sm: { fontSize: '0.75rem', gap: '6px', iconSize: 12 },
  md: { fontSize: '0.875rem', gap: '8px', iconSize: 14 },
  lg: { fontSize: '1rem', gap: '10px', iconSize: 16 },
}

export function Breadcrumb({
  items,
  separator = <DefaultSeparator />,
  maxItems,
  size = 'md',
  className,
  style,
}: BreadcrumbProps) {
  const sizes = sizeStyles[size]

  const containerStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: `${sizes.gap}px`,
    fontSize: sizes.fontSize,
    ...style,
  }

  let displayItems = items

  if (maxItems && items.length > maxItems) {
    const firstItem = items[0]
    const lastItems = items.slice(-(maxItems - 1))
    displayItems = [
      firstItem,
      { key: '__ellipsis__', label: '...' },
      ...lastItems,
    ]
  }

  return (
    <nav className={className} style={containerStyle} aria-label="Breadcrumb">
      {displayItems.map((item, index) => {
        const isLast = index === displayItems.length - 1
        const isEllipsis = item.key === '__ellipsis__'

        return (
          <BreadcrumbItemComponent
            key={item.key ?? index}
            item={item}
            isLast={isLast}
            isEllipsis={isEllipsis}
            separator={separator}
            iconSize={sizes.iconSize}
          />
        )
      })}
    </nav>
  )
}

interface BreadcrumbItemComponentProps {
  item: BreadcrumbItem
  isLast: boolean
  isEllipsis: boolean
  separator: ReactNode
  iconSize: number
}

function BreadcrumbItemComponent({
  item,
  isLast,
  isEllipsis,
  separator,
  iconSize,
}: BreadcrumbItemComponentProps) {
  const itemStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
  }

  const linkStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    color: isLast ? 'rgba(255, 255, 255, 0.9)' : 'rgba(255, 255, 255, 0.5)',
    fontWeight: isLast ? 500 : 400,
    textDecoration: 'none',
    cursor: isLast || isEllipsis ? 'default' : 'pointer',
    transition: 'color 0.15s',
  }

  const separatorStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    color: 'rgba(255, 255, 255, 0.3)',
  }

  const iconStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    width: iconSize,
    height: iconSize,
  }

  const handleClick = () => {
    if (!isLast && !isEllipsis && item.onClick) {
      item.onClick()
    }
  }

  const content = (
    <>
      {item.icon && <span style={iconStyle}>{item.icon}</span>}
      <span>{item.label}</span>
    </>
  )

  return (
    <span style={itemStyle}>
      {item.href && !isLast ? (
        <a
          href={item.href}
          style={linkStyle}
          onMouseEnter={(e) => {
            if (!isLast) {
              (e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.9)'
            }
          }}
          onMouseLeave={(e) => {
            if (!isLast) {
              (e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.5)'
            }
          }}
        >
          {content}
        </a>
      ) : (
        <span
          style={linkStyle}
          onClick={handleClick}
          onMouseEnter={(e) => {
            if (!isLast && !isEllipsis && item.onClick) {
              (e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.9)'
            }
          }}
          onMouseLeave={(e) => {
            if (!isLast && !isEllipsis && item.onClick) {
              (e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.5)'
            }
          }}
        >
          {content}
        </span>
      )}
      {!isLast && <span style={separatorStyle}>{separator}</span>}
    </span>
  )
}

function DefaultSeparator() {
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
      <path d="M4.5 2.5L7.5 6L4.5 9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  )
}

export interface BreadcrumbSeparatorProps {
  children?: ReactNode
}

export function BreadcrumbSeparator({ children }: BreadcrumbSeparatorProps) {
  return <>{children ?? <DefaultSeparator />}</>
}

Breadcrumb.Separator = BreadcrumbSeparator
