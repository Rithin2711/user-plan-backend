# Mock User Plan Server

A FastAPI-based mock server that demonstrates plan-specific API responses based on username. This server simulates different user plans (normal, premium, ultra) and returns customized responses for the same endpoints.

## Features

- **Plan-based responses**: Same API endpoints return different data based on user's plan
- **Multiple users**: Pre-configured users (alice, bob, carol) with different plans
- **RESTful API**: GET and POST endpoints for user data and features
- **OpenAPI documentation**: Auto-generated API docs with Swagger UI
- **CORS enabled**: Ready for frontend integration
- **Docker support**: Containerized deployment ready

## Users and Plans

- **alice** (normal plan): Basic features, limited quota
- **bob** (premium plan): Enhanced features, higher quota
- **carol** (ultra plan): All features, unlimited access

## API Endpoints

### GET/POST `/user/data`
Returns plan-specific user data based on username.

**Query Parameter**: `?username=alice|bob|carol`  
**JSON Body**: `{"username": "alice|bob|carol"}`

### GET/POST `/user/feature`
Returns available features for the user's plan.

**Query Parameter**: `?username=alice|bob|carol`  
**JSON Body**: `{"username": "alice|bob|carol"}`

### GET `/users`
Returns all available users and their plans.

## Quick Start

### Using Python directly

1. **Install dependencies**:
   ```bash
   cd mock_server
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python main.py
   # or
   ./run_mock_server.sh
   ```

3. **Access the API**:
   - Server: http://localhost:3001
   - API Docs: http://localhost:3001/docs
   - OpenAPI spec: http://localhost:3001/openapi.json

### Using Docker

1. **Build and run with docker-compose**:
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**:
   ```bash
   cd mock_server
   docker build -t mock-server .
   docker run -p 3001:3001 mock-server
   ```

## Example Usage

### Get user data for Alice (normal plan)
```bash
curl "http://localhost:3001/user/data?username=alice"
```

Response:
```json
{
  "username": "alice",
  "plan": "normal",
  "data": "Welcome, alice! You're on the NORMAL plan. You can access basic features, view standard data, and use the app with limited support. Your daily quota: 10 data items. Upgrade for more!"
}
```

### Get features for Bob (premium plan)
```bash
curl "http://localhost:3001/user/feature?username=bob"
```

Response:
```json
{
  "username": "bob",
  "plan": "premium", 
  "features": "PREMIUM plan: Includes all 'normal' features, plus premium analytics, early feature previews, increased API rate limit (50/day), email support, and monthly data exports."
}
```

### POST request with JSON body
```bash
curl -X POST "http://localhost:3001/user/data" \
  -H "Content-Type: application/json" \
  -d '{"username": "carol"}'
```

## Configuration

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

## Project Structure

```
user-plan-backend/
├── mock_server/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── run_mock_server.sh     # Start script
│   ├── Dockerfile             # Docker configuration
│   ├── .env.example           # Environment variables template
│   └── .env                   # Environment variables (create from .env.example)
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## Development

The server runs with auto-reload enabled in development mode. Any changes to the code will automatically restart the server.

## API Documentation

Visit http://localhost:3001/docs for interactive API documentation powered by Swagger UI.

## Health Check

The server includes a health check endpoint at `/users` that returns the list of available users and their plans.

## License

This is a demo/mock server for development and testing purposes.
