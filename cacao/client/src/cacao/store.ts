/**
 * State store for Cacao v2 client.
 *
 * A simple observable store that holds the current state from the server
 * and notifies subscribers when it changes.
 */

export type Listener = () => void

export interface Store {
  getState(): Record<string, unknown>
  getSessionId(): string | null
  setState(updates: Record<string, unknown>): void
  setFullState(state: Record<string, unknown>, sessionId: string): void
  subscribe(listener: Listener): () => void
  getSignal<T>(name: string, defaultValue: T): T
}

export function createStore(): Store {
  let state: Record<string, unknown> = {}
  let sessionId: string | null = null
  const listeners = new Set<Listener>()

  function notify(): void {
    listeners.forEach((listener) => {
      try {
        listener()
      } catch {
        // Ignore listener errors
      }
    })
  }

  return {
    getState(): Record<string, unknown> {
      return state
    },

    getSessionId(): string | null {
      return sessionId
    },

    setState(updates: Record<string, unknown>): void {
      // Shallow merge updates
      let hasChanges = false

      for (const key of Object.keys(updates)) {
        if (state[key] !== updates[key]) {
          hasChanges = true
          break
        }
      }

      if (hasChanges) {
        state = { ...state, ...updates }
        notify()
      }
    },

    setFullState(newState: Record<string, unknown>, newSessionId: string): void {
      state = newState
      sessionId = newSessionId
      notify()
    },

    subscribe(listener: Listener): () => void {
      listeners.add(listener)
      return () => {
        listeners.delete(listener)
      }
    },

    getSignal<T>(name: string, defaultValue: T): T {
      if (name in state) {
        return state[name] as T
      }
      return defaultValue
    },
  }
}
