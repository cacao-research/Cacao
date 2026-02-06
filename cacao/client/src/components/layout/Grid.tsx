import { CSSProperties, ReactNode } from 'react'
import { Box, BoxProps } from './Box'

export interface GridProps extends Omit<BoxProps, 'display'> {
  children?: ReactNode
  columns?: number | string
  rows?: number | string
  spacing?: number | string
  columnSpacing?: number | string
  rowSpacing?: number | string
  templateColumns?: string
  templateRows?: string
  autoFlow?: CSSProperties['gridAutoFlow']
  autoColumns?: string
  autoRows?: string
  areas?: string
  placeItems?: CSSProperties['placeItems']
}

function toGridTemplate(value: number | string | undefined): string | undefined {
  if (value === undefined) return undefined
  if (typeof value === 'number') return `repeat(${value}, 1fr)`
  return value
}

export function Grid({
  children,
  columns,
  rows,
  spacing,
  columnSpacing,
  rowSpacing,
  templateColumns,
  templateRows,
  autoFlow,
  autoColumns,
  autoRows,
  areas,
  placeItems,
  style,
  ...rest
}: GridProps) {
  const gridStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: templateColumns ?? toGridTemplate(columns),
    gridTemplateRows: templateRows ?? toGridTemplate(rows),
    columnGap: columnSpacing ? `${Number(columnSpacing) * 4}px` : spacing ? `${Number(spacing) * 4}px` : undefined,
    rowGap: rowSpacing ? `${Number(rowSpacing) * 4}px` : spacing ? `${Number(spacing) * 4}px` : undefined,
    gridAutoFlow: autoFlow,
    gridAutoColumns: autoColumns,
    gridAutoRows: autoRows,
    gridTemplateAreas: areas,
    placeItems,
    ...style,
  }

  return (
    <Box style={gridStyle} {...rest}>
      {children}
    </Box>
  )
}

export interface GridItemProps extends BoxProps {
  colSpan?: number
  rowSpan?: number
  colStart?: number
  colEnd?: number
  rowStart?: number
  rowEnd?: number
  area?: string
}

export function GridItem({
  children,
  colSpan,
  rowSpan,
  colStart,
  colEnd,
  rowStart,
  rowEnd,
  area,
  style,
  ...rest
}: GridItemProps) {
  const itemStyle: CSSProperties = {
    gridColumn: colSpan ? `span ${colSpan}` : colStart || colEnd ? `${colStart ?? 'auto'} / ${colEnd ?? 'auto'}` : undefined,
    gridRow: rowSpan ? `span ${rowSpan}` : rowStart || rowEnd ? `${rowStart ?? 'auto'} / ${rowEnd ?? 'auto'}` : undefined,
    gridArea: area,
    ...style,
  }

  return (
    <Box style={itemStyle} {...rest}>
      {children}
    </Box>
  )
}
