/**
 * Loading state components for Cacao v2.
 *
 * Provides various loading indicators and skeleton components.
 */

import { CSSProperties, ReactNode } from 'react'

export interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg' | number
  color?: string
  thickness?: number
  className?: string
  style?: CSSProperties
}

const spinnerSizes = {
  sm: 16,
  md: 24,
  lg: 40,
}

/**
 * Circular loading spinner.
 */
export function Spinner({
  size = 'md',
  color = '#a78bfa',
  thickness = 3,
  className,
  style,
}: SpinnerProps) {
  const pixelSize = typeof size === 'number' ? size : spinnerSizes[size]

  const containerStyle: CSSProperties = {
    display: 'inline-flex',
    width: pixelSize,
    height: pixelSize,
    ...style,
  }

  return (
    <div className={className} style={containerStyle}>
      <svg
        width={pixelSize}
        height={pixelSize}
        viewBox="0 0 24 24"
        fill="none"
        style={{ animation: 'cacao-spin 1s linear infinite' }}
      >
        <style>
          {`@keyframes cacao-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}
        </style>
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke={color}
          strokeWidth={thickness}
          strokeOpacity={0.25}
        />
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke={color}
          strokeWidth={thickness}
          strokeLinecap="round"
          strokeDasharray="31.4 31.4"
          style={{ transform: 'rotate(-90deg)', transformOrigin: 'center' }}
        />
      </svg>
    </div>
  )
}

export interface DotsLoaderProps {
  size?: 'sm' | 'md' | 'lg'
  color?: string
  className?: string
  style?: CSSProperties
}

const dotSizes = {
  sm: 6,
  md: 8,
  lg: 12,
}

/**
 * Animated dots loader.
 */
export function DotsLoader({
  size = 'md',
  color = '#a78bfa',
  className,
  style,
}: DotsLoaderProps) {
  const dotSize = dotSizes[size]
  const gap = dotSize / 2

  const containerStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: `${gap}px`,
    ...style,
  }

  const dotStyle: CSSProperties = {
    width: dotSize,
    height: dotSize,
    borderRadius: '50%',
    backgroundColor: color,
  }

  return (
    <div className={className} style={containerStyle}>
      <style>
        {`
          @keyframes cacao-bounce {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
          }
        `}
      </style>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            ...dotStyle,
            animation: `cacao-bounce 1.4s ease-in-out ${i * 0.16}s infinite`,
          }}
        />
      ))}
    </div>
  )
}

export interface SkeletonProps {
  width?: string | number
  height?: string | number
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded'
  animation?: 'pulse' | 'wave' | 'none'
  className?: string
  style?: CSSProperties
}

/**
 * Skeleton placeholder for loading content.
 */
export function Skeleton({
  width = '100%',
  height = '1em',
  variant = 'text',
  animation = 'pulse',
  className,
  style,
}: SkeletonProps) {
  const borderRadius = variant === 'circular'
    ? '50%'
    : variant === 'rounded'
    ? '8px'
    : variant === 'text'
    ? '4px'
    : '0'

  const baseStyle: CSSProperties = {
    display: 'block',
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
    borderRadius,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    ...style,
  }

  if (animation === 'pulse') {
    return (
      <>
        <style>
          {`@keyframes cacao-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }`}
        </style>
        <span
          className={className}
          style={{ ...baseStyle, animation: 'cacao-pulse 1.5s ease-in-out infinite' }}
        />
      </>
    )
  }

  if (animation === 'wave') {
    return (
      <>
        <style>
          {`
            @keyframes cacao-wave {
              0% { transform: translateX(-100%); }
              50%, 100% { transform: translateX(100%); }
            }
          `}
        </style>
        <span
          className={className}
          style={{ ...baseStyle, position: 'relative', overflow: 'hidden' }}
        >
          <span
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent)',
              animation: 'cacao-wave 1.5s ease-in-out infinite',
            }}
          />
        </span>
      </>
    )
  }

  return <span className={className} style={baseStyle} />
}

export interface SkeletonTextProps {
  lines?: number
  lastLineWidth?: string
  lineHeight?: number
  gap?: number
  animation?: 'pulse' | 'wave' | 'none'
  className?: string
  style?: CSSProperties
}

/**
 * Multi-line skeleton text placeholder.
 */
export function SkeletonText({
  lines = 3,
  lastLineWidth = '60%',
  lineHeight = 16,
  gap = 8,
  animation = 'pulse',
  className,
  style,
}: SkeletonTextProps) {
  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: `${gap}px`,
    ...style,
  }

  return (
    <div className={className} style={containerStyle}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          width={i === lines - 1 ? lastLineWidth : '100%'}
          height={lineHeight}
          variant="text"
          animation={animation}
        />
      ))}
    </div>
  )
}

export interface LoadingOverlayProps {
  visible?: boolean
  children?: ReactNode
  blur?: boolean
  spinner?: ReactNode
  text?: string
  className?: string
  style?: CSSProperties
}

/**
 * Full-screen or container loading overlay.
 */
export function LoadingOverlay({
  visible = true,
  children,
  blur = true,
  spinner,
  text,
  className,
  style,
}: LoadingOverlayProps) {
  if (!visible) return <>{children}</>

  const containerStyle: CSSProperties = {
    position: 'relative',
    ...style,
  }

  const overlayStyle: CSSProperties = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '12px',
    backgroundColor: 'rgba(30, 30, 46, 0.8)',
    backdropFilter: blur ? 'blur(4px)' : undefined,
    zIndex: 10,
    borderRadius: 'inherit',
  }

  const textStyle: CSSProperties = {
    fontSize: '0.875rem',
    color: 'rgba(255, 255, 255, 0.7)',
    fontWeight: 500,
  }

  return (
    <div className={className} style={containerStyle}>
      {children}
      <div style={overlayStyle}>
        {spinner ?? <Spinner size="lg" />}
        {text && <span style={textStyle}>{text}</span>}
      </div>
    </div>
  )
}

export interface LoadingProps {
  loading?: boolean
  children?: ReactNode
  fallback?: ReactNode
}

/**
 * Conditional loading wrapper.
 *
 * @example
 * <Loading loading={isLoading}>
 *   <Content />
 * </Loading>
 */
export function Loading({
  loading = false,
  children,
  fallback,
}: LoadingProps) {
  if (loading) {
    return <>{fallback ?? <Spinner />}</>
  }

  return <>{children}</>
}

export interface EmptyStateProps {
  icon?: ReactNode
  title?: string
  description?: string
  action?: ReactNode
  className?: string
  style?: CSSProperties
}

/**
 * Empty state placeholder.
 */
export function EmptyState({
  icon,
  title = 'No data',
  description,
  action,
  className,
  style,
}: EmptyStateProps) {
  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px',
    textAlign: 'center',
    ...style,
  }

  const iconContainerStyle: CSSProperties = {
    width: '64px',
    height: '64px',
    marginBottom: '16px',
    color: 'rgba(255, 255, 255, 0.3)',
  }

  const titleStyle: CSSProperties = {
    fontSize: '1.125rem',
    fontWeight: 600,
    color: 'rgba(255, 255, 255, 0.8)',
    marginBottom: '8px',
  }

  const descriptionStyle: CSSProperties = {
    fontSize: '0.875rem',
    color: 'rgba(255, 255, 255, 0.5)',
    marginBottom: action ? '16px' : 0,
    maxWidth: '300px',
  }

  return (
    <div className={className} style={containerStyle}>
      <div style={iconContainerStyle}>
        {icon ?? <DefaultEmptyIcon />}
      </div>
      <div style={titleStyle}>{title}</div>
      {description && <div style={descriptionStyle}>{description}</div>}
      {action}
    </div>
  )
}

function DefaultEmptyIcon() {
  return (
    <svg width="100%" height="100%" viewBox="0 0 64 64" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="8" y="16" width="48" height="40" rx="4" />
      <path d="M8 28h48" />
      <circle cx="16" cy="22" r="2" fill="currentColor" />
      <circle cx="24" cy="22" r="2" fill="currentColor" />
      <circle cx="32" cy="22" r="2" fill="currentColor" />
      <path d="M24 44l8-8 8 8" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M32 36v16" strokeLinecap="round" />
    </svg>
  )
}
