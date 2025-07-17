import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { versionsApi } from '../services/api'

interface VersionsState {
  currentVersion: string
  recentChanges: any[]
  summary: any
  loading: boolean
  error: string | null
}

const initialState: VersionsState = {
  currentVersion: '0.0.0',
  recentChanges: [],
  summary: null,
  loading: false,
  error: null,
}

export const fetchVersions = createAsyncThunk(
  'versions/fetchVersions',
  async () => {
    const response = await versionsApi.getVersions()
    return response.data
  }
)

export const bumpVersion = createAsyncThunk(
  'versions/bumpVersion',
  async ({ type, message }: { type: string; message?: string }) => {
    const response = await versionsApi.bumpVersion(type, message)
    return response.data
  }
)

const versionsSlice = createSlice({
  name: 'versions',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchVersions.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchVersions.fulfilled, (state, action) => {
        state.loading = false
        state.currentVersion = action.payload.current_version
        state.recentChanges = action.payload.recent_changes
        state.summary = action.payload.summary
      })
      .addCase(fetchVersions.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch versions'
      })
  },
})

export const { clearError } = versionsSlice.actions
export default versionsSlice.reducer