import { CSSProperties, ReactNode, useState, createContext, useContext } from 'react'
import { Box } from '../layout/Box'

export interface MenuItem {
  key: string
  label: ReactNode
  icon?: ReactNode
  disabled?: boolean
  children?: MenuItem[]
  danger?: boolean
}

export interface MenuProps {
  items?: MenuItem[]
  children?: ReactNode
  selectedKey?: string
  defaultSelectedKey?: string
  openKeys?: string[]
  defaultOpenKeys?: string[]
  mode?: 'vertical' | 'horizontal' | 'inline'
  collapsed?: boolean
  bordered?: boolean
  onSelect?: (key: string) => void
  onOpenChange?: (keys: string[]) => void
  className?: string
  style?: CSSProperties
}

const MenuContext = createContext<{
  selectedKey: string | null
  openKeys: string[]
  mode: 'vertical' | 'horizontal' | 'inline'
  collapsed: boolean
  onSelect: (key: string) => void
  onToggle: (key: string) => void
}>({
  selectedKey: null,
  openKeys: [],
  mode: 'vertical',
  collapsed: false,
  onSelect: () => {},
  onToggle: () => {},
})

export function Menu({
  items,
  children,
  selectedKey: controlledSelectedKey,
  defaultSelectedKey,
  openKeys: controlledOpenKeys,
  defaultOpenKeys = [],
  mode = 'vertical',
  collapsed = false,
  bordered = true,
  onSelect,
  onOpenChange,
  className,
  style,
}: MenuProps) {
  const [internalSelectedKey, setInternalSelectedKey] = useState<string | null>(defaultSelectedKey ?? null)
  const [internalOpenKeys, setInternalOpenKeys] = useState<string[]>(defaultOpenKeys)

  const selectedKey = controlledSelectedKey ?? internalSelectedKey
  const openKeys = controlledOpenKeys ?? internalOpenKeys

  const handleSelect = (key: string) => {
    if (controlledSelectedKey === undefined) {
      setInternalSelectedKey(key)
    }
    onSelect?.(key)
  }

  const handleToggle = (key: string) => {
    const newKeys = openKeys.includes(key)
      ? openKeys.filter(k => k !== key)
      : [...openKeys, key]

    if (controlledOpenKeys === undefined) {
      setInternalOpenKeys(newKeys)
    }
    onOpenChange?.(newKeys)
  }

  const containerStyle: CSSProperties = {
    display: mode === 'horizontal' ? 'flex' : 'block',
    backgroundColor: mode === 'horizontal' ? 'transparent' : '#1e1e2e',
    borderRadius: mode === 'horizontal' ? 0 : '12px',
    border: bordered && mode !== 'horizontal' ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    padding: mode === 'horizontal' ? 0 : '8px',
    overflow: 'hidden',
    ...style,
  }

  return (
    <MenuContext.Provider
      value={{
        selectedKey,
        openKeys,
        mode,
        collapsed,
        onSelect: handleSelect,
        onToggle: handleToggle,
      }}
    >
      <Box className={className} style={containerStyle}>
        {items ? items.map(item => (
          <MenuItemComponent key={item.key} item={item} level={0} />
        )) : children}
      </Box>
    </MenuContext.Provider>
  )
}

interface MenuItemComponentProps {
  item: MenuItem
  level: number
}

function MenuItemComponent({ item, level }: MenuItemComponentProps) {
  const { selectedKey, openKeys, mode, collapsed, onSelect, onToggle } = useContext(MenuContext)

  const hasChildren = item.children && item.children.length > 0
  const isOpen = openKeys.includes(item.key)
  const isSelected = selectedKey === item.key

  const itemStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: collapsed ? 'center' : 'space-between',
    gap: '10px',
    padding: mode === 'horizontal' ? '8px 16px' : collapsed ? '10px' : '10px 12px',
    paddingLeft: mode !== 'horizontal' && !collapsed ? `${12 + level * 16}px` : undefined,
    fontSize: '0.875rem',
    fontWeight: 500,
    color: item.danger
      ? '#f87171'
      : isSelected
      ? '#a78bfa'
      : 'rgba(255, 255, 255, 0.7)',
    backgroundColor: isSelected ? 'rgba(167, 139, 250, 0.15)' : 'transparent',
    borderRadius: '8px',
    cursor: item.disabled ? 'not-allowed' : 'pointer',
    opacity: item.disabled ? 0.5 : 1,
    transition: 'all 0.15s',
    marginBottom: mode === 'horizontal' ? 0 : '2px',
    whiteSpace: 'nowrap',
  }

  const iconStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    width: '18px',
    height: '18px',
    flexShrink: 0,
  }

  const chevronStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
    transition: 'transform 0.2s',
    marginLeft: 'auto',
  }

  const handleClick = () => {
    if (item.disabled) return
    if (hasChildren) {
      onToggle(item.key)
    } else {
      onSelect(item.key)
    }
  }

  return (
    <>
      <div
        style={itemStyle}
        onClick={handleClick}
        title={collapsed ? (typeof item.label === 'string' ? item.label : undefined) : undefined}
        onMouseEnter={(e) => {
          if (!item.disabled && !isSelected) {
            (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
          }
        }}
        onMouseLeave={(e) => {
          if (!item.disabled && !isSelected) {
            (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent'
          }
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {item.icon && <span style={iconStyle}>{item.icon}</span>}
          {!collapsed && <span>{item.label}</span>}
        </div>
        {hasChildren && !collapsed && (
          <span style={chevronStyle}>
            <ChevronIcon />
          </span>
        )}
      </div>

      {hasChildren && isOpen && !collapsed && (
        <div>
          {item.children!.map(child => (
            <MenuItemComponent key={child.key} item={child} level={level + 1} />
          ))}
        </div>
      )}
    </>
  )
}

export interface MenuItemProps {
  children?: ReactNode
  itemKey: string
  icon?: ReactNode
  disabled?: boolean
  danger?: boolean
  className?: string
  style?: CSSProperties
}

export function MenuItemElement({
  children,
  itemKey,
  icon,
  disabled = false,
  danger = false,
  className,
  style,
}: MenuItemProps) {
  const { selectedKey, collapsed, onSelect } = useContext(MenuContext)
  const isSelected = selectedKey === itemKey

  const itemStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: collapsed ? 'center' : 'flex-start',
    gap: '10px',
    padding: collapsed ? '10px' : '10px 12px',
    fontSize: '0.875rem',
    fontWeight: 500,
    color: danger ? '#f87171' : isSelected ? '#a78bfa' : 'rgba(255, 255, 255, 0.7)',
    backgroundColor: isSelected ? 'rgba(167, 139, 250, 0.15)' : 'transparent',
    borderRadius: '8px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.15s',
    marginBottom: '2px',
    ...style,
  }

  return (
    <div
      className={className}
      style={itemStyle}
      onClick={() => !disabled && onSelect(itemKey)}
      onMouseEnter={(e) => {
        if (!disabled && !isSelected) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled && !isSelected) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent'
        }
      }}
    >
      {icon && <span style={{ display: 'flex', width: '18px', height: '18px' }}>{icon}</span>}
      {!collapsed && children}
    </div>
  )
}

export interface MenuDividerProps {
  className?: string
  style?: CSSProperties
}

export function MenuDivider({ className, style }: MenuDividerProps) {
  const dividerStyle: CSSProperties = {
    height: '1px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    margin: '8px 0',
    ...style,
  }

  return <div className={className} style={dividerStyle} />
}

export interface MenuLabelProps {
  children?: ReactNode
  className?: string
  style?: CSSProperties
}

export function MenuLabel({ children, className, style }: MenuLabelProps) {
  const { collapsed } = useContext(MenuContext)

  if (collapsed) return null

  const labelStyle: CSSProperties = {
    padding: '8px 12px',
    fontSize: '0.6875rem',
    fontWeight: 600,
    color: 'rgba(255, 255, 255, 0.4)',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    ...style,
  }

  return (
    <div className={className} style={labelStyle}>
      {children}
    </div>
  )
}

function ChevronIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
      <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

Menu.Item = MenuItemElement
Menu.Divider = MenuDivider
Menu.Label = MenuLabel
