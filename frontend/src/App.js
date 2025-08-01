import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserSelector from './components/UserSelector';
import ApiTester from './components/ApiTester';
import ResponseDisplay from './components/ResponseDisplay';
import './App.css';

// PUBLIC_INTERFACE
function App() {
  /**
   * Main application component that orchestrates user login, API testing, and response display.
   * Manages global state for current user, available users, and API responses.
   */
  
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState({});
  const [apiResponses, setApiResponses] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // API base URL - targeting mock server on port 3001
  const API_BASE_URL = 'http://localhost:3001';

  // Fetch available users on component mount
  useEffect(() => {
    fetchUsers();
  }, []);

  // PUBLIC_INTERFACE
  const fetchUsers = async () => {
    /**
     * Fetches the list of available users and their plans from the backend.
     */
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/users`);
      setUsers(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError('Failed to fetch users. Make sure the mock server is running on port 3001.');
    } finally {
      setLoading(false);
    }
  };

  // PUBLIC_INTERFACE
  const loginUser = (username) => {
    /**
     * Sets the current user for the session.
     * @param {string} username - The username to log in as
     */
    setCurrentUser(username);
    setApiResponses({}); // Clear previous responses when switching users
    setError(null);
  };

  // PUBLIC_INTERFACE
  const makeApiCall = async (endpoint, method = 'GET', data = null) => {
    /**
     * Makes an API call to the specified endpoint with the current user context.
     * @param {string} endpoint - The API endpoint to call
     * @param {string} method - HTTP method (GET or POST)
     * @param {object} data - Optional data for POST requests
     */
    if (!currentUser) {
      setError('Please select a user first');
      return;
    }

    try {
      setLoading(true);
      let response;
      
      if (method === 'GET') {
        response = await axios.get(`${API_BASE_URL}${endpoint}?username=${currentUser}`);
      } else if (method === 'POST') {
        const postData = data || { username: currentUser };
        response = await axios.post(`${API_BASE_URL}${endpoint}`, postData);
      }

      // Store the response with a unique key
      const responseKey = `${method}_${endpoint}_${Date.now()}`;
      setApiResponses(prev => ({
        ...prev,
        [responseKey]: {
          endpoint,
          method,
          user: currentUser,
          data: response.data,
          timestamp: new Date().toISOString()
        }
      }));
      
      setError(null);
    } catch (err) {
      console.error('API call failed:', err);
      setError(`API call failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // PUBLIC_INTERFACE
  const clearResponses = () => {
    /**
     * Clears all stored API responses.
     */
    setApiResponses({});
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>User Plan Demo</h1>
        <p>Demonstrate plan-specific API responses for different users</p>
      </header>
      
      <main className="App-main">
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
            <button onClick={() => setError(null)} className="close-error">×</button>
          </div>
        )}
        
        <div className="demo-container">
          <div className="left-panel">
            <UserSelector
              users={users}
              currentUser={currentUser}
              onUserSelect={loginUser}
              loading={loading}
            />
            
            <ApiTester
              currentUser={currentUser}
              onApiCall={makeApiCall}
              loading={loading}
            />
            
            <div className="controls">
              <button 
                onClick={clearResponses}
                className="clear-button"
                disabled={Object.keys(apiResponses).length === 0}
              >
                Clear Responses
              </button>
              <button 
                onClick={fetchUsers}
                className="refresh-button"
                disabled={loading}
              >
                Refresh Users
              </button>
            </div>
          </div>
          
          <div className="right-panel">
            <ResponseDisplay
              responses={apiResponses}
              currentUser={currentUser}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
