/**
 * Type definitions for Cacao v2 client.
 */

/** Message types from server to client */
export type ServerMessage =
  | InitMessage
  | UpdateMessage
  | BatchMessage
  | ErrorMessage

export interface InitMessage {
  type: 'init'
  state: Record<string, unknown>
  sessionId: string
}

export interface UpdateMessage {
  type: 'update'
  changes: Record<string, unknown>
}

export interface BatchMessage {
  type: 'batch'
  changes: Array<{ key: string; value: unknown }>
}

export interface ErrorMessage {
  type: 'error'
  message: string
  code?: string
}

/** Message types from client to server */
export type ClientMessage = EventMessage

export interface EventMessage {
  type: 'event'
  name: string
  data: Record<string, unknown>
}

/** Connection status for the WebSocket */
export type ConnectionStatus =
  | 'connecting'
  | 'connected'
  | 'disconnected'
  | 'reconnecting'

/** Cacao context value passed through React context */
export interface CacaoContextValue {
  /** Current state from the server */
  state: Record<string, unknown>
  /** Current connection status */
  status: ConnectionStatus
  /** Session ID (null until connected) */
  sessionId: string | null
  /** Send an event to the server */
  sendEvent: (name: string, data?: Record<string, unknown>) => void
  /** Get a signal value with type safety */
  getSignal: <T>(name: string, defaultValue: T) => T
}

/** Options for the CacaoProvider */
export interface CacaoProviderOptions {
  /** WebSocket URL to connect to */
  url: string
  /** Whether to automatically reconnect on disconnect */
  autoReconnect?: boolean
  /** Delay between reconnection attempts (ms) */
  reconnectDelay?: number
  /** Maximum number of reconnection attempts */
  maxReconnectAttempts?: number
  /** Callback when connection is established */
  onConnect?: () => void
  /** Callback when connection is lost */
  onDisconnect?: () => void
  /** Callback when an error occurs */
  onError?: (error: Error) => void
}

/** Options for useSignal hook */
export interface UseSignalOptions<T> {
  /** Default value if signal is not in state */
  defaultValue: T
  /** Transform function applied to the value */
  transform?: (value: unknown) => T
}

/** Return type for useEvent hook */
export type EventDispatcher<T extends Record<string, unknown> = Record<string, unknown>> = (
  data?: T
) => void
