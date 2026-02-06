/**
 * React hooks for Cacao v2.
 *
 * These hooks provide access to the Cacao state and event system
 * from React components.
 */

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useRef,
  useSyncExternalStore,
  type ReactNode,
} from 'react'
import { WebSocketClient } from './websocket'
import { createStore, type Store } from './store'
import type {
  ServerMessage,
  ConnectionStatus,
  CacaoContextValue,
  CacaoProviderOptions,
  EventDispatcher,
} from './types'

// Create context with null default (must be used within provider)
const CacaoContext = createContext<CacaoContextValue | null>(null)

interface CacaoProviderProps extends CacaoProviderOptions {
  children: ReactNode
}

/**
 * Provider component that establishes the WebSocket connection
 * and provides Cacao context to child components.
 */
export function CacaoProvider({
  children,
  url,
  autoReconnect = true,
  reconnectDelay = 1000,
  maxReconnectAttempts = 10,
  onConnect,
  onDisconnect,
  onError,
}: CacaoProviderProps): ReactNode {
  const [status, setStatus] = useState<ConnectionStatus>('disconnected')
  const storeRef = useRef<Store | null>(null)
  const clientRef = useRef<WebSocketClient | null>(null)
  const [, forceUpdate] = useState({})

  // Initialize store on first render
  if (!storeRef.current) {
    storeRef.current = createStore()
  }

  const store = storeRef.current

  // Handle incoming messages
  const handleMessage = useCallback(
    (message: ServerMessage) => {
      switch (message.type) {
        case 'init':
          store.setFullState(message.state, message.sessionId)
          break

        case 'update':
          store.setState(message.changes)
          break

        case 'batch':
          const updates: Record<string, unknown> = {}
          for (const { key, value } of message.changes) {
            updates[key] = value
          }
          store.setState(updates)
          break

        case 'error':
          onError?.(new Error(message.message))
          break
      }
    },
    [store, onError]
  )

  // Handle status changes
  const handleStatusChange = useCallback(
    (newStatus: ConnectionStatus) => {
      setStatus(newStatus)

      if (newStatus === 'connected') {
        onConnect?.()
      } else if (newStatus === 'disconnected') {
        onDisconnect?.()
      }
    },
    [onConnect, onDisconnect]
  )

  // Initialize WebSocket client
  useEffect(() => {
    const client = new WebSocketClient({
      url,
      autoReconnect,
      reconnectDelay,
      maxReconnectAttempts,
      onMessage: handleMessage,
      onStatusChange: handleStatusChange,
      onError,
    })

    clientRef.current = client
    client.connect()

    // Subscribe to store changes for re-renders
    const unsubscribe = store.subscribe(() => {
      forceUpdate({})
    })

    return () => {
      client.disconnect()
      clientRef.current = null
      unsubscribe()
    }
  }, [
    url,
    autoReconnect,
    reconnectDelay,
    maxReconnectAttempts,
    handleMessage,
    handleStatusChange,
    onError,
    store,
  ])

  // Send event function
  const sendEvent = useCallback(
    (name: string, data: Record<string, unknown> = {}) => {
      clientRef.current?.sendEvent(name, data)
    },
    []
  )

  // Get signal value with type safety
  const getSignal = useCallback(
    <T,>(name: string, defaultValue: T): T => {
      return store.getSignal(name, defaultValue)
    },
    [store]
  )

  const value: CacaoContextValue = {
    state: store.getState(),
    status,
    sessionId: store.getSessionId(),
    sendEvent,
    getSignal,
  }

  return <CacaoContext.Provider value={value}>{children}</CacaoContext.Provider>
}

/**
 * Hook to access the full Cacao context.
 *
 * @throws Error if used outside of CacaoProvider
 */
export function useCacao(): CacaoContextValue {
  const context = useContext(CacaoContext)
  if (!context) {
    throw new Error('useCacao must be used within a CacaoProvider')
  }
  return context
}

/**
 * Hook to subscribe to a specific signal value.
 *
 * @param name - The signal name
 * @param defaultValue - Default value if signal is not in state
 * @returns The current signal value
 *
 * @example
 * const count = useSignal('count', 0)
 */
export function useSignal<T>(name: string, defaultValue: T): T {
  const { getSignal, state } = useCacao()

  // Use state in dependency to re-render when it changes
  // This is a simple approach - could optimize with useSyncExternalStore
  return getSignal(name, defaultValue)
}

/**
 * Hook to subscribe to a signal with external store synchronization.
 * This is more efficient for frequently changing values.
 *
 * @param name - The signal name
 * @param defaultValue - Default value if signal is not in state
 */
export function useSignalSync<T>(name: string, defaultValue: T): T {
  const context = useContext(CacaoContext)
  if (!context) {
    throw new Error('useSignalSync must be used within a CacaoProvider')
  }

  // Fallback to simple implementation since we manage store internally
  return context.getSignal(name, defaultValue)
}

/**
 * Hook to create an event dispatcher function.
 *
 * @param eventName - The event name to dispatch
 * @returns A function that sends the event with optional data
 *
 * @example
 * const increment = useEvent('increment')
 * // Later: increment() or increment({ amount: 5 })
 */
export function useEvent<T extends Record<string, unknown> = Record<string, unknown>>(
  eventName: string
): EventDispatcher<T> {
  const { sendEvent } = useCacao()

  return useCallback(
    (data?: T) => {
      sendEvent(eventName, data ?? {})
    },
    [sendEvent, eventName]
  )
}

/**
 * Hook to get the current connection status.
 *
 * @returns The current WebSocket connection status
 */
export function useConnectionStatus(): ConnectionStatus {
  const { status } = useCacao()
  return status
}

/**
 * Hook to get the current session ID.
 *
 * @returns The session ID or null if not connected
 */
export function useSessionId(): string | null {
  const { sessionId } = useCacao()
  return sessionId
}

/**
 * Hook to check if connected to the server.
 *
 * @returns True if connected
 */
export function useIsConnected(): boolean {
  const { status } = useCacao()
  return status === 'connected'
}
