import React from 'react';
import './ApiTester.css';

// PUBLIC_INTERFACE
const ApiTester = ({ currentUser, onApiCall, loading }) => {
  /**
   * Component for testing different API endpoints.
   * Provides buttons to call various endpoints with both GET and POST methods.
   */

  const endpoints = [
    {
      path: '/user/data',
      description: 'Get user data (plan-specific content)',
      methods: ['GET', 'POST']
    },
    {
      path: '/user/feature',
      description: 'Get feature information (plan-specific features)',
      methods: ['GET', 'POST']
    },
    {
      path: '/users',
      description: 'Get all users and their plans',
      methods: ['GET']
    }
  ];

  const handleApiCall = (endpoint, method) => {
    onApiCall(endpoint, method);
  };

  return (
    <div className="api-tester">
      <h3>API Endpoints</h3>
      
      {!currentUser ? (
        <div className="no-user-selected">
          Please select a user first to test API endpoints.
        </div>
      ) : (
        <div className="endpoint-list">
          {endpoints.map((endpoint) => (
            <div key={endpoint.path} className="endpoint-group">
              <div className="endpoint-info">
                <div className="endpoint-path">{endpoint.path}</div>
                <div className="endpoint-description">{endpoint.description}</div>
              </div>
              
              <div className="method-buttons">
                {endpoint.methods.map((method) => (
                  <button
                    key={`${endpoint.path}-${method}`}
                    className={`method-button method-${method.toLowerCase()}`}
                    onClick={() => handleApiCall(endpoint.path, method)}
                    disabled={loading}
                  >
                    {method}
                    {loading && <span className="loading-spinner">⏳</span>}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {currentUser && (
        <div className="testing-as">
          <strong>Testing as:</strong> {currentUser}
        </div>
      )}
    </div>
  );
};

export default ApiTester;
