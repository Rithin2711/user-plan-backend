import React from 'react';
import './UserSelector.css';

// PUBLIC_INTERFACE
const UserSelector = ({ users, currentUser, onUserSelect, loading }) => {
  /**
   * Component for selecting and logging in as different users.
   * Displays available users with their plans and highlights the current user.
   */

  const userEntries = Object.entries(users);

  return (
    <div className="user-selector">
      <h3>Select User</h3>
      
      {loading && userEntries.length === 0 ? (
        <div className="loading">Loading users...</div>
      ) : userEntries.length === 0 ? (
        <div className="no-users">
          No users available. Make sure the mock server is running.
        </div>
      ) : (
        <div className="user-list">
          {userEntries.map(([username, plan]) => (
            <button
              key={username}
              className={`user-button ${currentUser === username ? 'active' : ''} plan-${plan}`}
              onClick={() => onUserSelect(username)}
              disabled={loading}
            >
              <div className="user-info">
                <div className="username">{username}</div>
                <div className="plan-badge">{plan} plan</div>
              </div>
              {currentUser === username && (
                <div className="current-indicator">✓</div>
              )}
            </button>
          ))}
        </div>
      )}
      
      {currentUser && (
        <div className="current-user">
          <strong>Logged in as:</strong> {currentUser} ({users[currentUser]} plan)
        </div>
      )}
    </div>
  );
};

export default UserSelector;
