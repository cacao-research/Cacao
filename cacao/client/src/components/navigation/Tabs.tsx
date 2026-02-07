import { CSSProperties, ReactNode, useState, createContext, useContext } from 'react'

export interface TabItem {
  key: string
  label: ReactNode
  icon?: ReactNode
  disabled?: boolean
  closable?: boolean
  children?: ReactNode
}

export interface TabsProps {
  items?: TabItem[]
  children?: ReactNode
  activeKey?: string
  defaultActiveKey?: string
  variant?: 'line' | 'card' | 'pill'
  size?: 'sm' | 'md' | 'lg'
  position?: 'top' | 'bottom' | 'left' | 'right'
  centered?: boolean
  addable?: boolean
  onAdd?: () => void
  onChange?: (key: string) => void
  onClose?: (key: string) => void
  className?: string
  style?: CSSProperties
}

const sizeStyles = {
  sm: { padding: '6px 12px', fontSize: '0.8125rem', gap: '6px' },
  md: { padding: '10px 16px', fontSize: '0.875rem', gap: '8px' },
  lg: { padding: '12px 20px', fontSize: '1rem', gap: '10px' },
}

const TabsContext = createContext<{
  activeKey: string | null
  variant: 'line' | 'card' | 'pill'
  size: 'sm' | 'md' | 'lg'
  onSelect: (key: string) => void
  onClose?: (key: string) => void
}>({
  activeKey: null,
  variant: 'line',
  size: 'md',
  onSelect: () => {},
})

export function Tabs({
  items,
  children,
  activeKey: controlledActiveKey,
  defaultActiveKey,
  variant = 'line',
  size = 'md',
  position = 'top',
  centered = false,
  addable = false,
  onAdd,
  onChange,
  onClose,
  className,
  style,
}: TabsProps) {
  const [internalActiveKey, setInternalActiveKey] = useState<string | null>(
    defaultActiveKey ?? items?.[0]?.key ?? null
  )

  const activeKey = controlledActiveKey ?? internalActiveKey

  const handleSelect = (key: string) => {
    if (controlledActiveKey === undefined) {
      setInternalActiveKey(key)
    }
    onChange?.(key)
  }

  const isVertical = position === 'left' || position === 'right'

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: isVertical
      ? position === 'left' ? 'row' : 'row-reverse'
      : position === 'top' ? 'column' : 'column-reverse',
    ...style,
  }

  const tabListStyle: CSSProperties = {
    display: 'flex',
    flexDirection: isVertical ? 'column' : 'row',
    alignItems: centered && !isVertical ? 'center' : 'stretch',
    justifyContent: centered && !isVertical ? 'center' : 'flex-start',
    gap: variant === 'pill' ? '8px' : '0',
    borderBottom: !isVertical && variant === 'line' ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    borderRight: isVertical && position === 'left' && variant === 'line' ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    borderLeft: isVertical && position === 'right' && variant === 'line' ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    backgroundColor: variant === 'card' ? 'rgba(0, 0, 0, 0.2)' : 'transparent',
    padding: variant === 'card' ? '4px' : variant === 'pill' ? '4px' : '0',
    borderRadius: variant === 'card' || variant === 'pill' ? '12px' : 0,
  }

  const contentStyle: CSSProperties = {
    flex: 1,
    padding: '16px 0',
  }

  const activeItem = items?.find(item => item.key === activeKey)

  return (
    <TabsContext.Provider value={{ activeKey, variant, size, onSelect: handleSelect, onClose }}>
      <div className={className} style={containerStyle}>
        <div style={tabListStyle}>
          {items ? items.map(item => (
            <TabButton key={item.key} item={item} isVertical={isVertical} />
          )) : children}

          {addable && (
            <AddButton size={size} onClick={onAdd} />
          )}
        </div>

        {activeItem?.children && (
          <div style={contentStyle}>{activeItem.children}</div>
        )}
      </div>
    </TabsContext.Provider>
  )
}

interface TabButtonProps {
  item: TabItem
  isVertical: boolean
}

function TabButton({ item, isVertical }: TabButtonProps) {
  const { activeKey, variant, size, onSelect, onClose } = useContext(TabsContext)
  const isActive = activeKey === item.key
  const sizes = sizeStyles[size]

  const baseStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: sizes.gap,
    padding: sizes.padding,
    fontSize: sizes.fontSize,
    fontWeight: 500,
    cursor: item.disabled ? 'not-allowed' : 'pointer',
    opacity: item.disabled ? 0.5 : 1,
    transition: 'all 0.15s',
    whiteSpace: 'nowrap',
    border: 'none',
    background: 'none',
    position: 'relative',
  }

  const lineStyle: CSSProperties = {
    ...baseStyle,
    color: isActive ? '#a78bfa' : 'rgba(255, 255, 255, 0.6)',
    marginBottom: isVertical ? 0 : '-1px',
    marginRight: isVertical ? '-1px' : 0,
    borderBottom: !isVertical && isActive ? '2px solid #a78bfa' : !isVertical ? '2px solid transparent' : 'none',
    borderRight: isVertical && isActive ? '2px solid #a78bfa' : isVertical ? '2px solid transparent' : 'none',
  }

  const cardStyle: CSSProperties = {
    ...baseStyle,
    color: isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.6)',
    backgroundColor: isActive ? '#1e1e2e' : 'transparent',
    borderRadius: '8px',
  }

  const pillStyle: CSSProperties = {
    ...baseStyle,
    color: isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.6)',
    backgroundColor: isActive ? '#7c3aed' : 'transparent',
    borderRadius: '8px',
  }

  const tabStyle = variant === 'line' ? lineStyle : variant === 'card' ? cardStyle : pillStyle

  return (
    <button
      style={tabStyle}
      onClick={() => !item.disabled && onSelect(item.key)}
      onMouseEnter={(e) => {
        if (!item.disabled && !isActive) {
          (e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.9)'
          if (variant !== 'line') {
            (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
          }
        }
      }}
      onMouseLeave={(e) => {
        if (!item.disabled && !isActive) {
          (e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.6)'
          if (variant !== 'line') {
            (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent'
          }
        }
      }}
    >
      {item.icon && <span style={{ display: 'flex' }}>{item.icon}</span>}
      <span>{item.label}</span>
      {item.closable && onClose && (
        <span
          style={{
            display: 'flex',
            marginLeft: '4px',
            padding: '2px',
            borderRadius: '4px',
            opacity: 0.6,
          }}
          onClick={(e) => {
            e.stopPropagation()
            onClose(item.key)
          }}
          onMouseEnter={(e) => {
            const el = e.currentTarget as HTMLElement
            el.style.opacity = '1'
            el.style.backgroundColor = 'rgba(255, 255, 255, 0.1)'
          }}
          onMouseLeave={(e) => {
            const el = e.currentTarget as HTMLElement
            el.style.opacity = '0.6'
            el.style.backgroundColor = 'transparent'
          }}
        >
          <CloseIcon />
        </span>
      )}
    </button>
  )
}

function AddButton({ size, onClick }: { size: 'sm' | 'md' | 'lg'; onClick?: () => void }) {
  const sizes = sizeStyles[size]

  const buttonStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: sizes.padding,
    color: 'rgba(255, 255, 255, 0.5)',
    cursor: 'pointer',
    borderRadius: '8px',
    transition: 'all 0.15s',
    border: 'none',
    background: 'none',
  }

  return (
    <button
      style={buttonStyle}
      onClick={onClick}
      onMouseEnter={(e) => {
        const el = e.currentTarget as HTMLElement
        el.style.color = 'rgba(255, 255, 255, 0.9)'
        el.style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget as HTMLElement
        el.style.color = 'rgba(255, 255, 255, 0.5)'
        el.style.backgroundColor = 'transparent'
      }}
    >
      <PlusIcon />
    </button>
  )
}

export interface TabProps {
  children?: ReactNode
  tabKey: string
  label: ReactNode
  icon?: ReactNode
  disabled?: boolean
  closable?: boolean
}

export function Tab({ tabKey, label, icon, disabled, closable }: TabProps) {
  const { activeKey, variant, size, onSelect, onClose } = useContext(TabsContext)
  const isActive = activeKey === tabKey
  const sizes = sizeStyles[size]

  const baseStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: sizes.gap,
    padding: sizes.padding,
    fontSize: sizes.fontSize,
    fontWeight: 500,
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.15s',
    whiteSpace: 'nowrap',
    border: 'none',
    background: 'none',
    color: isActive ? '#a78bfa' : 'rgba(255, 255, 255, 0.6)',
    marginBottom: '-1px',
    borderBottom: isActive ? '2px solid #a78bfa' : '2px solid transparent',
  }

  if (variant === 'card') {
    baseStyle.color = isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.6)'
    baseStyle.backgroundColor = isActive ? '#1e1e2e' : 'transparent'
    baseStyle.borderRadius = '8px'
    baseStyle.borderBottom = 'none'
    baseStyle.marginBottom = '0'
  } else if (variant === 'pill') {
    baseStyle.color = isActive ? '#ffffff' : 'rgba(255, 255, 255, 0.6)'
    baseStyle.backgroundColor = isActive ? '#7c3aed' : 'transparent'
    baseStyle.borderRadius = '8px'
    baseStyle.borderBottom = 'none'
    baseStyle.marginBottom = '0'
  }

  return (
    <button style={baseStyle} onClick={() => !disabled && onSelect(tabKey)}>
      {icon && <span style={{ display: 'flex' }}>{icon}</span>}
      <span>{label}</span>
      {closable && onClose && (
        <span
          style={{ display: 'flex', marginLeft: '4px', opacity: 0.6 }}
          onClick={(e) => { e.stopPropagation(); onClose(tabKey) }}
        >
          <CloseIcon />
        </span>
      )}
    </button>
  )
}

function CloseIcon() {
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
      <path d="M3 3L9 9M9 3L3 9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

function PlusIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
      <path d="M7 3V11M3 7H11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

Tabs.Tab = Tab
