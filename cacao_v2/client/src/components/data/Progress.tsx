import { CSSProperties, ReactNode } from 'react'

export type ProgressType = 'line' | 'circle'
export type ProgressStatus = 'normal' | 'success' | 'warning' | 'danger'

export interface ProgressProps {
  value: number
  max?: number
  type?: ProgressType
  size?: 'sm' | 'md' | 'lg' | number
  status?: ProgressStatus
  showValue?: boolean
  format?: (value: number, max: number) => ReactNode
  strokeWidth?: number
  strokeColor?: string
  trailColor?: string
  animated?: boolean
  striped?: boolean
  className?: string
  style?: CSSProperties
}

const statusColors: Record<ProgressStatus, string> = {
  normal: '#7c3aed',
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
}

const sizeMap = {
  sm: { height: 6, fontSize: '0.75rem', circleSize: 80 },
  md: { height: 8, fontSize: '0.875rem', circleSize: 120 },
  lg: { height: 12, fontSize: '1rem', circleSize: 160 },
}

export function Progress({
  value,
  max = 100,
  type = 'line',
  size = 'md',
  status = 'normal',
  showValue = true,
  format,
  strokeWidth,
  strokeColor,
  trailColor = 'rgba(255, 255, 255, 0.1)',
  animated = false,
  striped = false,
  className,
  style,
}: ProgressProps) {
  const percent = Math.min(Math.max((value / max) * 100, 0), 100)
  const color = strokeColor ?? statusColors[status]

  const sizeConfig = typeof size === 'number'
    ? { height: size, fontSize: '0.875rem', circleSize: size }
    : sizeMap[size]

  const displayValue = format
    ? format(value, max)
    : `${Math.round(percent)}%`

  if (type === 'circle') {
    return (
      <CircleProgress
        percent={percent}
        size={sizeConfig.circleSize}
        strokeWidth={strokeWidth ?? (sizeConfig.circleSize / 10)}
        strokeColor={color}
        trailColor={trailColor}
        showValue={showValue}
        displayValue={displayValue}
        fontSize={sizeConfig.fontSize}
        className={className}
        style={style}
      />
    )
  }

  return (
    <LineProgress
      percent={percent}
      height={sizeConfig.height}
      strokeColor={color}
      trailColor={trailColor}
      showValue={showValue}
      displayValue={displayValue}
      fontSize={sizeConfig.fontSize}
      animated={animated}
      striped={striped}
      className={className}
      style={style}
    />
  )
}

interface LineProgressProps {
  percent: number
  height: number
  strokeColor: string
  trailColor: string
  showValue: boolean
  displayValue: ReactNode
  fontSize: string
  animated: boolean
  striped: boolean
  className?: string
  style?: CSSProperties
}

function LineProgress({
  percent,
  height,
  strokeColor,
  trailColor,
  showValue,
  displayValue,
  fontSize,
  animated,
  striped,
  className,
  style,
}: LineProgressProps) {
  const containerStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    ...style,
  }

  const trackStyle: CSSProperties = {
    flex: 1,
    height: `${height}px`,
    backgroundColor: trailColor,
    borderRadius: `${height / 2}px`,
    overflow: 'hidden',
  }

  const barStyle: CSSProperties = {
    width: `${percent}%`,
    height: '100%',
    backgroundColor: strokeColor,
    borderRadius: `${height / 2}px`,
    transition: 'width 0.3s ease',
    backgroundImage: striped
      ? `linear-gradient(45deg, rgba(255,255,255,0.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0.15) 75%, transparent 75%, transparent)`
      : undefined,
    backgroundSize: striped ? `${height * 2}px ${height * 2}px` : undefined,
    animation: animated && striped ? 'progress-stripes 1s linear infinite' : undefined,
  }

  const valueStyle: CSSProperties = {
    fontSize,
    fontWeight: 500,
    color: 'rgba(255, 255, 255, 0.8)',
    minWidth: '40px',
    textAlign: 'right',
  }

  return (
    <div className={className} style={containerStyle}>
      {striped && animated && (
        <style>
          {`@keyframes progress-stripes { from { background-position: 0 0; } to { background-position: ${height * 2}px 0; } }`}
        </style>
      )}
      <div style={trackStyle}>
        <div style={barStyle} />
      </div>
      {showValue && <div style={valueStyle}>{displayValue}</div>}
    </div>
  )
}

interface CircleProgressProps {
  percent: number
  size: number
  strokeWidth: number
  strokeColor: string
  trailColor: string
  showValue: boolean
  displayValue: ReactNode
  fontSize: string
  className?: string
  style?: CSSProperties
}

function CircleProgress({
  percent,
  size,
  strokeWidth,
  strokeColor,
  trailColor,
  showValue,
  displayValue,
  fontSize,
  className,
  style,
}: CircleProgressProps) {
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (percent / 100) * circumference

  const containerStyle: CSSProperties = {
    position: 'relative',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: size,
    height: size,
    ...style,
  }

  const valueStyle: CSSProperties = {
    position: 'absolute',
    fontSize,
    fontWeight: 600,
    color: 'rgba(255, 255, 255, 0.9)',
  }

  return (
    <div className={className} style={containerStyle}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={trailColor}
          strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          style={{ transition: 'stroke-dashoffset 0.3s ease' }}
        />
      </svg>
      {showValue && <div style={valueStyle}>{displayValue}</div>}
    </div>
  )
}
