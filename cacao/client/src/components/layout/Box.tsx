import { CSSProperties, ReactNode, forwardRef } from 'react'

export interface BoxProps {
  children?: ReactNode
  as?: keyof JSX.IntrinsicElements
  className?: string
  style?: CSSProperties

  // Spacing
  p?: number | string
  px?: number | string
  py?: number | string
  pt?: number | string
  pr?: number | string
  pb?: number | string
  pl?: number | string
  m?: number | string
  mx?: number | string
  my?: number | string
  mt?: number | string
  mr?: number | string
  mb?: number | string
  ml?: number | string
  gap?: number | string

  // Flexbox
  display?: CSSProperties['display']
  flex?: CSSProperties['flex']
  flexDirection?: CSSProperties['flexDirection']
  alignItems?: CSSProperties['alignItems']
  justifyContent?: CSSProperties['justifyContent']
  flexWrap?: CSSProperties['flexWrap']

  // Sizing
  width?: CSSProperties['width']
  height?: CSSProperties['height']
  minWidth?: CSSProperties['minWidth']
  minHeight?: CSSProperties['minHeight']
  maxWidth?: CSSProperties['maxWidth']
  maxHeight?: CSSProperties['maxHeight']

  // Other
  bg?: string
  color?: string
  borderRadius?: number | string
  border?: string
  shadow?: string
  overflow?: CSSProperties['overflow']
  position?: CSSProperties['position']
  onClick?: () => void
}

function toSpacing(value: number | string | undefined): string | undefined {
  if (value === undefined) return undefined
  if (typeof value === 'number') return `${value * 4}px`
  return value
}

export const Box = forwardRef<HTMLElement, BoxProps>(
  (
    {
      children,
      as: Component = 'div',
      className,
      style,
      p,
      px,
      py,
      pt,
      pr,
      pb,
      pl,
      m,
      mx,
      my,
      mt,
      mr,
      mb,
      ml,
      gap,
      display,
      flex,
      flexDirection,
      alignItems,
      justifyContent,
      flexWrap,
      width,
      height,
      minWidth,
      minHeight,
      maxWidth,
      maxHeight,
      bg,
      color,
      borderRadius,
      border,
      shadow,
      overflow,
      position,
      onClick,
      ...rest
    },
    ref
  ) => {
    const computedStyle: CSSProperties = {
      // Padding
      padding: toSpacing(p),
      paddingLeft: toSpacing(px ?? pl),
      paddingRight: toSpacing(px ?? pr),
      paddingTop: toSpacing(py ?? pt),
      paddingBottom: toSpacing(py ?? pb),

      // Margin
      margin: toSpacing(m),
      marginLeft: toSpacing(mx ?? ml),
      marginRight: toSpacing(mx ?? mr),
      marginTop: toSpacing(my ?? mt),
      marginBottom: toSpacing(my ?? mb),

      // Gap
      gap: toSpacing(gap),

      // Flexbox
      display,
      flex,
      flexDirection,
      alignItems,
      justifyContent,
      flexWrap,

      // Sizing
      width,
      height,
      minWidth,
      minHeight,
      maxWidth,
      maxHeight,

      // Other
      backgroundColor: bg,
      color,
      borderRadius: typeof borderRadius === 'number' ? `${borderRadius}px` : borderRadius,
      border,
      boxShadow: shadow,
      overflow,
      position,

      // Merge with style prop
      ...style,
    }

    // Filter out undefined values
    const cleanStyle = Object.fromEntries(
      Object.entries(computedStyle).filter(([, v]) => v !== undefined)
    ) as CSSProperties

    return (
      <Component
        ref={ref as any}
        className={className}
        style={cleanStyle}
        onClick={onClick}
        {...rest}
      >
        {children}
      </Component>
    )
  }
)

Box.displayName = 'Box'
