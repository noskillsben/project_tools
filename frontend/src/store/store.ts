import { configureStore } from '@reduxjs/toolkit'
import todosReducer from './todosSlice'
import versionsReducer from './versionsSlice'
import intelligenceReducer from './intelligenceSlice'
import socketReducer from './socketSlice'

export const store = configureStore({
  reducer: {
    todos: todosReducer,
    versions: versionsReducer,
    intelligence: intelligenceReducer,
    socket: socketReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['socket/initialize'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch