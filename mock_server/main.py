from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict

# --- In-memory user and plan setup ---

# PUBLIC_INTERFACE
class User(BaseModel):
    """User model with username and plan."""
    username: str = Field(..., description="The unique username")
    plan: str = Field(..., description="The subscription plan (basic, pro, enterprise)")

# Demo users: username -> plan
USER_PLAN_MAP: Dict[str, str] = {
    "alice": "basic",
    "bob": "pro",
    "charlie": "enterprise",
}

# In-memory current user (simulates a session; for demo/development only)
current_user: Optional[User] = None

# --- FastAPI app setup ---

app = FastAPI(
    title="Mock User Plan Server",
    description=(
        "A backend mock server that demonstrates username-based login and "
        "plan-based feature variation for demo purposes. No authentication required."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "Login and user management"},
        {"name": "Demo Endpoints", "description": "Plan-based API demo endpoints"},
    ],
)

# Allow CORS for demo/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper dependencies and responses ---

def get_current_user(x_username: Optional[str] = Header(default=None, alias="X-Username")) -> User:
    """
    Extracts current user based on X-Username header.
    Raises HTTPException if user is not recognized or not logged in.

    Args:
        x_username: Optional[str] - X-Username header (case-insensitive)

    Returns:
        User: The active User object from in-memory map
    """
    # Use header if provided, fall back to in-memory current_user
    if x_username:
        plan = USER_PLAN_MAP.get(x_username.lower())
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username not recognized. Please login first."
            )
        return User(username=x_username.lower(), plan=plan)
    if current_user:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No user logged in. Use /login to select a user."
    )

# --- Public API models ---

# PUBLIC_INTERFACE
class LoginRequest(BaseModel):
    """Request model for login endpoint."""
    username: str = Field(..., description="Username to login as")

# PUBLIC_INTERFACE
class LoginResponse(BaseModel):
    """Login response with assigned plan."""
    username: str = Field(..., description="Logged-in username")
    plan: str = Field(..., description="Assigned plan")

# --- Authentication Endpoints ---

# PUBLIC_INTERFACE
@app.post("/login", response_model=LoginResponse, tags=["Authentication"], summary="Login as a user")
async def login(request: LoginRequest):
    """
    Log in as one of the demo users by username (no password required).
    Sets the active user for your session.

    Args:
        request (LoginRequest): JSON body with 'username' field.

    Returns:
        LoginResponse: Username and assigned plan.
    """
    global current_user
    username = request.username.lower()
    plan = USER_PLAN_MAP.get(username)
    if not plan:
        raise HTTPException(status_code=401, detail="User not found. Available users: " + ", ".join(USER_PLAN_MAP.keys()))
    current_user = User(username=username, plan=plan)
    return LoginResponse(username=username, plan=plan)

# PUBLIC_INTERFACE
@app.post("/switch_user", response_model=LoginResponse, tags=["Authentication"], summary="Switch to a different user")
async def switch_user(request: LoginRequest):
    """
    Switch to another demo user using their username.

    Args:
        request (LoginRequest): JSON body with new username.

    Returns:
        LoginResponse: Username and assigned plan.
    """
    global current_user
    username = request.username.lower()
    plan = USER_PLAN_MAP.get(username)
    if not plan:
        raise HTTPException(status_code=401, detail="User not found. Available users: " + ", ".join(USER_PLAN_MAP.keys()))
    current_user = User(username=username, plan=plan)
    return LoginResponse(username=username, plan=plan)

# PUBLIC_INTERFACE
@app.get("/current_user", response_model=LoginResponse, tags=["Authentication"], summary="Get current logged-in user")
async def get_logged_in_user(user: User = Depends(get_current_user)):
    """
    Get info about the currently active/logged-in user.

    Returns:
        LoginResponse: Username and assigned plan.
    """
    return LoginResponse(username=user.username, plan=user.plan)

# PUBLIC_INTERFACE
@app.post("/logout", tags=["Authentication"], summary="Log out current user")
async def logout():
    """
    Log out the current user (clears session).
    """
    global current_user
    current_user = None
    return {"msg": "Logged out. No user active."}

# --- Demo Endpoints (plan-based responses) ---

# PUBLIC_INTERFACE
class UserDataResponse(BaseModel):
    """Data summary, varies based on plan."""
    username: str = Field(..., description="The current user")
    plan: str = Field(..., description="User's plan")
    data: str = Field(..., description="Plan-specific data/response")

# PUBLIC_INTERFACE
@app.get("/user/data", response_model=UserDataResponse, tags=["Demo Endpoints"], summary="Get user data for plan")
async def get_user_data(user: User = Depends(get_current_user)):
    """
    Get demo data for the user; output changes based on assigned plan.

    Returns:
        UserDataResponse: Data and details unique to the user's plan.
    """
    base = f"Hello {user.username}! You are on the {user.plan} plan."
    if user.plan == "basic":
        data = f"{base} You receive 5 data points and community support."
    elif user.plan == "pro":
        data = f"{base} You receive 20 data points, email support, and quarterly analytics."
    elif user.plan == "enterprise":
        data = f"{base} You receive UNLIMITED data points, 24/7 premium support, and dedicated account management."
    else:
        data = f"{base} [Unknown plan]"
    return UserDataResponse(username=user.username, plan=user.plan, data=data)

# PUBLIC_INTERFACE
class FeatureResponse(BaseModel):
    """Feature summary, varies based on plan."""
    username: str = Field(..., description="The current user")
    plan: str = Field(..., description="User's plan")
    feature_message: str = Field(..., description="Plan-specific feature description")

# PUBLIC_INTERFACE
@app.get("/user/feature", response_model=FeatureResponse, tags=["Demo Endpoints"], summary="Get feature flags/info based on plan")
async def get_user_feature(user: User = Depends(get_current_user)):
    """
    Returns unique feature messages based on the user's plan.

    Returns:
        FeatureResponse: Plan-specific feature variations.
    """
    if user.plan == "basic":
        message = "Basic plan: Feature A only. Upgrade for more!"
    elif user.plan == "pro":
        message = "Pro plan: Features A, B, and access to advanced reporting."
    elif user.plan == "enterprise":
        message = "Enterprise plan: All features (A, B, C), custom integrations, and VIP onboarding."
    else:
        message = "Unknown plan."
    return FeatureResponse(username=user.username, plan=user.plan, feature_message=message)

# PUBLIC_INTERFACE
@app.get("/user/dashboard", tags=["Demo Endpoints"], summary="Dashboard data (plan-varied)")
async def get_user_dashboard(user: User = Depends(get_current_user)):
    """
    Demo: Dashboard widgets/data varies based on plan.

    Returns:
        Dict[str, str]: Dashboard data details per plan.
    """
    if user.plan == "basic":
        resp = {
            "widgets": "2 widgets: 'Overview', 'Profile'",
            "tips": "Upgrade to Pro for analytics and reporting!",
        }
    elif user.plan == "pro":
        resp = {
            "widgets": "5 widgets: 'Overview', 'Profile', 'Analytics', 'Reports', 'Export'",
            "tips": "Enterprise unlocks customization options.",
        }
    elif user.plan == "enterprise":
        resp = {
            "widgets": "All widgets enabled, plus custom builder",
            "tips": "Enjoy priority SLAs and dedicated tools.",
        }
    else:
        resp = {
            "widgets": "None",
            "tips": "Unknown plan.",
        }
    resp.update({
        "username": user.username,
        "plan": user.plan,
    })
    return resp

# --- Extra: User directory endpoint for demo/testing ---

# PUBLIC_INTERFACE
@app.get("/directory", tags=["Authentication"], summary="Get directory of demo users (for demo/test)")
async def directory():
    """
    Lists all available demo users and their assigned plans.

    Returns:
        Dict[str, str]: Mapping of usernames to plans.
    """
    return USER_PLAN_MAP.copy()

# --- Custom OpenAPI: Add explicit demo notes ---

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description + (
            "\n\n---\n\n"
            "**Demo usage:**\n"
            "- Log in using /login (username only: alice, bob, charlie)\n"
            "- Use X-Username request header (or session) for all API calls\n"
            "- Endpoints like /user/data return responses unique to your plan\n"
            "- Switch between users with /switch_user\n"
            "- All data is in-memory and resets when server restarts.\n"
        ),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- Entrypoint ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
