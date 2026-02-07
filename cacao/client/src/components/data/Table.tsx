import { CSSProperties, ReactNode, useState, useMemo, useCallback } from 'react'
import { Box } from '../layout/Box'

export type SortDirection = 'asc' | 'desc' | null

export interface TableColumn<T = any> {
  key: string
  title: ReactNode
  width?: string | number
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  render?: (value: any, record: T, index: number) => ReactNode
}

export interface TableProps<T = any> {
  columns: TableColumn<T>[]
  data: T[]
  rowKey?: string | ((record: T, index: number) => string)
  loading?: boolean
  emptyText?: ReactNode
  striped?: boolean
  hoverable?: boolean
  bordered?: boolean
  compact?: boolean
  stickyHeader?: boolean
  maxHeight?: string | number

  // Sorting
  sortable?: boolean
  defaultSortKey?: string
  defaultSortDirection?: SortDirection
  onSort?: (key: string, direction: SortDirection) => void

  // Pagination
  pagination?: boolean | PaginationConfig

  // Selection
  selectable?: boolean
  selectedKeys?: string[]
  onSelectionChange?: (keys: string[]) => void

  // Row events
  onRowClick?: (record: T, index: number) => void

  className?: string
  style?: CSSProperties
}

export interface PaginationConfig {
  page?: number
  pageSize?: number
  total?: number
  showTotal?: boolean
  showPageSize?: boolean
  pageSizeOptions?: number[]
  onChange?: (page: number, pageSize: number) => void
}

const baseTableStyle: CSSProperties = {
  width: '100%',
  borderCollapse: 'separate',
  borderSpacing: 0,
}

const headerCellStyle: CSSProperties = {
  padding: '12px 16px',
  textAlign: 'left',
  fontWeight: 600,
  fontSize: '0.75rem',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
  color: 'rgba(255, 255, 255, 0.6)',
  backgroundColor: 'rgba(0, 0, 0, 0.2)',
  borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
  whiteSpace: 'nowrap',
}

const bodyCellStyle: CSSProperties = {
  padding: '12px 16px',
  fontSize: '0.875rem',
  color: 'rgba(255, 255, 255, 0.9)',
  borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
}

const compactCellStyle: CSSProperties = {
  padding: '8px 12px',
}

export function Table<T extends Record<string, any>>({
  columns,
  data,
  rowKey = 'id',
  loading = false,
  emptyText = 'No data',
  striped = false,
  hoverable = true,
  bordered = true,
  compact = false,
  stickyHeader = false,
  maxHeight,
  sortable: tableSortable = false,
  defaultSortKey,
  defaultSortDirection = 'asc',
  onSort,
  pagination = false,
  selectable = false,
  selectedKeys = [],
  onSelectionChange,
  onRowClick,
  className,
  style,
}: TableProps<T>) {
  // Sorting state
  const [sortKey, setSortKey] = useState<string | null>(defaultSortKey ?? null)
  const [sortDirection, setSortDirection] = useState<SortDirection>(defaultSortKey ? defaultSortDirection : null)

  // Pagination state
  const paginationConfig = typeof pagination === 'object' ? pagination : {}
  const [currentPage, setCurrentPage] = useState(paginationConfig.page ?? 1)
  const [pageSize, setPageSize] = useState(paginationConfig.pageSize ?? 10)

  // Selection state
  const [internalSelectedKeys, setInternalSelectedKeys] = useState<string[]>(selectedKeys)
  const effectiveSelectedKeys = selectedKeys.length > 0 ? selectedKeys : internalSelectedKeys

  const getRowKey = useCallback((record: T, index: number): string => {
    if (typeof rowKey === 'function') {
      return rowKey(record, index)
    }
    return String(record[rowKey] ?? index)
  }, [rowKey])

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortKey || !sortDirection) return data

    return [...data].sort((a, b) => {
      const aVal = a[sortKey]
      const bVal = b[sortKey]

      if (aVal === bVal) return 0
      if (aVal == null) return 1
      if (bVal == null) return -1

      const comparison = aVal < bVal ? -1 : 1
      return sortDirection === 'asc' ? comparison : -comparison
    })
  }, [data, sortKey, sortDirection])

  // Paginate data
  const paginatedData = useMemo(() => {
    if (!pagination) return sortedData

    const start = (currentPage - 1) * pageSize
    return sortedData.slice(start, start + pageSize)
  }, [sortedData, pagination, currentPage, pageSize])

  const totalItems = paginationConfig.total ?? data.length
  const totalPages = Math.ceil(totalItems / pageSize)

  const handleSort = (key: string) => {
    const column = columns.find(c => c.key === key)
    if (!column?.sortable && !tableSortable) return

    let newDirection: SortDirection = 'asc'
    if (sortKey === key) {
      if (sortDirection === 'asc') newDirection = 'desc'
      else if (sortDirection === 'desc') newDirection = null
    }

    setSortKey(newDirection ? key : null)
    setSortDirection(newDirection)
    onSort?.(key, newDirection)
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
    paginationConfig.onChange?.(page, pageSize)
  }

  const handlePageSizeChange = (size: number) => {
    setPageSize(size)
    setCurrentPage(1)
    paginationConfig.onChange?.(1, size)
  }

  const handleSelectAll = () => {
    if (effectiveSelectedKeys.length === paginatedData.length) {
      setInternalSelectedKeys([])
      onSelectionChange?.([])
    } else {
      const allKeys = paginatedData.map((record, index) => getRowKey(record, index))
      setInternalSelectedKeys(allKeys)
      onSelectionChange?.(allKeys)
    }
  }

  const handleSelectRow = (key: string) => {
    const newKeys = effectiveSelectedKeys.includes(key)
      ? effectiveSelectedKeys.filter(k => k !== key)
      : [...effectiveSelectedKeys, key]
    setInternalSelectedKeys(newKeys)
    onSelectionChange?.(newKeys)
  }

  const containerStyle: CSSProperties = {
    backgroundColor: '#1e1e2e',
    borderRadius: '12px',
    border: bordered ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
    overflow: 'hidden',
    ...style,
  }

  const wrapperStyle: CSSProperties = {
    overflow: maxHeight ? 'auto' : undefined,
    maxHeight: typeof maxHeight === 'number' ? `${maxHeight}px` : maxHeight,
  }

  const getSortIcon = (key: string) => {
    if (sortKey !== key) {
      return (
        <span style={{ opacity: 0.3, marginLeft: '4px' }}>
          <SortIcon direction={null} />
        </span>
      )
    }
    return (
      <span style={{ marginLeft: '4px', color: '#a78bfa' }}>
        <SortIcon direction={sortDirection} />
      </span>
    )
  }

  return (
    <Box className={className} style={containerStyle}>
      <div style={wrapperStyle}>
        <table style={baseTableStyle}>
          <thead>
            <tr>
              {selectable && (
                <th style={{ ...headerCellStyle, width: '48px', textAlign: 'center', ...(compact && compactCellStyle) }}>
                  <Checkbox
                    checked={effectiveSelectedKeys.length === paginatedData.length && paginatedData.length > 0}
                    indeterminate={effectiveSelectedKeys.length > 0 && effectiveSelectedKeys.length < paginatedData.length}
                    onChange={handleSelectAll}
                  />
                </th>
              )}
              {columns.map((column) => {
                const isSortable = column.sortable ?? tableSortable
                const thStyle: CSSProperties = {
                  ...headerCellStyle,
                  ...(compact && compactCellStyle),
                  textAlign: column.align,
                  width: column.width,
                  cursor: isSortable ? 'pointer' : undefined,
                  userSelect: isSortable ? 'none' : undefined,
                  ...(stickyHeader && { position: 'sticky', top: 0, zIndex: 1 }),
                }

                return (
                  <th
                    key={column.key}
                    style={thStyle}
                    onClick={() => isSortable && handleSort(column.key)}
                  >
                    <span style={{ display: 'inline-flex', alignItems: 'center' }}>
                      {column.title}
                      {isSortable && getSortIcon(column.key)}
                    </span>
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td
                  colSpan={columns.length + (selectable ? 1 : 0)}
                  style={{ ...bodyCellStyle, textAlign: 'center', padding: '40px' }}
                >
                  <LoadingSpinner />
                </td>
              </tr>
            ) : paginatedData.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length + (selectable ? 1 : 0)}
                  style={{ ...bodyCellStyle, textAlign: 'center', padding: '40px', color: 'rgba(255, 255, 255, 0.4)' }}
                >
                  {emptyText}
                </td>
              </tr>
            ) : (
              paginatedData.map((record, rowIndex) => {
                const key = getRowKey(record, rowIndex)
                const isSelected = effectiveSelectedKeys.includes(key)
                const isEven = rowIndex % 2 === 0

                const rowStyle: CSSProperties = {
                  backgroundColor: isSelected
                    ? 'rgba(167, 139, 250, 0.1)'
                    : striped && !isEven
                    ? 'rgba(255, 255, 255, 0.02)'
                    : undefined,
                  cursor: onRowClick ? 'pointer' : undefined,
                  transition: 'background-color 0.15s',
                }

                return (
                  <tr
                    key={key}
                    style={rowStyle}
                    onClick={() => onRowClick?.(record, rowIndex)}
                    onMouseEnter={(e) => {
                      if (hoverable) {
                        (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (hoverable) {
                        (e.currentTarget as HTMLElement).style.backgroundColor = isSelected
                          ? 'rgba(167, 139, 250, 0.1)'
                          : striped && !isEven
                          ? 'rgba(255, 255, 255, 0.02)'
                          : ''
                      }
                    }}
                  >
                    {selectable && (
                      <td style={{ ...bodyCellStyle, ...(compact && compactCellStyle), width: '48px', textAlign: 'center' }}>
                        <Checkbox
                          checked={isSelected}
                          onChange={() => handleSelectRow(key)}
                        />
                      </td>
                    )}
                    {columns.map((column) => {
                      const value = record[column.key]
                      const cellContent = column.render
                        ? column.render(value, record, rowIndex)
                        : value

                      return (
                        <td
                          key={column.key}
                          style={{
                            ...bodyCellStyle,
                            ...(compact && compactCellStyle),
                            textAlign: column.align,
                          }}
                        >
                          {cellContent}
                        </td>
                      )
                    })}
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>

      {pagination && !loading && paginatedData.length > 0 && (
        <Pagination
          currentPage={currentPage}
          pageSize={pageSize}
          totalItems={totalItems}
          totalPages={totalPages}
          showTotal={paginationConfig.showTotal ?? true}
          showPageSize={paginationConfig.showPageSize ?? true}
          pageSizeOptions={paginationConfig.pageSizeOptions ?? [10, 25, 50, 100]}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
        />
      )}
    </Box>
  )
}

// Internal components

function Checkbox({
  checked,
  indeterminate,
  onChange,
}: {
  checked: boolean
  indeterminate?: boolean
  onChange: () => void
}) {
  const style: CSSProperties = {
    width: '16px',
    height: '16px',
    borderRadius: '4px',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    backgroundColor: checked || indeterminate ? '#7c3aed' : 'transparent',
    cursor: 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.15s',
  }

  return (
    <div style={style} onClick={(e) => { e.stopPropagation(); onChange() }}>
      {checked && (
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <path d="M2 5L4 7L8 3" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
      {indeterminate && !checked && (
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <path d="M2 5H8" stroke="white" strokeWidth="2" strokeLinecap="round" />
        </svg>
      )}
    </div>
  )
}

function SortIcon({ direction }: { direction: SortDirection }) {
  if (direction === 'asc') {
    return (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
        <path d="M6 2L10 7H2L6 2Z" />
      </svg>
    )
  }
  if (direction === 'desc') {
    return (
      <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
        <path d="M6 10L2 5H10L6 10Z" />
      </svg>
    )
  }
  return (
    <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
      <path d="M6 2L9 5H3L6 2Z" opacity="0.5" />
      <path d="M6 10L3 7H9L6 10Z" opacity="0.5" />
    </svg>
  )
}

function LoadingSpinner() {
  return (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      style={{ animation: 'spin 1s linear infinite' }}
    >
      <style>
        {`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}
      </style>
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="rgba(167, 139, 250, 0.3)"
        strokeWidth="3"
      />
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="#a78bfa"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray="31.4 31.4"
        style={{ transform: 'rotate(-90deg)', transformOrigin: 'center' }}
      />
    </svg>
  )
}

interface PaginationProps {
  currentPage: number
  pageSize: number
  totalItems: number
  totalPages: number
  showTotal: boolean
  showPageSize: boolean
  pageSizeOptions: number[]
  onPageChange: (page: number) => void
  onPageSizeChange: (size: number) => void
}

function Pagination({
  currentPage,
  pageSize,
  totalItems,
  totalPages,
  showTotal,
  showPageSize,
  pageSizeOptions,
  onPageChange,
  onPageSizeChange,
}: PaginationProps) {
  const containerStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '12px 16px',
    borderTop: '1px solid rgba(255, 255, 255, 0.1)',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    fontSize: '0.875rem',
    color: 'rgba(255, 255, 255, 0.6)',
  }

  const buttonStyle: CSSProperties = {
    padding: '6px 12px',
    borderRadius: '6px',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    backgroundColor: 'transparent',
    color: 'rgba(255, 255, 255, 0.8)',
    cursor: 'pointer',
    fontSize: '0.875rem',
    transition: 'all 0.15s',
  }

  const disabledButtonStyle: CSSProperties = {
    ...buttonStyle,
    opacity: 0.4,
    cursor: 'not-allowed',
  }

  const selectStyle: CSSProperties = {
    padding: '6px 8px',
    borderRadius: '6px',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    backgroundColor: '#1e1e2e',
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: '0.875rem',
    cursor: 'pointer',
  }

  const start = (currentPage - 1) * pageSize + 1
  const end = Math.min(currentPage * pageSize, totalItems)

  return (
    <div style={containerStyle}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {showTotal && (
          <span>
            Showing {start}-{end} of {totalItems}
          </span>
        )}
        {showPageSize && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>Rows per page:</span>
            <select
              style={selectStyle}
              value={pageSize}
              onChange={(e) => onPageSizeChange(Number(e.target.value))}
            >
              {pageSizeOptions.map((size) => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button
          style={currentPage === 1 ? disabledButtonStyle : buttonStyle}
          disabled={currentPage === 1}
          onClick={() => onPageChange(1)}
        >
          First
        </button>
        <button
          style={currentPage === 1 ? disabledButtonStyle : buttonStyle}
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
        >
          Prev
        </button>
        <span style={{ padding: '0 8px' }}>
          Page {currentPage} of {totalPages}
        </span>
        <button
          style={currentPage === totalPages ? disabledButtonStyle : buttonStyle}
          disabled={currentPage === totalPages}
          onClick={() => onPageChange(currentPage + 1)}
        >
          Next
        </button>
        <button
          style={currentPage === totalPages ? disabledButtonStyle : buttonStyle}
          disabled={currentPage === totalPages}
          onClick={() => onPageChange(totalPages)}
        >
          Last
        </button>
      </div>
    </div>
  )
}
