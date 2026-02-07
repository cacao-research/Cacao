import { ReactNode } from 'react'
import { Box, BoxProps } from './Box'

export interface ContainerProps extends BoxProps {
  children?: ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  center?: boolean
}

const sizeMap = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  full: '100%',
}

export function Container({
  children,
  size = 'lg',
  center = true,
  px = 4,
  ...rest
}: ContainerProps) {
  return (
    <Box
      maxWidth={sizeMap[size]}
      width="100%"
      mx={center ? 'auto' : undefined}
      px={px}
      {...rest}
    >
      {children}
    </Box>
  )
}
