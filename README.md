# User Plan Demo Project

A comprehensive demo application showcasing plan-specific API responses with a React frontend and FastAPI backend mock server.

## 🎯 Project Overview

This project demonstrates how the same API endpoints can return different data based on user plans, providing a realistic example of tiered service offerings. The demo includes:

- **Mock Backend Server**: FastAPI server with plan-specific responses
- **React Frontend**: Interactive demo application for testing API responses
- **Three User Plans**: Normal, Premium, and Ultra with distinct features

## 🏗️ Architecture

```
┌─────────────────┐     HTTP/CORS     ┌──────────────────┐
│   React Frontend│ ◄──────────────► │  FastAPI Backend │
│   (Port 3000)   │                  │   (Port 3001)    │
└─────────────────┘                  └──────────────────┘
```

## 👥 Users and Plans

| User  | Plan    | Features | Daily Quota | Support Level |
|-------|---------|----------|-------------|---------------|
| alice | Normal  | Basic features | 10 items | Limited |
| bob   | Premium | Advanced features | 50 items | Priority |
| carol | Ultra   | All features | Unlimited | 24/7 VIP |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Start the Mock Server
```bash
cd mock_server
pip install -r requirements.txt
python main.py
```
Server will be available at: http://localhost:3001

### 2. Start the Frontend
```bash
cd frontend
npm install
npm start
```
Frontend will be available at: http://localhost:3000

### 3. Run the Demo
```bash
# Run comprehensive demo script
./demo_script.sh
```

## 📱 Frontend Features

### User Selection
- Visual user cards with plan indicators
- Color-coded by plan type (Blue: Normal, Orange: Premium, Purple: Ultra)
- Current user highlighting

### API Testing
- Multiple endpoint testing (GET/POST methods)
- Real-time API calls with loading states
- Error handling and user feedback

### Response Display
- Expandable response cards
- JSON syntax highlighting
- Plan-specific content highlighting
- Timestamp tracking
- Response comparison capabilities

## 🔌 API Endpoints

### Core Endpoints
- `GET /users` - List all users and their plans
- `GET /user/data?username={user}` - Get plan-specific user data
- `POST /user/data` - Same as GET but with JSON body
- `GET /user/feature?username={user}` - Get plan-specific features
- `POST /user/feature` - Same as GET but with JSON body

### Documentation
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## 🎨 Visual Design

The frontend uses a modern, responsive design with:
- Gradient background and glassmorphism effects
- Plan-specific color coding throughout
- Smooth animations and transitions
- Mobile-responsive layout
- Accessibility considerations

## 🧪 Testing the Demo

### Manual Testing Steps
1. Open http://localhost:3000
2. Select different users and observe plan differences
3. Test all API endpoints with different users
4. Compare responses between users
5. Switch users to see plan-specific variations

### Key Observations
- Same endpoints return different content based on user
- Visual indicators clearly show plan differences
- Response content reflects plan limitations and features
- UI provides clear feedback for all interactions

## 📁 Project Structure

```
user-plan-backend/
├── mock_server/           # FastAPI backend
│   ├── main.py           # Main server application
│   ├── requirements.txt  # Python dependencies
│   ├── start_server.sh   # Server startup script
│   └── API_DOCUMENTATION.md
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.js        # Main application
│   │   └── index.js      # Entry point
│   ├── public/           # Static assets
│   ├── package.json      # Node dependencies
│   └── start_frontend.sh # Frontend startup script
├── demo_script.sh        # Comprehensive demo script
└── README.md            # This file
```

## 🔧 Development

### Adding New Users
1. Update `USER_PLANS` dictionary in `mock_server/main.py`
2. Add plan-specific responses in endpoint handlers
3. Update frontend color schemes if needed

### Adding New Endpoints
1. Create new FastAPI endpoints in `mock_server/main.py`
2. Add endpoint buttons in `frontend/src/components/ApiTester.js`
3. Update documentation

### Customizing Plans
- Modify response content in endpoint handlers
- Update plan descriptions in documentation
- Adjust frontend color coding for new plan types

## 🚦 Status Indicators

- 🟢 **Mock Server**: Running on port 3001
- 🟢 **Frontend**: Running on port 3000
- 🟢 **CORS**: Enabled for cross-origin requests
- 🟢 **API Documentation**: Available at /docs endpoint

## 🎯 Demo Goals Achieved

✅ **User Login Simulation**: Switch between three distinct users  
✅ **Plan-Specific Responses**: Same endpoints return different data  
✅ **Visual Differentiation**: Clear UI indicators for plan differences  
✅ **API Communication**: Full CORS-enabled communication with backend  
✅ **Extensible Code**: Well-organized, documented, and maintainable  
✅ **Interactive Demo**: Engaging user experience with real-time feedback  

## 🤝 Contributing

This is a demo project, but contributions for improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for demonstration purposes. Feel free to use and modify as needed.