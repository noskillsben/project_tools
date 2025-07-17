import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add any auth tokens if needed
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Todos API
export const todosApi = {
  getTodos: (filters?: { status?: string; category?: string; min_priority?: number }) =>
    api.get('/todos', { params: filters }),
  
  createTodo: (data: any) =>
    api.post('/todos', data),
  
  getTodo: (id: number) =>
    api.get(`/todos/${id}`),
  
  updateTodo: (id: number, data: any) =>
    api.put(`/todos/${id}`, data),
  
  deleteTodo: (id: number) =>
    api.delete(`/todos/${id}`),
  
  completeTodo: (id: number, data?: any) =>
    api.post(`/todos/${id}/complete`, data),
  
  getSummary: () =>
    api.get('/todos/summary'),
  
  getDependencies: () =>
    api.get('/todos/dependencies'),
  
  addDependency: (todoId: number, dependsOnId: number) =>
    api.post(`/todos/${todoId}/dependencies`, { depends_on_id: dependsOnId }),
  
  removeDependency: (todoId: number, dependsOnId: number) =>
    api.delete(`/todos/${todoId}/dependencies/${dependsOnId}`),
  
  exportTodos: (format: string = 'json') =>
    api.get('/todos/export', { params: { format } }),
}

// Versions API
export const versionsApi = {
  getVersions: (days?: number) =>
    api.get('/versions', { params: { days } }),
  
  getCurrentVersion: () =>
    api.get('/versions/current'),
  
  getChanges: (days?: number, type?: string) =>
    api.get('/versions/changes', { params: { days, type } }),
  
  addChange: (data: { type: string; description: string; todo_id?: number }) =>
    api.post('/versions/changes', data),
  
  bumpVersion: (type: string, message?: string) =>
    api.post('/versions/bump', { type, message }),
  
  getHistory: () =>
    api.get('/versions/history'),
  
  getSummary: () =>
    api.get('/versions/summary'),
  
  getGitStatus: () =>
    api.get('/versions/git/status'),
  
  getChangelog: () =>
    api.get('/versions/changelog'),
  
  getStats: () =>
    api.get('/versions/stats'),
}

// Intelligence API
export const intelligenceApi = {
  getStatus: () =>
    api.get('/intelligence/status'),
  
  initialize: (data?: { project_name?: string; force?: boolean }) =>
    api.post('/intelligence/initialize', data),
  
  getRecommendations: () =>
    api.get('/intelligence/recommendations'),
  
  getSessionFocus: () =>
    api.get('/intelligence/session-focus'),
  
  getProjectHealth: () =>
    api.get('/intelligence/health'),
  
  getEnhancements: () =>
    api.get('/intelligence/enhancements'),
  
  getCompass: () =>
    api.get('/intelligence/compass'),
  
  getDirection: () =>
    api.get('/intelligence/direction'),
  
  getTaskChains: () =>
    api.get('/intelligence/task-chains'),
  
  getReflection: () =>
    api.get('/intelligence/reflection'),
  
  getPortfolio: () =>
    api.get('/intelligence/portfolio'),
  
  getDashboard: () =>
    api.get('/intelligence/dashboard'),
}

// General API
export const generalApi = {
  getStatus: () =>
    api.get('/status'),
  
  getHealth: () =>
    api.get('/health'),
}

export default api