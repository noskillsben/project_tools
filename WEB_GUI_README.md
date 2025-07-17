# Project Tools Web GUI

A modern Flask + React web interface for the Project Tools project management system. Provides an intuitive dashboard for managing todos, tracking versions, and visualizing project intelligence data.

## Features

### 🎯 Todo Management
- **Interactive Dashboard**: View, create, edit, and delete todos with real-time updates
- **Advanced Filtering**: Filter by status, category, priority, and search terms
- **Priority Management**: Visual priority indicators with color coding
- **Dependency Tracking**: Manage todo dependencies and visualize relationships
- **Status Tracking**: Todo, In Progress, Complete status management
- **Categories**: Organize todos by bug, feature, enhancement, docs, refactor, test

### 📊 Version Management
- **Current Version Display**: See your current project version at a glance
- **Changelog Tracking**: View recent changes and version history
- **Version Bumping**: Increment major, minor, or patch versions
- **Git Integration**: Track git status and repository information
- **Change Statistics**: Visual metrics for project activity

### 🧠 Project Intelligence
- **AI-Assisted Insights**: Get recommendations for workflow optimization
- **Project Health**: Comprehensive project health evaluation
- **Session Focus**: AI suggestions for next working session priorities
- **Component Status**: Track status of different intelligence components
- **Enhancement Opportunities**: Identify areas for AI-assisted improvements

### 🔄 Real-time Features
- **WebSocket Integration**: Live updates across all connected clients
- **Collaborative Editing**: Multiple users can work simultaneously
- **Instant Notifications**: Real-time todo updates, completions, and changes
- **Connection Status**: Visual indicator of server connection

## Technology Stack

### Backend
- **Flask**: Web framework with REST API endpoints
- **Flask-SocketIO**: Real-time WebSocket communication
- **Flask-CORS**: Cross-origin resource sharing support
- **Project Tools**: Core project management functionality

### Frontend
- **React 18**: Modern UI framework with hooks and concurrent features
- **TypeScript**: Type-safe JavaScript development
- **Redux Toolkit**: State management with real-time updates
- **Tailwind CSS**: Utility-first styling framework
- **Vite**: Fast build tool and development server
- **Axios**: HTTP client for API communication
- **Socket.IO Client**: Real-time communication

### Visualization (Coming Soon)
- **Cytoscape.js**: Graph visualization for dependencies
- **Chart.js**: Metrics and statistics visualization
- **Interactive Graphs**: Dependency trees and project relationships

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements-web.txt

# Install Node.js dependencies (requires Node.js 16+)
cd frontend
npm install
cd ..
```

### 2. Start Development Servers

```bash
# Easy startup script (starts both Flask and React dev servers)
python start_web_gui.py --dev

# Or start manually:
# Terminal 1 - Flask API server
python -m project_tools.web_gui.app

# Terminal 2 - React development server
cd frontend
npm run dev
```

### 3. Access the Application

- **React Development**: http://localhost:3000 (with hot reload)
- **Flask API**: http://localhost:5000 (API endpoints)

## Production Deployment

### Build and Run

```bash
# Build frontend and start production server
python start_web_gui.py

# Or manually:
cd frontend
npm run build
cd ..
python -m project_tools.web_gui.app
```

### Advanced Options

```bash
# Custom host and port
python start_web_gui.py --host 0.0.0.0 --port 8080

# Specify project root
python start_web_gui.py --project-root /path/to/your/project

# Install dependencies and build
python start_web_gui.py --install-deps --build-frontend
```

## API Documentation

### Todo Endpoints
- `GET /api/todos` - Get todos with optional filtering
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `POST /api/todos/{id}/complete` - Complete todo
- `GET /api/todos/summary` - Get todo statistics
- `GET /api/todos/dependencies` - Get dependency information

### Version Endpoints
- `GET /api/versions` - Get version information and recent changes
- `POST /api/versions/bump` - Bump version (major/minor/patch)
- `POST /api/versions/changes` - Add changelog entry
- `GET /api/versions/history` - Get complete version history

### Intelligence Endpoints
- `GET /api/intelligence/status` - Get intelligence system status
- `GET /api/intelligence/recommendations` - Get workflow recommendations
- `GET /api/intelligence/dashboard` - Get comprehensive dashboard data
- `POST /api/intelligence/initialize` - Initialize intelligence features

### General Endpoints
- `GET /api/status` - Get overall project status
- `GET /api/health` - Health check endpoint

## Real-time Events

The application uses WebSocket for real-time updates:

### Todo Events
- `todo_created` - New todo added
- `todo_updated` - Todo modified
- `todo_deleted` - Todo removed
- `todo_completed` - Todo marked complete

### Version Events
- `version_bumped` - Version incremented
- `change_added` - New changelog entry

## Configuration

### Environment Variables
- `FLASK_ENV` - Set to 'development' for debug mode
- `PROJECT_ROOT` - Override project root directory detection
- `HOST` - Server host (default: 127.0.0.1)
- `PORT` - Server port (default: 5000)

### Project Structure
```
project_tools/
├── web_gui/                 # Flask web application
│   ├── api/                # API blueprints
│   │   ├── todos.py        # Todo endpoints
│   │   ├── versions.py     # Version endpoints
│   │   └── intelligence.py # Intelligence endpoints
│   ├── app.py              # Main Flask application
│   └── static/             # Built frontend assets
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── store/          # Redux store and slices
│   │   └── services/       # API services
│   ├── package.json
│   └── vite.config.ts
├── requirements-web.txt    # Python web dependencies
└── start_web_gui.py       # Startup script
```

## Development

### Frontend Development

```bash
cd frontend

# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Type checking
npm run tsc
```

### Backend Development

```bash
# Start Flask in debug mode
python -m project_tools.web_gui.app

# Or with custom settings
FLASK_ENV=development python -m project_tools.web_gui.app
```

### Adding New Features

1. **Backend**: Add API endpoints in `web_gui/api/`
2. **Frontend**: Create Redux slices in `store/` and components in `components/`
3. **Real-time**: Add WebSocket events in `socketSlice.ts` and Flask app
4. **Styling**: Use Tailwind CSS classes for consistent design

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Use different ports
   python start_web_gui.py --port 5001
   ```

2. **Node.js Dependencies**
   ```bash
   # Clear and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Python Dependencies**
   ```bash
   # Reinstall with force
   pip install -r requirements-web.txt --force-reinstall
   ```

4. **WebSocket Connection Issues**
   - Check if port 5000 is accessible
   - Verify CORS settings in Flask app
   - Check browser console for connection errors

### Performance Tips

- Use production build for better performance
- Enable gzip compression for static assets
- Consider using nginx as reverse proxy for production
- Monitor WebSocket connection stability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.