import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '../store/store'
import { fetchVersions } from '../store/versionsSlice'
import { GitBranch, Clock, Tag } from 'lucide-react'

const VersionPage = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { currentVersion, recentChanges, summary, loading } = useSelector(
    (state: RootState) => state.versions
  )

  useEffect(() => {
    dispatch(fetchVersions())
  }, [dispatch])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Version Management</h1>
        <p className="text-muted-foreground mt-2">
          Track version history and manage releases
        </p>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="text-muted-foreground mt-2">Loading version data...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Current Version Card */}
          <div className="bg-card rounded-lg border border-border p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Tag className="h-6 w-6 text-primary" />
              <h2 className="text-lg font-semibold text-foreground">Current Version</h2>
            </div>
            <div className="text-3xl font-bold text-primary mb-2">{currentVersion}</div>
            {summary && (
              <div className="space-y-2 text-sm text-muted-foreground">
                <p>Last updated: {summary.version_date || 'Unknown'}</p>
                <p>Total versions: {summary.total_versions || 0}</p>
              </div>
            )}
          </div>

          {/* Recent Changes */}
          <div className="lg:col-span-2 bg-card rounded-lg border border-border p-6">
            <div className="flex items-center space-x-3 mb-4">
              <Clock className="h-6 w-6 text-primary" />
              <h2 className="text-lg font-semibold text-foreground">Recent Changes</h2>
            </div>
            
            {recentChanges.length === 0 ? (
              <p className="text-muted-foreground">No recent changes</p>
            ) : (
              <div className="space-y-3">
                {recentChanges.map((change, index) => (
                  <div
                    key={index}
                    className="flex items-start space-x-3 p-3 bg-accent rounded-md"
                  >
                    <GitBranch className="h-4 w-4 mt-0.5 text-muted-foreground flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-foreground">
                        {change.description}
                      </p>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-muted-foreground">
                        <span className="capitalize">{change.type}</span>
                        <span>{change.date}</span>
                        {change.author && <span>by {change.author}</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default VersionPage