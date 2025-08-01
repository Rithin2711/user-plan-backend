#!/bin/bash

# User Plan Demo Script
# This script demonstrates the frontend application capabilities

set -e

echo "🚀 User Plan Demo Application"
echo "============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Demo Overview:${NC}"
echo "This demo showcases a frontend application that demonstrates plan-specific API responses."
echo "• Three users with different plans: alice (normal), bob (premium), carol (ultra)"
echo "• Same API endpoints return different data based on user's plan"
echo "• Visual demonstration of plan differences in the UI"
echo ""

echo -e "${BLUE}🔧 Architecture:${NC}"
echo "• Backend: FastAPI mock server on http://localhost:3001"
echo "• Frontend: React application on http://localhost:3000"
echo "• CORS enabled for cross-origin requests"
echo ""

echo -e "${BLUE}📱 Frontend Features:${NC}"
echo "• User Selection: Switch between alice, bob, and carol"
echo "• API Testing: Call endpoints with GET and POST methods"
echo "• Response Display: View plan-specific API responses"
echo "• Visual Plan Differences: Color-coded responses by plan type"
echo ""

echo -e "${BLUE}🛠 Available API Endpoints:${NC}"
echo "• GET/POST /user/data - Returns plan-specific user data"
echo "• GET/POST /user/feature - Returns plan-specific feature information"  
echo "• GET /users - Returns all available users and their plans"
echo ""

echo -e "${BLUE}👥 User Plans:${NC}"
echo -e "${GREEN}• alice (normal):${NC} Basic features, 10 daily quota, limited support"
echo -e "${YELLOW}• bob (premium):${NC} Advanced features, 50 daily quota, priority support"
echo -e "${RED}• carol (ultra):${NC} Unlimited features, unlimited quota, 24/7 support"
echo ""

echo -e "${BLUE}🧪 Testing the API:${NC}"
echo "Testing backend connectivity..."

# Test if mock server is running
if curl -s http://localhost:3001/users > /dev/null; then
    echo -e "${GREEN}✅ Mock server is running on port 3001${NC}"
else
    echo -e "${RED}❌ Mock server is not accessible on port 3001${NC}"
    echo "Please start the mock server: cd mock_server && python main.py"
    exit 1
fi

# Test if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✅ Frontend is running on port 3000${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend is not accessible on port 3000${NC}"
    echo "Please start the frontend: cd frontend && npm start"
fi

echo ""
echo -e "${BLUE}📊 Demo API Responses:${NC}"

echo ""
echo "Testing /users endpoint:"
curl -s http://localhost:3001/users | python3 -m json.tool

echo ""
echo "Testing alice (normal plan) /user/data:"
curl -s "http://localhost:3001/user/data?username=alice" | python3 -m json.tool

echo ""
echo "Testing bob (premium plan) /user/data:"
curl -s "http://localhost:3001/user/data?username=bob" | python3 -m json.tool

echo ""
echo "Testing carol (ultra plan) /user/data:"
curl -s "http://localhost:3001/user/data?username=carol" | python3 -m json.tool

echo ""
echo -e "${GREEN}🎯 How to Use the Demo:${NC}"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Select a user (alice, bob, or carol) from the left panel"
echo "3. Click API endpoint buttons to make requests"
echo "4. Observe different responses in the right panel"
echo "5. Switch between users to compare plan differences"
echo "6. Use 'Clear Responses' button to reset the display"
echo ""

echo -e "${BLUE}🔍 Key Features to Observe:${NC}"
echo "• Color-coded user buttons by plan type"
echo "• Plan-specific response content"
echo "• Visual indicators showing current user"
echo "• Response timestamps and method indicators"
echo "• Expandable response details"
echo ""

echo -e "${GREEN}✨ Demo is ready! Open http://localhost:3000 to start exploring!${NC}"
