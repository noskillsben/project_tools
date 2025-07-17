import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { AppDispatch, RootState } from '../store/store'
import { fetchTodos, fetchSummary } from '../store/todosSlice'
import { fetchVersions } from '../store/versionsSlice'
import { fetchRecommendations } from '../store/intelligenceSlice'
import { 
  CheckSquare, 
  GitBranch, 
  Brain, 
  TrendingUp, 
  AlertCircle,
  Clock,
  Target
} from 'lucide-react'

const Dashboard = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { todos, summary, loading: todosLoading } = useSelector((state: RootState) => state.todos)
  const { currentVersion, recentChanges } = useSelector((state: RootState) => state.versions)
  const { recommendations } = useSelector((state: RootState) => state.intelligence)

  useEffect(() => {
    dispatch(fetchTodos())
    dispatch(fetchSummary())
    dispatch(fetchVersions())
    dispatch(fetchRecommendations())
  }, [dispatch])

  const stats = [
    {
      name: 'Total Todos',
      value: summary?.total || 0,
      icon: CheckSquare,
      color: 'text-blue-600',
      href: '/todos'
    },
    {
      name: 'High Priority',
      value: summary?.high_priority_count || 0,
      icon: AlertCircle,
      color: 'text-red-600',
      href: '/todos?priority=high'
    },
    {
      name: 'In Progress',
      value: summary?.in_progress_count || 0,
      icon: Clock,
      color: 'text-yellow-600',
      href: '/todos?status=in_progress'
    },
    {
      name: 'Current Version',
      value: currentVersion,
      icon: GitBranch,
      color: 'text-green-600',
      href: '/versions'
    },
  ]

  const highPriorityTodos = todos
    .filter(todo => todo.priority >= 8 && todo.status !== 'complete')
    .slice(0, 5)

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Overview of your project management activities
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <Link
              key={stat.name}
              to={stat.href}
              className="bg-card rounded-lg border border-border p-6 hover:bg-accent transition-colors"
            >
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Icon className={`h-8 w-8 ${stat.color}`} />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-muted-foreground truncate">
                      {stat.name}
                    </dt>
                    <dd className="text-lg font-medium text-foreground">
                      {stat.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </Link>
          )
        })}
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* High Priority Todos */}
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-foreground flex items-center">
              <Target className="h-5 w-5 mr-2 text-red-600" />
              High Priority Todos
            </h2>
            <Link 
              to="/todos?priority=high" 
              className="text-sm text-primary hover:text-primary/80"
            >
              View all
            </Link>
          </div>
          
          {todosLoading ? (
            <div className="text-center py-4">
              <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
            </div>
          ) : highPriorityTodos.length === 0 ? (
            <p className="text-muted-foreground text-center py-4">
              No high priority todos
            </p>
          ) : (
            <div className="space-y-3">
              {highPriorityTodos.map((todo) => (
                <div
                  key={todo.id}
                  className="flex items-center justify-between p-3 bg-accent rounded-md"
                >
                  <div className="flex-1">
                    <h3 className="font-medium text-foreground text-sm">
                      {todo.title}
                    </h3>
                    <p className="text-xs text-muted-foreground">
                      Priority: {todo.priority} | {todo.category}
                    </p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    todo.status === 'todo' 
                      ? 'bg-blue-100 text-blue-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {todo.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Changes */}
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-foreground flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
              Recent Changes
            </h2>
            <Link 
              to="/versions" 
              className="text-sm text-primary hover:text-primary/80"
            >
              View all
            </Link>
          </div>
          
          {recentChanges.length === 0 ? (
            <p className="text-muted-foreground text-center py-4">
              No recent changes
            </p>
          ) : (
            <div className="space-y-3">
              {recentChanges.slice(0, 5).map((change, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-accent rounded-md"
                >
                  <div className="flex-1">
                    <h3 className="font-medium text-foreground text-sm">
                      {change.description}
                    </h3>
                    <p className="text-xs text-muted-foreground">
                      {change.type} • {change.date}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Workflow Recommendations */}
        {recommendations.length > 0 && (
          <div className="lg:col-span-2 bg-card rounded-lg border border-border p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-foreground flex items-center">
                <Brain className="h-5 w-5 mr-2 text-purple-600" />
                Workflow Recommendations
              </h2>
              <Link 
                to="/intelligence" 
                className="text-sm text-primary hover:text-primary/80"
              >
                View intelligence
              </Link>
            </div>
            
            <div className="space-y-2">
              {recommendations.map((recommendation, index) => (
                <div
                  key={index}
                  className="flex items-center p-3 bg-accent rounded-md"
                >
                  <div className="flex-shrink-0 w-2 h-2 bg-primary rounded-full mr-3"></div>
                  <p className="text-sm text-foreground">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard