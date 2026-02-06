/**
 * Error Boundary components for Cacao v2.
 *
 * Provides error handling and fallback UI for React component trees.
 */

import { Component, ReactNode, CSSProperties } from 'react'

export interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode)
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void
  resetOnPropsChange?: unknown[]
}

interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

/**
 * Error boundary component that catches JavaScript errors in its child tree.
 *
 * @example
 * <ErrorBoundary fallback={<ErrorFallback />}>
 *   <MyComponent />
 * </ErrorBoundary>
 *
 * @example
 * <ErrorBoundary fallback={(error, reset) => (
 *   <div>
 *     <p>Error: {error.message}</p>
 *     <button onClick={reset}>Try Again</button>
 *   </div>
 * )}>
 *   <MyComponent />
 * </ErrorBoundary>
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    this.props.onError?.(error, errorInfo)
  }

  componentDidUpdate(prevProps: ErrorBoundaryProps): void {
    if (this.state.hasError && this.props.resetOnPropsChange) {
      const hasPropsChanged = this.props.resetOnPropsChange.some(
        (prop, index) => prop !== prevProps.resetOnPropsChange?.[index]
      )
      if (hasPropsChanged) {
        this.reset()
      }
    }
  }

  reset = (): void => {
    this.setState({ hasError: false, error: null })
  }

  render(): ReactNode {
    if (this.state.hasError && this.state.error) {
      if (typeof this.props.fallback === 'function') {
        return this.props.fallback(this.state.error, this.reset)
      }
      if (this.props.fallback) {
        return this.props.fallback
      }
      return <DefaultErrorFallback error={this.state.error} onReset={this.reset} />
    }

    return this.props.children
  }
}

interface DefaultErrorFallbackProps {
  error: Error
  onReset: () => void
}

/**
 * Default error fallback UI.
 */
function DefaultErrorFallback({ error, onReset }: DefaultErrorFallbackProps) {
  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px',
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    borderRadius: '12px',
    border: '1px solid rgba(239, 68, 68, 0.3)',
  }

  const iconStyle: CSSProperties = {
    width: '48px',
    height: '48px',
    color: '#f87171',
    marginBottom: '16px',
  }

  const titleStyle: CSSProperties = {
    fontSize: '1.125rem',
    fontWeight: 600,
    color: '#f87171',
    marginBottom: '8px',
  }

  const messageStyle: CSSProperties = {
    fontSize: '0.875rem',
    color: 'rgba(255, 255, 255, 0.6)',
    textAlign: 'center',
    marginBottom: '16px',
    maxWidth: '400px',
  }

  const buttonStyle: CSSProperties = {
    padding: '8px 16px',
    fontSize: '0.875rem',
    fontWeight: 500,
    color: '#ffffff',
    backgroundColor: '#ef4444',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.15s',
  }

  return (
    <div style={containerStyle}>
      <svg style={iconStyle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
      <div style={titleStyle}>Something went wrong</div>
      <div style={messageStyle}>{error.message}</div>
      <button
        style={buttonStyle}
        onClick={onReset}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLElement).style.backgroundColor = '#dc2626'
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLElement).style.backgroundColor = '#ef4444'
        }}
      >
        Try Again
      </button>
    </div>
  )
}

export interface ConnectionErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode | ((retry: () => void) => ReactNode)
}

/**
 * Simple error display component for connection errors.
 */
export function ConnectionError({
  message = 'Connection lost',
  onRetry,
}: {
  message?: string
  onRetry?: () => void
}) {
  const containerStyle: CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px',
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
    borderRadius: '12px',
    border: '1px solid rgba(245, 158, 11, 0.3)',
  }

  const iconStyle: CSSProperties = {
    width: '48px',
    height: '48px',
    color: '#fbbf24',
    marginBottom: '16px',
  }

  const titleStyle: CSSProperties = {
    fontSize: '1.125rem',
    fontWeight: 600,
    color: '#fbbf24',
    marginBottom: '8px',
  }

  const messageStyle: CSSProperties = {
    fontSize: '0.875rem',
    color: 'rgba(255, 255, 255, 0.6)',
    textAlign: 'center',
    marginBottom: '16px',
  }

  const buttonStyle: CSSProperties = {
    padding: '8px 16px',
    fontSize: '0.875rem',
    fontWeight: 500,
    color: '#000000',
    backgroundColor: '#fbbf24',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.15s',
  }

  return (
    <div style={containerStyle}>
      <svg style={iconStyle} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M1 1l22 22M16.72 11.06A10.94 10.94 0 0119 12.55M5 12.55a10.94 10.94 0 015.17-2.39M10.71 5.05A16 16 0 0122.58 9M1.42 9a15.91 15.91 0 014.7-2.88M8.53 16.11a6 6 0 016.95 0M12 20h.01" />
      </svg>
      <div style={titleStyle}>{message}</div>
      <div style={messageStyle}>Please check your connection and try again.</div>
      {onRetry && (
        <button
          style={buttonStyle}
          onClick={onRetry}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLElement).style.backgroundColor = '#f59e0b'
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLElement).style.backgroundColor = '#fbbf24'
          }}
        >
          Retry Connection
        </button>
      )}
    </div>
  )
}
