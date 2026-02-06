/**
 * Todo Example - Cacao v2 React Client
 *
 * Demonstrates form binding and list state management.
 */

import { CacaoProvider, useSignal, useEvent, useSignalInput, useConnectionStatus } from '../../client/src/cacao'
import { Container, VStack, HStack, Box } from '../../client/src/components/layout'
import { Button, Text, Card, Badge } from '../../client/src/components/ui'
import { Input, Checkbox } from '../../client/src/components/forms'

interface Todo {
  id: number
  text: string
  completed: boolean
}

function TodoApp() {
  const todos = useSignal<Todo[]>('todos', [])
  const filterMode = useSignal<string>('filterMode', 'all')
  const status = useConnectionStatus()

  // Form bindings
  const newTodoInput = useSignalInput('newTodoText', '')

  // Events
  const addTodo = useEvent('todo:add')
  const toggleTodo = useEvent('todo:toggle')
  const deleteTodo = useEvent('todo:delete')
  const clearCompleted = useEvent('todo:clear-completed')
  const toggleAll = useEvent('todo:toggle-all')
  const setFilter = useEvent('filterMode:input')

  // Filter todos based on mode
  const filteredTodos = todos.filter((todo) => {
    if (filterMode === 'active') return !todo.completed
    if (filterMode === 'completed') return todo.completed
    return true
  })

  // Stats
  const activeCount = todos.filter((t) => !t.completed).length
  const completedCount = todos.filter((t) => t.completed).length

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    addTodo()
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addTodo()
    }
  }

  return (
    <Container size="md" py={8}>
      <VStack spacing={6}>
        {/* Header */}
        <HStack justify="space-between" style={{ width: '100%' }}>
          <Text variant="h2" style={{ margin: 0, color: '#a78bfa' }}>
            Cacao Todo
          </Text>
          <Badge variant={status === 'connected' ? 'success' : 'danger'} dot>
            {status}
          </Badge>
        </HStack>

        {/* Add Todo Form */}
        <Card style={{ width: '100%' }}>
          <form onSubmit={handleSubmit}>
            <HStack spacing={3}>
              <Box flex={1}>
                <Input
                  placeholder="What needs to be done?"
                  fullWidth
                  {...newTodoInput}
                  onKeyDown={handleKeyDown}
                />
              </Box>
              <Button type="submit" variant="primary">
                Add
              </Button>
            </HStack>
          </form>
        </Card>

        {/* Todo List */}
        {todos.length > 0 && (
          <Card style={{ width: '100%' }} padding="none">
            {/* Toggle All */}
            <Box
              p={3}
              style={{
                borderBottom: '1px solid rgba(255,255,255,0.1)',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
              }}
            >
              <Checkbox
                checked={todos.length > 0 && activeCount === 0}
                onChange={() => toggleAll()}
                label="Mark all as complete"
              />
            </Box>

            {/* Todo Items */}
            <VStack spacing={0}>
              {filteredTodos.map((todo) => (
                <Box
                  key={todo.id}
                  p={3}
                  style={{
                    borderBottom: '1px solid rgba(255,255,255,0.05)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                  }}
                >
                  <Checkbox
                    checked={todo.completed}
                    onChange={() => toggleTodo({ id: todo.id })}
                  />
                  <Text
                    style={{
                      flex: 1,
                      textDecoration: todo.completed ? 'line-through' : 'none',
                      opacity: todo.completed ? 0.5 : 1,
                      margin: 0,
                    }}
                  >
                    {todo.text}
                  </Text>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => deleteTodo({ id: todo.id })}
                    style={{ color: '#ef4444' }}
                  >
                    ×
                  </Button>
                </Box>
              ))}
            </VStack>

            {/* Footer */}
            <Box p={3} style={{ backgroundColor: 'rgba(0,0,0,0.2)' }}>
              <HStack justify="space-between" align="center">
                <Text variant="small" style={{ margin: 0 }}>
                  {activeCount} item{activeCount !== 1 ? 's' : ''} left
                </Text>

                <HStack spacing={2}>
                  {(['all', 'active', 'completed'] as const).map((mode) => (
                    <Button
                      key={mode}
                      variant={filterMode === mode ? 'primary' : 'ghost'}
                      size="sm"
                      onClick={() => setFilter({ value: mode })}
                    >
                      {mode.charAt(0).toUpperCase() + mode.slice(1)}
                    </Button>
                  ))}
                </HStack>

                {completedCount > 0 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => clearCompleted()}
                  >
                    Clear completed
                  </Button>
                )}
              </HStack>
            </Box>
          </Card>
        )}

        {/* Empty State */}
        {todos.length === 0 && (
          <Card style={{ width: '100%', textAlign: 'center' }} padding={6}>
            <Text variant="body" color="rgba(255,255,255,0.5)">
              No todos yet. Add one above!
            </Text>
          </Card>
        )}

        {/* Info */}
        <Text variant="caption" align="center">
          Double-click to edit a todo • Press Enter to add
        </Text>
      </VStack>
    </Container>
  )
}

export default function App() {
  return (
    <CacaoProvider
      url="ws://localhost:1634/ws"
      onConnect={() => console.log('Connected to Cacao server')}
      onDisconnect={() => console.log('Disconnected from Cacao server')}
      onError={(err) => console.error('Cacao error:', err)}
    >
      <TodoApp />
    </CacaoProvider>
  )
}
