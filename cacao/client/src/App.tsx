import { CacaoProvider, useSignal, useEvent, useConnectionStatus } from './cacao'

function Counter() {
  const count = useSignal<number>('count', 0)
  const increment = useEvent('increment')
  const decrement = useEvent('decrement')
  const reset = useEvent('reset')
  const status = useConnectionStatus()

  return (
    <div style={styles.container}>
      <div style={styles.statusBadge(status === 'connected')}>
        {status}
      </div>

      <h1 style={styles.title}>Cacao v2 Counter</h1>

      <div style={styles.counter}>
        <span style={styles.count}>{count}</span>
      </div>

      <div style={styles.buttons}>
        <button
          style={styles.button}
          onClick={() => decrement()}
        >
          -
        </button>
        <button
          style={styles.button}
          onClick={() => reset()}
        >
          Reset
        </button>
        <button
          style={styles.button}
          onClick={() => increment()}
        >
          +
        </button>
      </div>

      <div style={styles.buttons}>
        <button
          style={{ ...styles.button, ...styles.smallButton }}
          onClick={() => decrement({ amount: 10 })}
        >
          -10
        </button>
        <button
          style={{ ...styles.button, ...styles.smallButton }}
          onClick={() => increment({ amount: 10 })}
        >
          +10
        </button>
      </div>

      <p style={styles.hint}>
        Open multiple browser tabs to see session isolation in action!
      </p>
    </div>
  )
}

export default function App() {
  return (
    <CacaoProvider
      url="ws://localhost:1502/ws"
      onConnect={() => console.log('Connected to Cacao server')}
      onDisconnect={() => console.log('Disconnected from Cacao server')}
      onError={(err) => console.error('Cacao error:', err)}
    >
      <Counter />
    </CacaoProvider>
  )
}

// Inline styles for the example
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    backgroundColor: '#1a1a2e',
    color: '#eee',
  },
  statusBadge: (connected: boolean) => ({
    position: 'fixed' as const,
    top: '1rem',
    right: '1rem',
    padding: '0.5rem 1rem',
    borderRadius: '9999px',
    fontSize: '0.875rem',
    fontWeight: 500,
    backgroundColor: connected ? '#10b981' : '#ef4444',
    color: 'white',
  }),
  title: {
    fontSize: '2rem',
    fontWeight: 600,
    marginBottom: '2rem',
    color: '#a78bfa',
  },
  counter: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '200px',
    height: '200px',
    borderRadius: '50%',
    backgroundColor: '#16213e',
    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.3)',
    marginBottom: '2rem',
  },
  count: {
    fontSize: '4rem',
    fontWeight: 700,
    color: '#f0f0f0',
  },
  buttons: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '1rem',
  },
  button: {
    padding: '1rem 2rem',
    fontSize: '1.5rem',
    fontWeight: 600,
    border: 'none',
    borderRadius: '12px',
    backgroundColor: '#7c3aed',
    color: 'white',
    cursor: 'pointer',
    transition: 'all 0.2s',
    minWidth: '80px',
  },
  smallButton: {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
  },
  hint: {
    marginTop: '2rem',
    color: '#888',
    fontSize: '0.875rem',
  },
}
