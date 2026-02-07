/**
 * Form binding utilities for Cacao v2.
 *
 * Provides hooks for easily binding form inputs to server signals.
 */

import { useCallback, ChangeEvent } from 'react'
import { useSignal, useEvent } from './hooks'

/**
 * Creates a bound input that syncs with a server signal.
 *
 * @param name - The signal name
 * @param defaultValue - Default value if signal not in state
 * @returns Props to spread on an input element
 *
 * @example
 * const nameProps = useSignalInput('name', '')
 * <Input {...nameProps} />
 */
export function useSignalInput(name: string, defaultValue: string = '') {
  const value = useSignal<string>(name, defaultValue)
  const sendInput = useEvent(`${name}:input`)

  const onChange = useCallback(
    (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      sendInput({ value: e.target.value })
    },
    [sendInput]
  )

  return { value, onChange }
}

/**
 * Creates a bound select that syncs with a server signal.
 *
 * @param name - The signal name
 * @param defaultValue - Default value if signal not in state
 * @returns Props to spread on a select element
 */
export function useSignalSelect(name: string, defaultValue: string = '') {
  const value = useSignal<string>(name, defaultValue)
  const sendInput = useEvent(`${name}:input`)

  const onChange = useCallback(
    (e: ChangeEvent<HTMLSelectElement>) => {
      sendInput({ value: e.target.value })
    },
    [sendInput]
  )

  return { value, onChange }
}

/**
 * Creates a bound checkbox that syncs with a server signal.
 *
 * @param name - The signal name
 * @param defaultValue - Default value if signal not in state
 * @returns Props to spread on a checkbox element
 */
export function useSignalCheckbox(name: string, defaultValue: boolean = false) {
  const checked = useSignal<boolean>(name, defaultValue)
  const sendInput = useEvent(`${name}:input`)

  const onChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      sendInput({ value: e.target.checked })
    },
    [sendInput]
  )

  return { checked, onChange }
}

/**
 * Creates a bound switch that syncs with a server signal.
 * Same as useSignalCheckbox but named for semantic clarity.
 */
export function useSignalSwitch(name: string, defaultValue: boolean = false) {
  return useSignalCheckbox(name, defaultValue)
}

/**
 * Creates a form object with multiple bound fields.
 *
 * @param fields - Object mapping field names to default values
 * @returns Object with field props and submit function
 *
 * @example
 * const form = useSignalForm({
 *   name: '',
 *   email: '',
 *   agreed: false,
 * })
 *
 * <Input {...form.fields.name} />
 * <Input {...form.fields.email} />
 * <Checkbox {...form.fields.agreed} />
 * <Button onClick={form.submit}>Submit</Button>
 */
export function useSignalForm<T extends Record<string, string | boolean | number>>(
  fields: T
): {
  fields: {
    [K in keyof T]: T[K] extends boolean
      ? { checked: boolean; onChange: (e: ChangeEvent<HTMLInputElement>) => void }
      : { value: T[K]; onChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => void }
  }
  values: T
  submit: (eventName?: string) => void
} {
  const values = {} as T
  const fieldProps = {} as any

  for (const [name, defaultValue] of Object.entries(fields)) {
    if (typeof defaultValue === 'boolean') {
      const checked = useSignal<boolean>(name, defaultValue)
      const sendInput = useEvent(`${name}:input`)

      values[name as keyof T] = checked as T[keyof T]
      fieldProps[name] = {
        checked,
        onChange: (e: ChangeEvent<HTMLInputElement>) => {
          sendInput({ value: e.target.checked })
        },
      }
    } else {
      const value = useSignal<string | number>(name, defaultValue)
      const sendInput = useEvent(`${name}:input`)

      values[name as keyof T] = value as T[keyof T]
      fieldProps[name] = {
        value,
        onChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
          sendInput({ value: e.target.value })
        },
      }
    }
  }

  const submitEvent = useEvent('form:submit')
  const submit = useCallback(
    (eventName?: string) => {
      if (eventName) {
        const customSubmit = useEvent(eventName)
        customSubmit(values as Record<string, unknown>)
      } else {
        submitEvent(values as Record<string, unknown>)
      }
    },
    [submitEvent, values]
  )

  return { fields: fieldProps, values, submit }
}
