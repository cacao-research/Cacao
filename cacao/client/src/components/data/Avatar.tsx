import { CSSProperties, ReactNode } from 'react'

export type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | number
export type AvatarShape = 'circle' | 'square'

export interface AvatarProps {
  src?: string
  alt?: string
  name?: string
  size?: AvatarSize
  shape?: AvatarShape
  icon?: ReactNode
  color?: string
  bordered?: boolean
  className?: string
  style?: CSSProperties
  onClick?: () => void
}

const sizeMap: Record<Exclude<AvatarSize, number>, number> = {
  xs: 24,
  sm: 32,
  md: 40,
  lg: 48,
  xl: 64,
}

const fontSizeMap: Record<Exclude<AvatarSize, number>, number> = {
  xs: 10,
  sm: 12,
  md: 14,
  lg: 18,
  xl: 24,
}

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) {
    return parts[0].charAt(0).toUpperCase()
  }
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase()
}

function stringToColor(str: string): string {
  const colors = [
    '#7c3aed', '#8b5cf6', '#a78bfa', // Purple
    '#3b82f6', '#60a5fa', // Blue
    '#10b981', '#34d399', // Green
    '#f59e0b', '#fbbf24', // Yellow
    '#ef4444', '#f87171', // Red
    '#ec4899', '#f472b6', // Pink
  ]

  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length]
}

export function Avatar({
  src,
  alt,
  name,
  size = 'md',
  shape = 'circle',
  icon,
  color,
  bordered = false,
  className,
  style,
  onClick,
}: AvatarProps) {
  const pixelSize = typeof size === 'number' ? size : sizeMap[size]
  const fontSize = typeof size === 'number' ? size * 0.4 : fontSizeMap[size]
  const bgColor = color ?? (name ? stringToColor(name) : '#4b5563')

  const avatarStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: `${pixelSize}px`,
    height: `${pixelSize}px`,
    borderRadius: shape === 'circle' ? '50%' : '8px',
    backgroundColor: src ? 'transparent' : bgColor,
    color: '#ffffff',
    fontSize: `${fontSize}px`,
    fontWeight: 600,
    overflow: 'hidden',
    flexShrink: 0,
    border: bordered ? '2px solid rgba(255, 255, 255, 0.2)' : 'none',
    cursor: onClick ? 'pointer' : undefined,
    transition: 'transform 0.15s',
    ...style,
  }

  const imgStyle: CSSProperties = {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  }

  return (
    <div
      className={className}
      style={avatarStyle}
      onClick={onClick}
      onMouseEnter={(e) => {
        if (onClick) {
          (e.currentTarget as HTMLElement).style.transform = 'scale(1.05)'
        }
      }}
      onMouseLeave={(e) => {
        if (onClick) {
          (e.currentTarget as HTMLElement).style.transform = 'scale(1)'
        }
      }}
    >
      {src ? (
        <img src={src} alt={alt ?? name ?? 'Avatar'} style={imgStyle} />
      ) : icon ? (
        icon
      ) : name ? (
        getInitials(name)
      ) : (
        <DefaultUserIcon size={pixelSize * 0.6} />
      )}
    </div>
  )
}

function DefaultUserIcon({ size }: { size: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" />
    </svg>
  )
}

export interface AvatarGroupProps {
  children?: ReactNode
  max?: number
  size?: AvatarSize
  spacing?: number
  className?: string
  style?: CSSProperties
}

export function AvatarGroup({
  children,
  max,
  size = 'md',
  spacing = -8,
  className,
  style,
}: AvatarGroupProps) {
  const childArray = Array.isArray(children) ? children : [children]
  const visibleChildren = max ? childArray.slice(0, max) : childArray
  const remaining = max ? childArray.length - max : 0

  const groupStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    ...style,
  }

  const itemStyle: CSSProperties = {
    marginLeft: `${spacing}px`,
    border: '2px solid #1e1e2e',
    borderRadius: '50%',
  }

  return (
    <div className={className} style={groupStyle}>
      {visibleChildren.map((child, index) => (
        <div key={index} style={index === 0 ? {} : itemStyle}>
          {child}
        </div>
      ))}
      {remaining > 0 && (
        <div style={itemStyle}>
          <Avatar size={size} name={`+${remaining}`} color="#4b5563" />
        </div>
      )}
    </div>
  )
}
