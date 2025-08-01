# User Plan Demo Frontend

A React-based frontend application that demonstrates plan-specific API responses by allowing users to log in as different users and interact with the mock backend server.

## Features

- **User Selection**: Switch between three users (alice, bob, carol) with different plans
- **API Testing**: Test various endpoints with both GET and POST methods
- **Response Display**: View API responses with visual plan differences
- **Real-time Updates**: See how the same endpoints return different data based on user plans
- **Responsive Design**: Works on desktop and mobile devices

## Users and Plans

- **alice**: Normal plan (basic features, 10 daily quota)
- **bob**: Premium plan (advanced features, 50 daily quota)  
- **carol**: Ultra plan (unlimited features, unlimited quota)

## Available API Endpoints

1. **GET/POST /user/data** - Returns plan-specific user data
2. **GET/POST /user/feature** - Returns plan-specific feature information
3. **GET /users** - Returns all available users and their plans

## Setup and Running

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Make sure the mock server is running**:
   - The frontend expects the mock server to be running on `http://localhost:3001`
   - Start the mock server from the `../mock_server` directory

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML template
├── src/
│   ├── components/
│   │   ├── UserSelector.js     # User login/selection component
│   │   ├── UserSelector.css
│   │   ├── ApiTester.js        # API endpoint testing component
│   │   ├── ApiTester.css
│   │   ├── ResponseDisplay.js  # API response display component
│   │   └── ResponseDisplay.css
│   ├── App.js              # Main application component
│   ├── App.css
│   └── index.js            # Application entry point
├── package.json
└── README.md
```

## How to Use

1. **Select a User**: Click on one of the three user buttons (alice, bob, or carol)
2. **Test Endpoints**: Use the API testing buttons to call different endpoints
3. **Compare Responses**: View how the same endpoint returns different data for different users
4. **Switch Users**: Change users to see plan-specific differences
5. **Clear Responses**: Use the "Clear Responses" button to reset the display

## Plan Differences Demonstration

The application visually demonstrates how the same API endpoints return different data based on the user's plan:

- **Color Coding**: Each plan has a distinct color (Normal: Blue, Premium: Orange, Ultra: Purple)
- **Content Differences**: API responses show plan-specific features and limitations
- **Visual Indicators**: Plan badges and color coding make differences obvious

## CORS Configuration

The frontend is configured to work with the mock server running on port 3001. The `package.json` includes a proxy configuration to handle CORS during development.

## Technologies Used

- **React 18**: Modern React with hooks
- **Axios**: HTTP client for API calls
- **CSS3**: Custom styling with flexbox and grid
- **Responsive Design**: Mobile-friendly layout
