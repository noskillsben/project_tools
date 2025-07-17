import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { todosApi } from '../services/api'

export interface Todo {
  id: number
  title: string
  description: string
  priority: number
  status: string
  category: string
  created_date: string
  target_date?: string
  completed_date?: string
  notes?: string
}

interface TodosState {
  todos: Todo[]
  loading: boolean
  error: string | null
  summary: {
    total: number
    by_status: Record<string, number>
    by_category: Record<string, number>
    by_priority: Record<string, number>
    high_priority_count: number
    in_progress_count: number
    blocked_count: number
    unblocked_count: number
  } | null
  dependencies: {
    blocked: Todo[]
    unblocked: Todo[]
  } | null
}

const initialState: TodosState = {
  todos: [],
  loading: false,
  error: null,
  summary: null,
  dependencies: null,
}

// Async thunks
export const fetchTodos = createAsyncThunk(
  'todos/fetchTodos',
  async (filters?: { status?: string; category?: string; min_priority?: number }) => {
    const response = await todosApi.getTodos(filters)
    return response.data
  }
)

export const createTodo = createAsyncThunk(
  'todos/createTodo',
  async (todoData: Partial<Todo>) => {
    const response = await todosApi.createTodo(todoData)
    return response.data
  }
)

export const updateTodo = createAsyncThunk(
  'todos/updateTodo',
  async ({ id, updates }: { id: number; updates: Partial<Todo> }) => {
    const response = await todosApi.updateTodo(id, updates)
    return response.data
  }
)

export const deleteTodo = createAsyncThunk(
  'todos/deleteTodo',
  async (id: number) => {
    await todosApi.deleteTodo(id)
    return id
  }
)

export const completeTodo = createAsyncThunk(
  'todos/completeTodo',
  async ({ id, withChangelog = false }: { id: number; withChangelog?: boolean }) => {
    const response = await todosApi.completeTodo(id, { with_changelog: withChangelog })
    return response.data
  }
)

export const fetchSummary = createAsyncThunk(
  'todos/fetchSummary',
  async () => {
    const response = await todosApi.getSummary()
    return response.data
  }
)

export const fetchDependencies = createAsyncThunk(
  'todos/fetchDependencies',
  async () => {
    const response = await todosApi.getDependencies()
    return response.data
  }
)

export const addDependency = createAsyncThunk(
  'todos/addDependency',
  async ({ todoId, dependsOnId }: { todoId: number; dependsOnId: number }) => {
    const response = await todosApi.addDependency(todoId, dependsOnId)
    return response.data
  }
)

const todosSlice = createSlice({
  name: 'todos',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
    // Real-time updates from WebSocket
    todoCreated: (state, action: PayloadAction<Todo>) => {
      state.todos.unshift(action.payload)
    },
    todoUpdated: (state, action: PayloadAction<Todo>) => {
      const index = state.todos.findIndex(todo => todo.id === action.payload.id)
      if (index !== -1) {
        state.todos[index] = action.payload
      }
    },
    todoDeleted: (state, action: PayloadAction<number>) => {
      state.todos = state.todos.filter(todo => todo.id !== action.payload)
    },
    todoCompleted: (state, action: PayloadAction<Todo>) => {
      const index = state.todos.findIndex(todo => todo.id === action.payload.id)
      if (index !== -1) {
        state.todos[index] = action.payload
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch todos
      .addCase(fetchTodos.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.loading = false
        state.todos = action.payload.todos
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch todos'
      })
      
      // Create todo
      .addCase(createTodo.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(createTodo.fulfilled, (state, action) => {
        state.loading = false
        state.todos.unshift(action.payload.todo)
      })
      .addCase(createTodo.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to create todo'
      })
      
      // Update todo
      .addCase(updateTodo.fulfilled, (state, action) => {
        const index = state.todos.findIndex(todo => todo.id === action.payload.todo.id)
        if (index !== -1) {
          state.todos[index] = action.payload.todo
        }
      })
      
      // Delete todo
      .addCase(deleteTodo.fulfilled, (state, action) => {
        state.todos = state.todos.filter(todo => todo.id !== action.payload)
      })
      
      // Complete todo
      .addCase(completeTodo.fulfilled, (state, action) => {
        const index = state.todos.findIndex(todo => todo.id === action.payload.todo.id)
        if (index !== -1) {
          state.todos[index] = action.payload.todo
        }
      })
      
      // Fetch summary
      .addCase(fetchSummary.fulfilled, (state, action) => {
        state.summary = action.payload.summary
      })
      
      // Fetch dependencies
      .addCase(fetchDependencies.fulfilled, (state, action) => {
        state.dependencies = action.payload.dependencies
      })
  },
})

export const { 
  clearError, 
  todoCreated, 
  todoUpdated, 
  todoDeleted, 
  todoCompleted 
} = todosSlice.actions

export default todosSlice.reducer