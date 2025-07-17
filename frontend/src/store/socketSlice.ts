import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { io, Socket } from 'socket.io-client'
import { AppDispatch } from './store'
import { todoCreated, todoUpdated, todoDeleted, todoCompleted } from './todosSlice'

interface SocketState {
  connected: boolean
  socket: Socket | null
}

const initialState: SocketState = {
  connected: false,
  socket: null,
}

const socketSlice = createSlice({
  name: 'socket',
  initialState,
  reducers: {
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.connected = action.payload
    },
    setSocket: (state, action: PayloadAction<Socket | null>) => {
      state.socket = action.payload
    },
  },
})

export const { setConnected, setSocket } = socketSlice.actions

// Thunk to initialize socket connection
export const initializeSocket = () => (dispatch: AppDispatch) => {
  const socket = io('http://127.0.0.1:5000', {
    autoConnect: true,
  })

  socket.on('connect', () => {
    console.log('Connected to server')
    dispatch(setConnected(true))
    
    // Join default project room
    socket.emit('join_project', { project_id: 'default' })
  })

  socket.on('disconnect', () => {
    console.log('Disconnected from server')
    dispatch(setConnected(false))
  })

  // Listen for real-time todo updates
  socket.on('todo_created', (data) => {
    dispatch(todoCreated(data.todo))
  })

  socket.on('todo_updated', (data) => {
    dispatch(todoUpdated(data.todo))
  })

  socket.on('todo_deleted', (data) => {
    dispatch(todoDeleted(data.todo_id))
  })

  socket.on('todo_completed', (data) => {
    dispatch(todoCompleted(data.todo))
  })

  dispatch(setSocket(socket))
}

export default socketSlice.reducer