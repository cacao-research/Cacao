import { CSSProperties, ReactNode, useState, useCallback } from 'react'
import { Box } from '../layout/Box'

export interface TreeNode {
  key: string
  title: ReactNode
  icon?: ReactNode
  children?: TreeNode[]
  disabled?: boolean
  selectable?: boolean
}

export interface TreeProps {
  data: TreeNode[]
  defaultExpandedKeys?: string[]
  defaultSelectedKeys?: string[]
  expandedKeys?: string[]
  selectedKeys?: string[]
  multiple?: boolean
  checkable?: boolean
  checkedKeys?: string[]
  defaultCheckedKeys?: string[]
  showLine?: boolean
  showIcon?: boolean
  indent?: number
  onExpand?: (keys: string[], node: TreeNode) => void
  onSelect?: (keys: string[], node: TreeNode) => void
  onCheck?: (keys: string[], node: TreeNode) => void
  className?: string
  style?: CSSProperties
}

export function Tree({
  data,
  defaultExpandedKeys = [],
  defaultSelectedKeys = [],
  expandedKeys: controlledExpandedKeys,
  selectedKeys: controlledSelectedKeys,
  multiple = false,
  checkable = false,
  checkedKeys: controlledCheckedKeys,
  defaultCheckedKeys = [],
  showLine = false,
  showIcon = true,
  indent = 24,
  onExpand,
  onSelect,
  onCheck,
  className,
  style,
}: TreeProps) {
  const [internalExpanded, setInternalExpanded] = useState<string[]>(defaultExpandedKeys)
  const [internalSelected, setInternalSelected] = useState<string[]>(defaultSelectedKeys)
  const [internalChecked, setInternalChecked] = useState<string[]>(defaultCheckedKeys)

  const expandedKeys = controlledExpandedKeys ?? internalExpanded
  const selectedKeys = controlledSelectedKeys ?? internalSelected
  const checkedKeys = controlledCheckedKeys ?? internalChecked

  const handleExpand = useCallback((key: string, node: TreeNode) => {
    const newKeys = expandedKeys.includes(key)
      ? expandedKeys.filter(k => k !== key)
      : [...expandedKeys, key]

    if (!controlledExpandedKeys) {
      setInternalExpanded(newKeys)
    }
    onExpand?.(newKeys, node)
  }, [expandedKeys, controlledExpandedKeys, onExpand])

  const handleSelect = useCallback((key: string, node: TreeNode) => {
    if (node.disabled || node.selectable === false) return

    let newKeys: string[]
    if (multiple) {
      newKeys = selectedKeys.includes(key)
        ? selectedKeys.filter(k => k !== key)
        : [...selectedKeys, key]
    } else {
      newKeys = selectedKeys.includes(key) ? [] : [key]
    }

    if (!controlledSelectedKeys) {
      setInternalSelected(newKeys)
    }
    onSelect?.(newKeys, node)
  }, [selectedKeys, controlledSelectedKeys, multiple, onSelect])

  const handleCheck = useCallback((key: string, node: TreeNode) => {
    if (node.disabled) return

    const newKeys = checkedKeys.includes(key)
      ? checkedKeys.filter(k => k !== key)
      : [...checkedKeys, key]

    if (!controlledCheckedKeys) {
      setInternalChecked(newKeys)
    }
    onCheck?.(newKeys, node)
  }, [checkedKeys, controlledCheckedKeys, onCheck])

  const containerStyle: CSSProperties = {
    backgroundColor: '#1e1e2e',
    borderRadius: '12px',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    padding: '8px 0',
    overflow: 'hidden',
    ...style,
  }

  return (
    <Box className={className} style={containerStyle}>
      {data.map(node => (
        <TreeNodeComponent
          key={node.key}
          node={node}
          level={0}
          expandedKeys={expandedKeys}
          selectedKeys={selectedKeys}
          checkedKeys={checkedKeys}
          checkable={checkable}
          showLine={showLine}
          showIcon={showIcon}
          indent={indent}
          onExpand={handleExpand}
          onSelect={handleSelect}
          onCheck={handleCheck}
        />
      ))}
    </Box>
  )
}

interface TreeNodeComponentProps {
  node: TreeNode
  level: number
  expandedKeys: string[]
  selectedKeys: string[]
  checkedKeys: string[]
  checkable: boolean
  showLine: boolean
  showIcon: boolean
  indent: number
  onExpand: (key: string, node: TreeNode) => void
  onSelect: (key: string, node: TreeNode) => void
  onCheck: (key: string, node: TreeNode) => void
}

function TreeNodeComponent({
  node,
  level,
  expandedKeys,
  selectedKeys,
  checkedKeys,
  checkable,
  showLine,
  showIcon,
  indent,
  onExpand,
  onSelect,
  onCheck,
}: TreeNodeComponentProps) {
  const hasChildren = node.children && node.children.length > 0
  const isExpanded = expandedKeys.includes(node.key)
  const isSelected = selectedKeys.includes(node.key)
  const isChecked = checkedKeys.includes(node.key)

  const nodeStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    padding: '6px 12px',
    paddingLeft: `${12 + level * indent}px`,
    cursor: node.disabled ? 'not-allowed' : 'pointer',
    opacity: node.disabled ? 0.5 : 1,
    backgroundColor: isSelected ? 'rgba(167, 139, 250, 0.15)' : 'transparent',
    transition: 'background-color 0.15s',
    position: 'relative',
  }

  const expandIconStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '20px',
    height: '20px',
    marginRight: '4px',
    flexShrink: 0,
    transition: 'transform 0.2s',
    transform: isExpanded ? 'rotate(90deg)' : 'rotate(0deg)',
  }

  const contentStyle: CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    flex: 1,
    minWidth: 0,
  }

  const titleStyle: CSSProperties = {
    fontSize: '0.875rem',
    color: isSelected ? '#a78bfa' : 'rgba(255, 255, 255, 0.9)',
    fontWeight: isSelected ? 500 : 400,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  }

  const lineStyle: CSSProperties = showLine ? {
    position: 'absolute',
    left: `${12 + (level - 1) * indent + indent / 2}px`,
    top: 0,
    bottom: 0,
    width: '1px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  } : {}

  return (
    <>
      <div
        style={nodeStyle}
        onClick={() => onSelect(node.key, node)}
        onMouseEnter={(e) => {
          if (!node.disabled && !isSelected) {
            (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
          }
        }}
        onMouseLeave={(e) => {
          if (!node.disabled && !isSelected) {
            (e.currentTarget as HTMLElement).style.backgroundColor = ''
          }
        }}
      >
        {showLine && level > 0 && <div style={lineStyle} />}

        <div
          style={expandIconStyle}
          onClick={(e) => {
            e.stopPropagation()
            if (hasChildren) onExpand(node.key, node)
          }}
        >
          {hasChildren && <ChevronIcon />}
        </div>

        {checkable && (
          <Checkbox
            checked={isChecked}
            disabled={node.disabled}
            onChange={() => onCheck(node.key, node)}
          />
        )}

        <div style={contentStyle}>
          {showIcon && node.icon && (
            <span style={{ display: 'flex', color: 'rgba(255, 255, 255, 0.6)' }}>
              {node.icon}
            </span>
          )}
          {showIcon && !node.icon && hasChildren && (
            <span style={{ display: 'flex', color: 'rgba(255, 255, 255, 0.6)' }}>
              {isExpanded ? <FolderOpenIcon /> : <FolderIcon />}
            </span>
          )}
          {showIcon && !node.icon && !hasChildren && (
            <span style={{ display: 'flex', color: 'rgba(255, 255, 255, 0.4)' }}>
              <FileIcon />
            </span>
          )}
          <span style={titleStyle}>{node.title}</span>
        </div>
      </div>

      {hasChildren && isExpanded && (
        <div>
          {node.children!.map(child => (
            <TreeNodeComponent
              key={child.key}
              node={child}
              level={level + 1}
              expandedKeys={expandedKeys}
              selectedKeys={selectedKeys}
              checkedKeys={checkedKeys}
              checkable={checkable}
              showLine={showLine}
              showIcon={showIcon}
              indent={indent}
              onExpand={onExpand}
              onSelect={onSelect}
              onCheck={onCheck}
            />
          ))}
        </div>
      )}
    </>
  )
}

function Checkbox({
  checked,
  disabled,
  onChange,
}: {
  checked: boolean
  disabled?: boolean
  onChange: () => void
}) {
  const style: CSSProperties = {
    width: '16px',
    height: '16px',
    borderRadius: '4px',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    backgroundColor: checked ? '#7c3aed' : 'transparent',
    cursor: disabled ? 'not-allowed' : 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
    marginRight: '4px',
  }

  return (
    <div style={style} onClick={(e) => { e.stopPropagation(); if (!disabled) onChange() }}>
      {checked && (
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <path d="M2 5L4 7L8 3" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      )}
    </div>
  )
}

function ChevronIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" fill="rgba(255, 255, 255, 0.5)">
      <path d="M5 3L9 7L5 11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    </svg>
  )
}

function FolderIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <path d="M2 4C2 3.44772 2.44772 3 3 3H6L7.5 4.5H13C13.5523 4.5 14 4.94772 14 5.5V12C14 12.5523 13.5523 13 13 13H3C2.44772 13 2 12.5523 2 12V4Z" />
    </svg>
  )
}

function FolderOpenIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <path d="M2 4C2 3.44772 2.44772 3 3 3H6L7.5 4.5H13C13.5523 4.5 14 4.94772 14 5.5V6H3.5C2.67157 6 2 6.67157 2 7.5V4Z" />
      <path d="M2 7.5C2 6.94772 2.44772 6.5 3 6.5H14L13 13H3C2.44772 13 2 12.5523 2 12V7.5Z" />
    </svg>
  )
}

function FileIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <path d="M4 2C3.44772 2 3 2.44772 3 3V13C3 13.5523 3.44772 14 4 14H12C12.5523 14 13 13.5523 13 13V6L9 2H4Z" />
    </svg>
  )
}
