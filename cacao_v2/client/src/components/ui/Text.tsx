import { CSSProperties, ReactNode } from 'react'

export type TextVariant = 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body' | 'small' | 'caption' | 'code'

export interface TextProps {
  children?: ReactNode
  variant?: TextVariant
  as?: keyof JSX.IntrinsicElements
  color?: string
  weight?: CSSProperties['fontWeight']
  align?: CSSProperties['textAlign']
  truncate?: boolean
  lines?: number
  className?: string
  style?: CSSProperties
}

const variantStyles: Record<TextVariant, { element: keyof JSX.IntrinsicElements; style: CSSProperties }> = {
  h1: {
    element: 'h1',
    style: { fontSize: '2.5rem', fontWeight: 700, lineHeight: 1.2, margin: '0 0 0.5em' },
  },
  h2: {
    element: 'h2',
    style: { fontSize: '2rem', fontWeight: 700, lineHeight: 1.25, margin: '0 0 0.5em' },
  },
  h3: {
    element: 'h3',
    style: { fontSize: '1.5rem', fontWeight: 600, lineHeight: 1.3, margin: '0 0 0.5em' },
  },
  h4: {
    element: 'h4',
    style: { fontSize: '1.25rem', fontWeight: 600, lineHeight: 1.4, margin: '0 0 0.5em' },
  },
  h5: {
    element: 'h5',
    style: { fontSize: '1rem', fontWeight: 600, lineHeight: 1.5, margin: '0 0 0.5em' },
  },
  h6: {
    element: 'h6',
    style: { fontSize: '0.875rem', fontWeight: 600, lineHeight: 1.5, margin: '0 0 0.5em' },
  },
  body: {
    element: 'p',
    style: { fontSize: '1rem', fontWeight: 400, lineHeight: 1.6, margin: 0 },
  },
  small: {
    element: 'span',
    style: { fontSize: '0.875rem', fontWeight: 400, lineHeight: 1.5 },
  },
  caption: {
    element: 'span',
    style: { fontSize: '0.75rem', fontWeight: 400, lineHeight: 1.4, opacity: 0.7 },
  },
  code: {
    element: 'code',
    style: {
      fontSize: '0.875rem',
      fontFamily: 'monospace',
      backgroundColor: 'rgba(255, 255, 255, 0.1)',
      padding: '2px 6px',
      borderRadius: '4px',
    },
  },
}

export function Text({
  children,
  variant = 'body',
  as,
  color,
  weight,
  align,
  truncate = false,
  lines,
  className,
  style,
}: TextProps) {
  const { element: defaultElement, style: variantStyle } = variantStyles[variant]
  const Component = as ?? defaultElement

  const textStyle: CSSProperties = {
    ...variantStyle,
    color,
    fontWeight: weight,
    textAlign: align,
    ...(truncate && {
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap',
    }),
    ...(lines && {
      display: '-webkit-box',
      WebkitLineClamp: lines,
      WebkitBoxOrient: 'vertical',
      overflow: 'hidden',
    }),
    ...style,
  }

  return (
    <Component className={className} style={textStyle}>
      {children}
    </Component>
  )
}
