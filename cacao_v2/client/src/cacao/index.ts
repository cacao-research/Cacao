/**
 * Cacao v2 Client - React hooks and utilities for Cacao applications.
 *
 * @example
 * import { CacaoProvider, useSignal, useEvent } from './cacao'
 *
 * function Counter() {
 *   const count = useSignal('count', 0)
 *   const increment = useEvent('increment')
 *
 *   return (
 *     <div>
 *       <h1>Count: {count}</h1>
 *       <button onClick={() => increment()}>+</button>
 *     </div>
 *   )
 * }
 *
 * function App() {
 *   return (
 *     <CacaoProvider url="ws://localhost:8000/ws">
 *       <Counter />
 *     </CacaoProvider>
 *   )
 * }
 */

// Core provider and hooks
export {
  CacaoProvider,
  useCacao,
  useSignal,
  useSignalSync,
  useEvent,
  useConnectionStatus,
  useSessionId,
  useIsConnected,
} from './hooks'

// WebSocket client (for advanced use cases)
export { WebSocketClient } from './websocket'

// Store (for advanced use cases)
export { createStore } from './store'
export type { Store } from './store'

// Types
export type {
  ServerMessage,
  ClientMessage,
  InitMessage,
  UpdateMessage,
  BatchMessage,
  ErrorMessage,
  EventMessage,
  ConnectionStatus,
  CacaoContextValue,
  CacaoProviderOptions,
  UseSignalOptions,
  EventDispatcher,
} from './types'
