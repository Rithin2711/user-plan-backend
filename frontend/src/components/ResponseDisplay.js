import React, { useState } from 'react';
import './ResponseDisplay.css';

// PUBLIC_INTERFACE
const ResponseDisplay = ({ responses, currentUser }) => {
  /**
   * Component for displaying API responses with plan comparison.
   * Shows responses in a formatted manner with syntax highlighting and plan differences.
   */

  const [expandedResponses, setExpandedResponses] = useState({});

  const toggleExpanded = (responseKey) => {
    setExpandedResponses(prev => ({
      ...prev,
      [responseKey]: !prev[responseKey]
    }));
  };

  const responseEntries = Object.entries(responses).reverse(); // Show newest first

  const getPlanColor = (user) => {
    // Assuming we can get plan from response data
    if (!responses || Object.keys(responses).length === 0) return '#666';
    
    const userResponses = Object.values(responses).filter(r => r.user === user);
    if (userResponses.length === 0) return '#666';
    
    const plan = userResponses[0].data?.plan;
    switch (plan) {
      case 'normal': return '#2196f3';
      case 'premium': return '#ff9800';
      case 'ultra': return '#9c27b0';
      default: return '#666';
    }
  };

  const formatJson = (obj) => {
    return JSON.stringify(obj, null, 2);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="response-display">
      <div className="response-header">
        <h3>API Responses</h3>
        {responseEntries.length > 0 && (
          <div className="response-count">
            {responseEntries.length} response{responseEntries.length !== 1 ? 's' : ''}
          </div>
        )}
      </div>

      {responseEntries.length === 0 ? (
        <div className="no-responses">
          <div className="empty-state">
            <div className="empty-icon">📡</div>
            <h4>No API responses yet</h4>
            <p>Select a user and click on an API endpoint to see responses here.</p>
            <p>Responses will show plan-specific differences for each user.</p>
          </div>
        </div>
      ) : (
        <div className="response-list">
          {responseEntries.map(([responseKey, response]) => (
            <div key={responseKey} className="response-item">
              <div className="response-item-header">
                <div className="response-meta">
                  <span className={`method-tag method-${response.method.toLowerCase()}`}>
                    {response.method}
                  </span>
                  <span className="endpoint-tag">{response.endpoint}</span>
                  <span 
                    className="user-tag"
                    style={{ 
                      backgroundColor: getPlanColor(response.user),
                      color: 'white'
                    }}
                  >
                    {response.user}
                  </span>
                  <span className="timestamp-tag">
                    {formatTimestamp(response.timestamp)}
                  </span>
                </div>
                <button
                  className="expand-button"
                  onClick={() => toggleExpanded(responseKey)}
                >
                  {expandedResponses[responseKey] ? '▼' : '▶'}
                </button>
              </div>

              <div className={`response-content ${expandedResponses[responseKey] ? 'expanded' : ''}`}>
                {response.data?.plan && (
                  <div className={`plan-indicator plan-${response.data.plan}`}>
                    <strong>{response.data.plan.toUpperCase()} PLAN</strong>
                  </div>
                )}

                <div className="response-body">
                  <pre className="json-response">
                    {formatJson(response.data)}
                  </pre>
                </div>

                {response.data?.data && (
                  <div className="plan-specific-content">
                    <h5>Plan-Specific Content:</h5>
                    <div className="content-text">
                      {response.data.data}
                    </div>
                  </div>
                )}

                {response.data?.features && (
                  <div className="plan-specific-content">
                    <h5>Plan-Specific Features:</h5>
                    <div className="content-text">
                      {response.data.features}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {responseEntries.length > 0 && (
        <div className="plan-legend">
          <h4>Plan Colors:</h4>
          <div className="legend-items">
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#2196f3' }}></span>
              Normal Plan
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#ff9800' }}></span>
              Premium Plan
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: '#9c27b0' }}></span>
              Ultra Plan
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResponseDisplay;
