# Mock User Plan Server API Documentation

## Overview
This mock server demonstrates plan-specific API responses based on username. The same endpoints return different data depending on the user's assigned plan.

## Base URL
```
http://localhost:8081
```

## Users and Plans
- **alice**: normal plan
- **bob**: premium plan  
- **carol**: ultra plan

## Endpoints

### GET /user/data
Returns plan-specific data for a user.

**Query Parameters:**
- `username` (string): The username (alice, bob, or carol)

**Example:**
```bash
curl "http://localhost:8081/user/data?username=alice"
```

**Response:**
```json
{
  "username": "alice",
  "plan": "normal", 
  "data": "Welcome, alice! You're on the NORMAL plan. You can access basic features..."
}
```

### POST /user/data
Same as GET but accepts username in JSON body.

**Request Body:**
```json
{
  "username": "alice"
}
```

### GET /user/feature
Returns plan-specific feature information.

**Query Parameters:**
- `username` (string): The username (alice, bob, or carol)

**Example:**
```bash
curl "http://localhost:8081/user/feature?username=bob"
```

**Response:**
```json
{
  "username": "bob",
  "plan": "premium",
  "features": "PREMIUM plan: Includes all 'normal' features, plus premium analytics..."
}
```

### POST /user/feature
Same as GET but accepts username in JSON body.

### GET /users
Returns all available users and their plans.

**Response:**
```json
{
  "alice": "normal",
  "bob": "premium", 
  "carol": "ultra"
}
```

## Plan Differences

### Normal Plan (alice)
- Basic features access
- Standard data view
- Limited support
- 10 daily data items quota

### Premium Plan (bob)  
- All normal features
- Premium analytics
- Priority support
- 50 daily data items quota
- Early feature previews
- Monthly data exports

### Ultra Plan (carol)
- All premium features
- Unlimited API usage
- Direct product team access
- Custom integrations
- VIP tools
- 24/7 support
- White-glove onboarding

## Interactive Documentation
Visit http://localhost:8081/docs for Swagger UI documentation.

## CORS
The server is configured to allow all origins for demo purposes.
