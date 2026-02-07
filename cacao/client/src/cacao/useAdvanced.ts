/**
 * Advanced hooks for Cacao v2.
 *
 * These hooks provide additional functionality beyond the basic
 * signal and event hooks.
 */

import { useState, useEffect, useRef, useMemo, useCallback } from 'react'
import { useSignal, useEvent } from './hooks'

/**
 * Hook for client-side computed values derived from signals.
 *
 * @param deps - Array of signal names and their default values
 * @param compute - Function that computes the derived value
 * @returns The computed value
 *
 * @example
 * const total = useComputed(
 *   [['price', 0], ['quantity', 1]],
 *   ([price, quantity]) => price * quantity
 * )
 */
export function useComputed<T, D extends [string, unknown][]>(
  deps: D,
  compute: (values: { [K in keyof D]: D[K] extends [string, infer V] ? V : never }) => T
): T {
  // Get all signal values
  const values = deps.map(([name, defaultValue]) => useSignal(name, defaultValue))

  // Memoize the computed value
  return useMemo(() => compute(values as any), [values, compute])
}

/**
 * Hook to persist a value to localStorage with automatic sync.
 *
 * @param key - The localStorage key
 * @param defaultValue - Default value if not in storage
 * @returns [value, setValue] tuple
 *
 * @example
 * const [theme, setTheme] = useLocalStorage('theme', 'dark')
 */
export function useLocalStorage<T>(
  key: string,
  defaultValue: T
): [T, (value: T | ((prev: T) => T)) => void] {
  // Get initial value from localStorage or use default
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return defaultValue
    }
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error)
      return defaultValue
    }
  })

  // Update localStorage when value changes
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      try {
        const valueToStore = value instanceof Function ? value(storedValue) : value
        setStoredValue(valueToStore)
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(key, JSON.stringify(valueToStore))
        }
      } catch (error) {
        console.warn(`Error setting localStorage key "${key}":`, error)
      }
    },
    [key, storedValue]
  )

  // Listen for changes from other tabs
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key && e.newValue !== null) {
        try {
          setStoredValue(JSON.parse(e.newValue))
        } catch (error) {
          console.warn(`Error parsing localStorage change for key "${key}":`, error)
        }
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [key])

  return [storedValue, setValue]
}

/**
 * Hook that debounces a value.
 *
 * @param value - The value to debounce
 * @param delay - Delay in milliseconds
 * @returns The debounced value
 *
 * @example
 * const [search, setSearch] = useState('')
 * const debouncedSearch = useDebounce(search, 300)
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(timer)
    }
  }, [value, delay])

  return debouncedValue
}

/**
 * Hook that creates a debounced callback.
 *
 * @param callback - The callback to debounce
 * @param delay - Delay in milliseconds
 * @returns The debounced callback
 *
 * @example
 * const debouncedSave = useDebouncedCallback((value) => save(value), 500)
 */
export function useDebouncedCallback<T extends (...args: any[]) => any>(
  callback: T,
  delay: number
): (...args: Parameters<T>) => void {
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>()
  const callbackRef = useRef(callback)

  // Keep callback ref updated
  useEffect(() => {
    callbackRef.current = callback
  }, [callback])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  return useCallback(
    (...args: Parameters<T>) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
      timeoutRef.current = setTimeout(() => {
        callbackRef.current(...args)
      }, delay)
    },
    [delay]
  )
}

/**
 * Hook that throttles a value.
 *
 * @param value - The value to throttle
 * @param interval - Minimum interval between updates in milliseconds
 * @returns The throttled value
 */
export function useThrottle<T>(value: T, interval: number): T {
  const [throttledValue, setThrottledValue] = useState<T>(value)
  const lastUpdated = useRef<number>(Date.now())

  useEffect(() => {
    const now = Date.now()
    const timeSinceLastUpdate = now - lastUpdated.current

    if (timeSinceLastUpdate >= interval) {
      lastUpdated.current = now
      setThrottledValue(value)
    } else {
      const timer = setTimeout(() => {
        lastUpdated.current = Date.now()
        setThrottledValue(value)
      }, interval - timeSinceLastUpdate)

      return () => clearTimeout(timer)
    }
  }, [value, interval])

  return throttledValue
}

/**
 * Hook for debounced signal updates to the server.
 *
 * @param signalName - The signal name
 * @param defaultValue - Default value
 * @param delay - Debounce delay in milliseconds
 * @returns [value, setValue, debouncedValue] tuple
 *
 * @example
 * const [search, setSearch, debouncedSearch] = useSignalDebounced('search', '', 300)
 */
export function useSignalDebounced<T>(
  signalName: string,
  defaultValue: T,
  delay: number = 300
): [T, (value: T) => void, T] {
  const serverValue = useSignal(signalName, defaultValue)
  const sendUpdate = useEvent(`${signalName}:input`)

  const [localValue, setLocalValue] = useState<T>(serverValue)
  const debouncedValue = useDebounce(localValue, delay)

  // Sync local value with server when server value changes
  useEffect(() => {
    setLocalValue(serverValue)
  }, [serverValue])

  // Send debounced value to server
  useEffect(() => {
    if (debouncedValue !== serverValue) {
      sendUpdate({ value: debouncedValue })
    }
  }, [debouncedValue, serverValue, sendUpdate])

  return [localValue, setLocalValue, debouncedValue]
}

/**
 * Hook to track previous value.
 *
 * @param value - Current value
 * @returns Previous value (undefined on first render)
 */
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}

/**
 * Hook to run effect only on updates, not on mount.
 *
 * @param effect - Effect callback
 * @param deps - Dependencies
 */
export function useUpdateEffect(
  effect: () => void | (() => void),
  deps: React.DependencyList
): void {
  const isFirstMount = useRef(true)

  useEffect(() => {
    if (isFirstMount.current) {
      isFirstMount.current = false
      return
    }
    return effect()
  }, deps)
}

/**
 * Hook that returns true after a delay.
 * Useful for delayed loading states.
 *
 * @param delay - Delay in milliseconds before returning true
 * @param immediate - If true, starts as true and becomes false after delay
 * @returns Boolean value
 */
export function useTimeout(delay: number, immediate = false): boolean {
  const [ready, setReady] = useState(immediate)

  useEffect(() => {
    const timer = setTimeout(() => {
      setReady(!immediate)
    }, delay)

    return () => clearTimeout(timer)
  }, [delay, immediate])

  return ready
}

/**
 * Hook for interval-based updates.
 *
 * @param callback - Function to call on each interval
 * @param delay - Interval delay in milliseconds (null to pause)
 */
export function useInterval(callback: () => void, delay: number | null): void {
  const savedCallback = useRef(callback)

  useEffect(() => {
    savedCallback.current = callback
  }, [callback])

  useEffect(() => {
    if (delay === null) return

    const tick = () => savedCallback.current()
    const id = setInterval(tick, delay)

    return () => clearInterval(id)
  }, [delay])
}
