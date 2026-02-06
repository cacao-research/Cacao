import { CSSProperties, ReactNode } from 'react'
import { Box } from '../layout/Box'

export interface DescriptionItem {
  key?: string
  label: ReactNode
  value: ReactNode
  span?: number
}

export interface DescriptionsProps {
  items: DescriptionItem[]
  title?: ReactNode
  columns?: number
  bordered?: boolean
  layout?: 'horizontal' | 'vertical'
  size?: 'sm' | 'md' | 'lg'
  colon?: boolean
  labelWidth?: string | number
  className?: string
  style?: CSSProperties
}

const sizeStyles = {
  sm: { labelSize: '0.75rem', valueSize: '0.8125rem', padding: '8px 12px' },
  md: { labelSize: '0.8125rem', valueSize: '0.875rem', padding: '12px 16px' },
  lg: { labelSize: '0.875rem', valueSize: '1rem', padding: '16px 20px' },
}

export function Descriptions({
  items,
  title,
  columns = 3,
  bordered = true,
  layout = 'horizontal',
  size = 'md',
  colon = true,
  labelWidth = 'auto',
  className,
  style,
}: DescriptionsProps) {
  const sizes = sizeStyles[size]

  const containerStyle: CSSProperties = {
    backgroundColor: '#1e1e2e',
    borderRadius: '12px',
    border: bordered ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    overflow: 'hidden',
    ...style,
  }

  const titleStyle: CSSProperties = {
    padding: sizes.padding,
    fontWeight: 600,
    fontSize: '1rem',
    color: 'rgba(255, 255, 255, 0.9)',
    borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
  }

  const gridStyle: CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, 1fr)`,
  }

  return (
    <Box className={className} style={containerStyle}>
      {title && <div style={titleStyle}>{title}</div>}
      <div style={gridStyle}>
        {items.map((item, index) => (
          <DescriptionCell
            key={item.key ?? index}
            item={item}
            layout={layout}
            size={size}
            colon={colon}
            labelWidth={labelWidth}
            bordered={bordered}
            isLast={index === items.length - 1}
            column={index % columns}
            columns={columns}
          />
        ))}
      </div>
    </Box>
  )
}

interface DescriptionCellProps {
  item: DescriptionItem
  layout: 'horizontal' | 'vertical'
  size: 'sm' | 'md' | 'lg'
  colon: boolean
  labelWidth: string | number
  bordered: boolean
  isLast: boolean
  column: number
  columns: number
}

function DescriptionCell({
  item,
  layout,
  size,
  colon,
  labelWidth,
  bordered,
  column,
  columns,
}: DescriptionCellProps) {
  const sizes = sizeStyles[size]

  const cellStyle: CSSProperties = {
    padding: sizes.padding,
    gridColumn: item.span ? `span ${item.span}` : undefined,
    borderBottom: bordered ? '1px solid rgba(255, 255, 255, 0.05)' : 'none',
    borderRight: bordered && column < columns - 1 ? '1px solid rgba(255, 255, 255, 0.05)' : 'none',
  }

  const labelStyle: CSSProperties = {
    fontSize: sizes.labelSize,
    color: 'rgba(255, 255, 255, 0.5)',
    fontWeight: 500,
    width: layout === 'horizontal' ? (typeof labelWidth === 'number' ? `${labelWidth}px` : labelWidth) : undefined,
    flexShrink: 0,
    marginBottom: layout === 'vertical' ? '4px' : 0,
    marginRight: layout === 'horizontal' ? '12px' : 0,
  }

  const valueStyle: CSSProperties = {
    fontSize: sizes.valueSize,
    color: 'rgba(255, 255, 255, 0.9)',
    flex: 1,
    wordBreak: 'break-word',
  }

  if (layout === 'vertical') {
    return (
      <div style={cellStyle}>
        <div style={labelStyle}>
          {item.label}
          {colon && ':'}
        </div>
        <div style={valueStyle}>{item.value}</div>
      </div>
    )
  }

  return (
    <div style={{ ...cellStyle, display: 'flex', alignItems: 'flex-start' }}>
      <div style={labelStyle}>
        {item.label}
        {colon && ':'}
      </div>
      <div style={valueStyle}>{item.value}</div>
    </div>
  )
}
