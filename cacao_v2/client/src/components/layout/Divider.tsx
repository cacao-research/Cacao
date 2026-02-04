import { CSSProperties } from 'react'

export interface DividerProps {
  orientation?: 'horizontal' | 'vertical'
  color?: string
  thickness?: number | string
  spacing?: number
  className?: string
  style?: CSSProperties
}

export function Divider({
  orientation = 'horizontal',
  color = 'rgba(255, 255, 255, 0.1)',
  thickness = 1,
  spacing = 0,
  className,
  style,
}: DividerProps) {
  const isHorizontal = orientation === 'horizontal'
  const thicknessValue = typeof thickness === 'number' ? `${thickness}px` : thickness
  const spacingValue = spacing * 4

  const dividerStyle: CSSProperties = {
    backgroundColor: color,
    border: 'none',
    ...(isHorizontal
      ? {
          width: '100%',
          height: thicknessValue,
          marginTop: `${spacingValue}px`,
          marginBottom: `${spacingValue}px`,
        }
      : {
          width: thicknessValue,
          height: '100%',
          minHeight: '1em',
          marginLeft: `${spacingValue}px`,
          marginRight: `${spacingValue}px`,
          alignSelf: 'stretch',
        }),
    ...style,
  }

  return <div className={className} style={dividerStyle} role="separator" />
}
