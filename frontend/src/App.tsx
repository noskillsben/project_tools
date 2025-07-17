import { Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import TodoPage from './pages/TodoPage'
import VersionPage from './pages/VersionPage'
import IntelligencePage from './pages/IntelligencePage'
import { initializeSocket } from './store/socketSlice'
import { AppDispatch } from './store/store'

function App() {
  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    // Initialize WebSocket connection
    dispatch(initializeSocket())
  }, [dispatch])

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/todos" element={<TodoPage />} />
        <Route path="/versions" element={<VersionPage />} />
        <Route path="/intelligence" element={<IntelligencePage />} />
      </Routes>
    </Layout>
  )
}

export default App