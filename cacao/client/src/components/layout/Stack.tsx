import { CSSProperties, ReactNode } from 'react'
import { Box, BoxProps } from './Box'

export interface StackProps extends Omit<BoxProps, 'flexDirection'> {
  children?: ReactNode
  direction?: 'row' | 'column'
  spacing?: number | string
  align?: CSSProperties['alignItems']
  justify?: CSSProperties['justifyContent']
  wrap?: boolean
  divider?: ReactNode
}

export function Stack({
  children,
  direction = 'column',
  spacing = 2,
  align,
  justify,
  wrap = false,
  divider,
  ...rest
}: StackProps) {
  // If divider is provided, intersperse it between children
  let content = children
  if (divider) {
    const childArray = Array.isArray(children) ? children : [children]
    content = childArray.reduce<ReactNode[]>((acc, child, index) => {
      if (index > 0) {
        acc.push(
          <div key={`divider-${index}`} style={{ flexShrink: 0 }}>
            {divider}
          </div>
        )
      }
      acc.push(child)
      return acc
    }, [])
  }

  return (
    <Box
      display="flex"
      flexDirection={direction}
      gap={spacing}
      alignItems={align}
      justifyContent={justify}
      flexWrap={wrap ? 'wrap' : 'nowrap'}
      {...rest}
    >
      {content}
    </Box>
  )
}

export function HStack(props: Omit<StackProps, 'direction'>) {
  return <Stack direction="row" {...props} />
}

export function VStack(props: Omit<StackProps, 'direction'>) {
  return <Stack direction="column" {...props} />
}
