import { CSSProperties, ReactNode, useState } from 'react'

export interface SidebarProps {
  children?: ReactNode
  width?: number
  collapsedWidth?: number
  collapsed?: boolean
  defaultCollapsed?: boolean
  onCollapse?: (collapsed: boolean) => void
  header?: ReactNode
  footer?: ReactNode
  bordered?: boolean
  className?: string
  style?: CSSProperties
}

export function Sidebar({
  children,
  width = 260,
  collapsedWidth = 64,
  collapsed: controlledCollapsed,
  defaultCollapsed = false,
  onCollapse,
  header,
  footer,
  bordered = true,
  className,
  style,
}: SidebarProps) {
  const [internalCollapsed, setInternalCollapsed] = useState(defaultCollapsed)
  const isCollapsed = controlledCollapsed ?? internalCollapsed

  const handleToggle = () => {
    const newValue = !isCollapsed
    if (controlledCollapsed === undefined) {
      setInternalCollapsed(newValue)
    }
    onCollapse?.(newValue)
  }

  const sidebarStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: `${isCollapsed ? collapsedWidth : width}px`,
    height: '100%',
    backgroundColor: '#1e1e2e',
    borderRight: bordered ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    transition: 'width 0.2s ease',
    overflow: 'hidden',
    flexShrink: 0,
    ...style,
  }

  const headerStyle: CSSProperties = {
    padding: isCollapsed ? '16px 8px' : '16px',
    borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: isCollapsed ? 'center' : 'space-between',
  }

  const contentStyle: CSSProperties = {
    flex: 1,
    overflow: 'auto',
    padding: isCollapsed ? '8px' : '8px 12px',
  }

  const footerStyle: CSSProperties = {
    padding: isCollapsed ? '16px 8px' : '16px',
    borderTop: '1px solid rgba(255, 255, 255, 0.1)',
  }

  const toggleButtonStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '28px',
    height: '28px',
    borderRadius: '6px',
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    border: 'none',
    cursor: 'pointer',
    color: 'rgba(255, 255, 255, 0.6)',
    transition: 'all 0.15s',
  }

  return (
    <aside className={className} style={sidebarStyle}>
      {header !== undefined ? (
        <div style={headerStyle}>{header}</div>
      ) : (
        <div style={headerStyle}>
          {!isCollapsed && <div style={{ width: '28px' }} />}
          <button
            style={toggleButtonStyle}
            onClick={handleToggle}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.1)'
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
            }}
          >
            <CollapseIcon collapsed={isCollapsed} />
          </button>
        </div>
      )}

      <div style={contentStyle}>
        <SidebarContext.Provider value={{ collapsed: isCollapsed }}>
          {children}
        </SidebarContext.Provider>
      </div>

      {footer && <div style={footerStyle}>{footer}</div>}
    </aside>
  )
}

import { createContext, useContext } from 'react'

const SidebarContext = createContext<{ collapsed: boolean }>({ collapsed: false })

export interface SidebarGroupProps {
  children?: ReactNode
  title?: string
  collapsible?: boolean
  defaultOpen?: boolean
  className?: string
  style?: CSSProperties
}

export function SidebarGroup({
  children,
  title,
  collapsible = false,
  defaultOpen = true,
  className,
  style,
}: SidebarGroupProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen)
  const { collapsed: sidebarCollapsed } = useContext(SidebarContext)

  const groupStyle: CSSProperties = {
    marginBottom: '8px',
    ...style,
  }

  const titleStyle: CSSProperties = {
    display: sidebarCollapsed ? 'none' : 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '8px 12px',
    fontSize: '0.6875rem',
    fontWeight: 600,
    color: 'rgba(255, 255, 255, 0.4)',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    cursor: collapsible ? 'pointer' : undefined,
  }

  return (
    <div className={className} style={groupStyle}>
      {title && (
        <div style={titleStyle} onClick={() => collapsible && setIsOpen(!isOpen)}>
          <span>{title}</span>
          {collapsible && (
            <ChevronIcon style={{ transform: isOpen ? 'rotate(0deg)' : 'rotate(-90deg)', transition: 'transform 0.2s' }} />
          )}
        </div>
      )}
      {(!collapsible || isOpen) && children}
    </div>
  )
}

export interface SidebarItemProps {
  children?: ReactNode
  icon?: ReactNode
  active?: boolean
  disabled?: boolean
  badge?: ReactNode
  onClick?: () => void
  className?: string
  style?: CSSProperties
}

export function SidebarItem({
  children,
  icon,
  active = false,
  disabled = false,
  badge,
  onClick,
  className,
  style,
}: SidebarItemProps) {
  const { collapsed } = useContext(SidebarContext)

  const itemStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: collapsed ? 'center' : 'flex-start',
    gap: '12px',
    padding: collapsed ? '10px' : '10px 12px',
    fontSize: '0.875rem',
    fontWeight: 500,
    color: active ? '#a78bfa' : 'rgba(255, 255, 255, 0.7)',
    backgroundColor: active ? 'rgba(167, 139, 250, 0.15)' : 'transparent',
    borderRadius: '8px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.15s',
    marginBottom: '2px',
    ...style,
  }

  const iconStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '20px',
    height: '20px',
    flexShrink: 0,
  }

  const labelStyle: CSSProperties = {
    flex: 1,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  }

  return (
    <div
      className={className}
      style={itemStyle}
      onClick={disabled ? undefined : onClick}
      title={collapsed && typeof children === 'string' ? children : undefined}
      onMouseEnter={(e) => {
        if (!disabled && !active) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled && !active) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent'
        }
      }}
    >
      {icon && <span style={iconStyle}>{icon}</span>}
      {!collapsed && <span style={labelStyle}>{children}</span>}
      {!collapsed && badge && <span>{badge}</span>}
    </div>
  )
}

function CollapseIcon({ collapsed }: { collapsed: boolean }) {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      style={{ transform: collapsed ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}
    >
      <path d="M10 4L6 8L10 12" />
    </svg>
  )
}

function ChevronIcon({ style }: { style?: CSSProperties }) {
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor" style={style}>
      <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" />
    </svg>
  )
}

Sidebar.Group = SidebarGroup
Sidebar.Item = SidebarItem
