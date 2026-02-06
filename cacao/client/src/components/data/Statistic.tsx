import { CSSProperties, ReactNode } from 'react'

export interface StatisticProps {
  title: ReactNode
  value: ReactNode
  prefix?: ReactNode
  suffix?: ReactNode
  precision?: number
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: ReactNode
  description?: ReactNode
  loading?: boolean
  size?: 'sm' | 'md' | 'lg'
  className?: string
  style?: CSSProperties
}

const sizeStyles = {
  sm: { titleSize: '0.75rem', valueSize: '1.5rem', trendSize: '0.75rem' },
  md: { titleSize: '0.875rem', valueSize: '2rem', trendSize: '0.875rem' },
  lg: { titleSize: '1rem', valueSize: '2.5rem', trendSize: '1rem' },
}

const trendColors = {
  up: '#10b981',
  down: '#ef4444',
  neutral: 'rgba(255, 255, 255, 0.5)',
}

export function Statistic({
  title,
  value,
  prefix,
  suffix,
  precision,
  trend,
  trendValue,
  description,
  loading = false,
  size = 'md',
  className,
  style,
}: StatisticProps) {
  const sizes = sizeStyles[size]

  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
    ...style,
  }

  const titleStyle: CSSProperties = {
    fontSize: sizes.titleSize,
    fontWeight: 500,
    color: 'rgba(255, 255, 255, 0.5)',
    textTransform: 'uppercase',
    letterSpacing: '0.03em',
  }

  const valueContainerStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'baseline',
    gap: '4px',
  }

  const valueStyle: CSSProperties = {
    fontSize: sizes.valueSize,
    fontWeight: 700,
    color: 'rgba(255, 255, 255, 0.95)',
    lineHeight: 1.2,
    fontVariantNumeric: 'tabular-nums',
  }

  const affixStyle: CSSProperties = {
    fontSize: `calc(${sizes.valueSize} * 0.6)`,
    fontWeight: 500,
    color: 'rgba(255, 255, 255, 0.6)',
  }

  const trendStyle: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    fontSize: sizes.trendSize,
    fontWeight: 500,
    color: trend ? trendColors[trend] : 'rgba(255, 255, 255, 0.5)',
  }

  const descriptionStyle: CSSProperties = {
    fontSize: `calc(${sizes.titleSize} * 0.9)`,
    color: 'rgba(255, 255, 255, 0.4)',
    marginTop: '2px',
  }

  const formatValue = (val: ReactNode): ReactNode => {
    if (typeof val === 'number' && precision !== undefined) {
      return val.toFixed(precision)
    }
    return val
  }

  if (loading) {
    return (
      <div className={className} style={containerStyle}>
        <div style={titleStyle}>{title}</div>
        <div style={valueContainerStyle}>
          <div
            style={{
              ...valueStyle,
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '4px',
              width: '80px',
              height: sizes.valueSize,
              animation: 'pulse 1.5s infinite',
            }}
          />
          <style>
            {`@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }`}
          </style>
        </div>
      </div>
    )
  }

  return (
    <div className={className} style={containerStyle}>
      <div style={titleStyle}>{title}</div>

      <div style={valueContainerStyle}>
        {prefix && <span style={affixStyle}>{prefix}</span>}
        <span style={valueStyle}>{formatValue(value)}</span>
        {suffix && <span style={affixStyle}>{suffix}</span>}
      </div>

      {(trend || trendValue) && (
        <div style={trendStyle}>
          {trend && <TrendIcon direction={trend} />}
          {trendValue}
        </div>
      )}

      {description && <div style={descriptionStyle}>{description}</div>}
    </div>
  )
}

function TrendIcon({ direction }: { direction: 'up' | 'down' | 'neutral' }) {
  if (direction === 'up') {
    return (
      <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor">
        <path d="M7 3L12 9H2L7 3Z" />
      </svg>
    )
  }
  if (direction === 'down') {
    return (
      <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor">
        <path d="M7 11L2 5H12L7 11Z" />
      </svg>
    )
  }
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor">
      <rect x="2" y="6" width="10" height="2" rx="1" />
    </svg>
  )
}

export interface StatisticGroupProps {
  children?: ReactNode
  columns?: number
  gap?: number
  className?: string
  style?: CSSProperties
}

export function StatisticGroup({
  children,
  columns = 4,
  gap = 24,
  className,
  style,
}: StatisticGroupProps) {
  const groupStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, 1fr)`,
    gap: `${gap}px`,
    ...style,
  }

  return (
    <div className={className} style={groupStyle}>
      {children}
    </div>
  )
}
