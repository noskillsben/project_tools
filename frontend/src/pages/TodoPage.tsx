import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '../store/store'
import { 
  fetchTodos, 
  createTodo, 
  updateTodo, 
  deleteTodo, 
  completeTodo,
  Todo
} from '../store/todosSlice'
import { 
  Plus, 
  Search, 
  Filter, 
  Edit2, 
  Trash2, 
  Check,
  AlertCircle,
  Clock,
  CheckSquare
} from 'lucide-react'

const TodoPage = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { todos, loading, error } = useSelector((state: RootState) => state.todos)
  
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null)
  const [filters, setFilters] = useState({
    status: '',
    category: '',
    priority: '',
    search: ''
  })

  const [newTodo, setNewTodo] = useState({
    title: '',
    description: '',
    priority: 5,
    category: 'general',
    target_date: ''
  })

  useEffect(() => {
    dispatch(fetchTodos(filters.status ? { status: filters.status } : undefined))
  }, [dispatch, filters.status])

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await dispatch(createTodo(newTodo)).unwrap()
      setNewTodo({
        title: '',
        description: '',
        priority: 5,
        category: 'general',
        target_date: ''
      })
      setShowCreateForm(false)
    } catch (error) {
      console.error('Failed to create todo:', error)
    }
  }

  const handleUpdateTodo = async (id: number, updates: Partial<Todo>) => {
    try {
      await dispatch(updateTodo({ id, updates })).unwrap()
      setEditingTodo(null)
    } catch (error) {
      console.error('Failed to update todo:', error)
    }
  }

  const handleDeleteTodo = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await dispatch(deleteTodo(id)).unwrap()
      } catch (error) {
        console.error('Failed to delete todo:', error)
      }
    }
  }

  const handleCompleteTodo = async (id: number) => {
    try {
      await dispatch(completeTodo({ id })).unwrap()
    } catch (error) {
      console.error('Failed to complete todo:', error)
    }
  }

  const getPriorityColor = (priority: number) => {
    if (priority >= 9) return 'text-red-600'
    if (priority >= 7) return 'text-orange-600'
    if (priority >= 5) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'complete':
        return <CheckSquare className="h-4 w-4 text-green-600" />
      case 'in_progress':
        return <Clock className="h-4 w-4 text-yellow-600" />
      default:
        return <AlertCircle className="h-4 w-4 text-blue-600" />
    }
  }

  const filteredTodos = todos.filter(todo => {
    if (filters.search && !todo.title.toLowerCase().includes(filters.search.toLowerCase())) {
      return false
    }
    if (filters.category && todo.category !== filters.category) {
      return false
    }
    if (filters.priority) {
      const minPriority = filters.priority === 'high' ? 8 : 
                         filters.priority === 'medium' ? 4 : 1
      const maxPriority = filters.priority === 'high' ? 10 : 
                         filters.priority === 'medium' ? 7 : 3
      if (todo.priority < minPriority || todo.priority > maxPriority) {
        return false
      }
    }
    return true
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Todos</h1>
          <p className="text-muted-foreground mt-2">
            Manage your tasks and track progress
          </p>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="flex items-center space-x-2 bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90"
        >
          <Plus className="h-4 w-4" />
          <span>Add Todo</span>
        </button>
      </div>

      {/* Filters */}
      <div className="bg-card rounded-lg border border-border p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Search
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search todos..."
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                className="w-full pl-10 pr-4 py-2 border border-border rounded-md bg-background text-foreground"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
            >
              <option value="">All Statuses</option>
              <option value="todo">Todo</option>
              <option value="in_progress">In Progress</option>
              <option value="complete">Complete</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Priority
            </label>
            <select
              value={filters.priority}
              onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
            >
              <option value="">All Priorities</option>
              <option value="high">High (8-10)</option>
              <option value="medium">Medium (4-7)</option>
              <option value="low">Low (1-3)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Category
            </label>
            <select
              value={filters.category}
              onChange={(e) => setFilters({ ...filters, category: e.target.value })}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
            >
              <option value="">All Categories</option>
              <option value="bug">Bug</option>
              <option value="feature">Feature</option>
              <option value="enhancement">Enhancement</option>
              <option value="docs">Documentation</option>
              <option value="refactor">Refactor</option>
              <option value="test">Test</option>
            </select>
          </div>
        </div>
      </div>

      {/* Create Todo Form */}
      {showCreateForm && (
        <div className="bg-card rounded-lg border border-border p-6">
          <h2 className="text-lg font-semibold text-foreground mb-4">Create New Todo</h2>
          <form onSubmit={handleCreateTodo} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                Title *
              </label>
              <input
                type="text"
                required
                value={newTodo.title}
                onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
                className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
                placeholder="Enter todo title..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                Description
              </label>
              <textarea
                value={newTodo.description}
                onChange={(e) => setNewTodo({ ...newTodo, description: e.target.value })}
                className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
                rows={3}
                placeholder="Enter description..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  Priority (1-10)
                </label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={newTodo.priority}
                  onChange={(e) => setNewTodo({ ...newTodo, priority: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  Category
                </label>
                <select
                  value={newTodo.category}
                  onChange={(e) => setNewTodo({ ...newTodo, category: e.target.value })}
                  className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
                >
                  <option value="general">General</option>
                  <option value="bug">Bug</option>
                  <option value="feature">Feature</option>
                  <option value="enhancement">Enhancement</option>
                  <option value="docs">Documentation</option>
                  <option value="refactor">Refactor</option>
                  <option value="test">Test</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-1">
                  Target Date
                </label>
                <input
                  type="date"
                  value={newTodo.target_date}
                  onChange={(e) => setNewTodo({ ...newTodo, target_date: e.target.value })}
                  className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground"
                />
              </div>
            </div>

            <div className="flex space-x-4">
              <button
                type="submit"
                className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90"
              >
                Create Todo
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="bg-secondary text-secondary-foreground px-4 py-2 rounded-md hover:bg-secondary/90"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Todos List */}
      <div className="bg-card rounded-lg border border-border">
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <p className="text-muted-foreground mt-2">Loading todos...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-destructive">{error}</p>
          </div>
        ) : filteredTodos.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground">No todos found</p>
          </div>
        ) : (
          <div className="divide-y divide-border">
            {filteredTodos.map((todo) => (
              <div
                key={todo.id}
                className="p-4 hover:bg-accent transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(todo.status)}
                      <h3 className="text-sm font-medium text-foreground truncate">
                        {todo.title}
                      </h3>
                      <span className={`text-sm font-medium ${getPriorityColor(todo.priority)}`}>
                        P{todo.priority}
                      </span>
                      <span className="px-2 py-1 text-xs bg-secondary text-secondary-foreground rounded-full">
                        {todo.category}
                      </span>
                    </div>
                    {todo.description && (
                      <p className="text-sm text-muted-foreground mt-1 truncate">
                        {todo.description}
                      </p>
                    )}
                    <div className="flex items-center space-x-4 mt-2 text-xs text-muted-foreground">
                      <span>Created: {todo.created_date}</span>
                      {todo.target_date && <span>Due: {todo.target_date}</span>}
                      {todo.completed_date && <span>Completed: {todo.completed_date}</span>}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {todo.status !== 'complete' && (
                      <button
                        onClick={() => handleCompleteTodo(todo.id)}
                        className="p-1 text-green-600 hover:bg-green-100 rounded"
                        title="Complete"
                      >
                        <Check className="h-4 w-4" />
                      </button>
                    )}
                    <button
                      onClick={() => setEditingTodo(todo)}
                      className="p-1 text-blue-600 hover:bg-blue-100 rounded"
                      title="Edit"
                    >
                      <Edit2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteTodo(todo.id)}
                      className="p-1 text-red-600 hover:bg-red-100 rounded"
                      title="Delete"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default TodoPage