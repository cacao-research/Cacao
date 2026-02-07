import { CSSProperties, ReactNode } from 'react'

export interface NavbarProps {
  children?: ReactNode
  logo?: ReactNode
  brand?: ReactNode
  fixed?: boolean
  bordered?: boolean
  transparent?: boolean
  height?: number
  className?: string
  style?: CSSProperties
}

export function Navbar({
  children,
  logo,
  brand,
  fixed = false,
  bordered = true,
  transparent = false,
  height = 64,
  className,
  style,
}: NavbarProps) {
  const navStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: `${height}px`,
    padding: '0 24px',
    backgroundColor: transparent ? 'transparent' : '#1e1e2e',
    borderBottom: bordered ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    position: fixed ? 'fixed' : 'relative',
    top: fixed ? 0 : undefined,
    left: fixed ? 0 : undefined,
    right: fixed ? 0 : undefined,
    zIndex: fixed ? 1000 : undefined,
    backdropFilter: transparent ? 'blur(12px)' : undefined,
    ...style,
  }

  const brandStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  }

  const logoStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
  }

  const brandTextStyle: CSSProperties = {
    fontSize: '1.25rem',
    fontWeight: 700,
    color: '#ffffff',
    letterSpacing: '-0.02em',
  }

  return (
    <nav className={className} style={navStyle}>
      <div style={brandStyle}>
        {logo && <div style={logoStyle}>{logo}</div>}
        {brand && (
          typeof brand === 'string'
            ? <span style={brandTextStyle}>{brand}</span>
            : brand
        )}
      </div>
      {children}
    </nav>
  )
}

export interface NavbarSectionProps {
  children?: ReactNode
  align?: 'left' | 'center' | 'right'
  gap?: number
  className?: string
  style?: CSSProperties
}

export function NavbarSection({
  children,
  align = 'left',
  gap = 8,
  className,
  style,
}: NavbarSectionProps) {
  const sectionStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: `${gap}px`,
    marginLeft: align === 'right' ? 'auto' : align === 'center' ? 'auto' : undefined,
    marginRight: align === 'center' ? 'auto' : undefined,
    ...style,
  }

  return (
    <div className={className} style={sectionStyle}>
      {children}
    </div>
  )
}

export interface NavbarItemProps {
  children?: ReactNode
  active?: boolean
  disabled?: boolean
  icon?: ReactNode
  onClick?: () => void
  className?: string
  style?: CSSProperties
}

export function NavbarItem({
  children,
  active = false,
  disabled = false,
  icon,
  onClick,
  className,
  style,
}: NavbarItemProps) {
  const itemStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    padding: '8px 12px',
    fontSize: '0.875rem',
    fontWeight: 500,
    color: active ? '#a78bfa' : 'rgba(255, 255, 255, 0.7)',
    backgroundColor: active ? 'rgba(167, 139, 250, 0.1)' : 'transparent',
    borderRadius: '8px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.15s',
    ...style,
  }

  return (
    <div
      className={className}
      style={itemStyle}
      onClick={disabled ? undefined : onClick}
      onMouseEnter={(e) => {
        if (!disabled && !active) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
          ;(e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.9)'
        }
      }}
      onMouseLeave={(e) => {
        if (!disabled && !active) {
          (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent'
          ;(e.currentTarget as HTMLElement).style.color = 'rgba(255, 255, 255, 0.7)'
        }
      }}
    >
      {icon && <span style={{ display: 'flex' }}>{icon}</span>}
      {children}
    </div>
  )
}

Navbar.Section = NavbarSection
Navbar.Item = NavbarItem
