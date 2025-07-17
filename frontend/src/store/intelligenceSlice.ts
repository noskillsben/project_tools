import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { intelligenceApi } from '../services/api'

interface IntelligenceState {
  status: any
  recommendations: string[]
  dashboard: any
  loading: boolean
  error: string | null
}

const initialState: IntelligenceState = {
  status: null,
  recommendations: [],
  dashboard: null,
  loading: false,
  error: null,
}

export const fetchIntelligenceStatus = createAsyncThunk(
  'intelligence/fetchStatus',
  async () => {
    const response = await intelligenceApi.getStatus()
    return response.data
  }
)

export const fetchRecommendations = createAsyncThunk(
  'intelligence/fetchRecommendations',
  async () => {
    const response = await intelligenceApi.getRecommendations()
    return response.data
  }
)

export const fetchDashboard = createAsyncThunk(
  'intelligence/fetchDashboard',
  async () => {
    const response = await intelligenceApi.getDashboard()
    return response.data
  }
)

const intelligenceSlice = createSlice({
  name: 'intelligence',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchIntelligenceStatus.fulfilled, (state, action) => {
        state.status = action.payload
      })
      .addCase(fetchRecommendations.fulfilled, (state, action) => {
        state.recommendations = action.payload.recommendations
      })
      .addCase(fetchDashboard.fulfilled, (state, action) => {
        state.dashboard = action.payload.dashboard
      })
  },
})

export const { clearError } = intelligenceSlice.actions
export default intelligenceSlice.reducer