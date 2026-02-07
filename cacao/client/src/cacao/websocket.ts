/**
 * WebSocket client with automatic reconnection for Cacao v2.
 */

import type { ServerMessage, ClientMessage, ConnectionStatus } from './types'

export interface WebSocketClientOptions {
  url: string
  autoReconnect?: boolean
  reconnectDelay?: number
  maxReconnectAttempts?: number
  onMessage?: (message: ServerMessage) => void
  onStatusChange?: (status: ConnectionStatus) => void
  onError?: (error: Error) => void
}

export class WebSocketClient {
  private ws: WebSocket | null = null
  private url: string
  private autoReconnect: boolean
  private reconnectDelay: number
  private maxReconnectAttempts: number
  private reconnectAttempts = 0
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null
  private status: ConnectionStatus = 'disconnected'
  private messageQueue: ClientMessage[] = []

  private onMessage?: (message: ServerMessage) => void
  private onStatusChange?: (status: ConnectionStatus) => void
  private onError?: (error: Error) => void

  constructor(options: WebSocketClientOptions) {
    this.url = options.url
    this.autoReconnect = options.autoReconnect ?? true
    this.reconnectDelay = options.reconnectDelay ?? 1000
    this.maxReconnectAttempts = options.maxReconnectAttempts ?? 10
    this.onMessage = options.onMessage
    this.onStatusChange = options.onStatusChange
    this.onError = options.onError
  }

  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return // Already connected
    }

    this.setStatus('connecting')

    try {
      this.ws = new WebSocket(this.url)

      this.ws.onopen = () => {
        this.setStatus('connected')
        this.reconnectAttempts = 0
        this.flushMessageQueue()
      }

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as ServerMessage
          this.onMessage?.(message)
        } catch (error) {
          this.onError?.(new Error(`Failed to parse message: ${event.data}`))
        }
      }

      this.ws.onclose = () => {
        this.setStatus('disconnected')
        this.ws = null

        if (this.autoReconnect) {
          this.scheduleReconnect()
        }
      }

      this.ws.onerror = () => {
        this.onError?.(new Error('WebSocket error'))
      }
    } catch (error) {
      this.onError?.(error instanceof Error ? error : new Error(String(error)))
      this.setStatus('disconnected')

      if (this.autoReconnect) {
        this.scheduleReconnect()
      }
    }
  }

  disconnect(): void {
    this.autoReconnect = false
    this.cancelReconnect()

    if (this.ws) {
      this.ws.close()
      this.ws = null
    }

    this.setStatus('disconnected')
  }

  send(message: ClientMessage): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      // Queue message for when connection is restored
      this.messageQueue.push(message)
    }
  }

  sendEvent(name: string, data: Record<string, unknown> = {}): void {
    this.send({
      type: 'event',
      name,
      data,
    })
  }

  getStatus(): ConnectionStatus {
    return this.status
  }

  isConnected(): boolean {
    return this.status === 'connected'
  }

  private setStatus(status: ConnectionStatus): void {
    if (this.status !== status) {
      this.status = status
      this.onStatusChange?.(status)
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.onError?.(new Error('Max reconnection attempts reached'))
      return
    }

    this.cancelReconnect()
    this.setStatus('reconnecting')

    // Exponential backoff with jitter
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts) +
        Math.random() * 1000,
      30000 // Max 30 seconds
    )

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectAttempts++
      this.connect()
    }, delay)
  }

  private cancelReconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout)
      this.reconnectTimeout = null
    }
  }

  private flushMessageQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift()
      if (message) {
        this.send(message)
      }
    }
  }
}
