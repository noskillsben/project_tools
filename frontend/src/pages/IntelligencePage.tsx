import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '../store/store'
import { fetchIntelligenceStatus, fetchRecommendations } from '../store/intelligenceSlice'
import { Brain, Lightbulb, TrendingUp } from 'lucide-react'

const IntelligencePage = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { status, recommendations, dashboard } = useSelector(
    (state: RootState) => state.intelligence
  )

  useEffect(() => {
    dispatch(fetchIntelligenceStatus())
    dispatch(fetchRecommendations())
  }, [dispatch])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Project Intelligence</h1>
        <p className="text-muted-foreground mt-2">
          AI-assisted insights and recommendations for your project
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Intelligence Status */}
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Brain className="h-6 w-6 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Intelligence Status</h2>
          </div>
          
          {status ? (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Active</span>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  status.intelligence_active 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {status.intelligence_active ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              
              {status.intelligence_active && status.components && (
                <div className="space-y-2">
                  <h3 className="text-sm font-medium text-foreground">Components</h3>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {Object.entries(status.components).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="capitalize">{key.replace('_', ' ')}</span>
                        <span className={value ? 'text-green-600' : 'text-red-600'}>
                          {value ? '✓' : '✗'}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-muted-foreground">Loading intelligence status...</p>
          )}
        </div>

        {/* Recommendations */}
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Lightbulb className="h-6 w-6 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">Recommendations</h2>
          </div>
          
          {recommendations.length === 0 ? (
            <p className="text-muted-foreground">No recommendations available</p>
          ) : (
            <div className="space-y-3">
              {recommendations.map((recommendation, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-3 p-3 bg-accent rounded-md"
                >
                  <TrendingUp className="h-4 w-4 mt-0.5 text-primary flex-shrink-0" />
                  <p className="text-sm text-foreground">{recommendation}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Intelligence Features Placeholder */}
      <div className="bg-card rounded-lg border border-border p-6">
        <h2 className="text-lg font-semibold text-foreground mb-4">Intelligence Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { name: 'Project Compass', description: 'Track project direction and goals' },
            { name: 'Task Chains', description: 'Visualize task dependencies' },
            { name: 'Reflection', description: 'Project insights and learnings' },
            { name: 'Portfolio', description: 'Multi-project management' }
          ].map((feature) => (
            <div key={feature.name} className="p-4 bg-accent rounded-md">
              <h3 className="font-medium text-foreground text-sm">{feature.name}</h3>
              <p className="text-xs text-muted-foreground mt-1">{feature.description}</p>
              <button className="mt-2 text-xs text-primary hover:text-primary/80">
                Coming Soon
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default IntelligencePage