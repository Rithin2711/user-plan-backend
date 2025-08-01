from fastapi import FastAPI, Query, Body
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal

# --- In-memory hardcoded users and plans (per requirements) ---

# Maps each username to their plan name.
USER_PLANS = {
    "alice": "normal",
    "bob": "premium",
    "carol": "ultra"
}

# --- FastAPI app setup ---

app = FastAPI(
    title="Mock User Plan Server",
    description=(
        "Mock backend server: demonstrates endpoints whose output varies entirely based on the username. "
        "The same endpoint will reply with distinct data for 'alice' (normal plan), 'bob' (premium), and 'carol' (ultra). "
        "No authentication. Send username as a query param or JSON body field. "
        "Great for frontend and plan-tier demo."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "UserPlanDemo", "description": "Plan-based API endpoints for demo. Behavior is user/plan-specific."},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic models for API I/O ---

# PUBLIC_INTERFACE
class UserDataRequest(BaseModel):
    """Request body: provide username for data request."""
    username: str = Field(..., description="The username (alice, bob, or carol)")

# PUBLIC_INTERFACE
class FeatureRequest(BaseModel):
    """Request body: provide username for feature info request."""
    username: str = Field(..., description="The username (alice, bob, or carol)")

# PUBLIC_INTERFACE
class UserDataResponse(BaseModel):
    """Response for /user/data: always includes username, plan level, and a distinct data description."""
    username: str = Field(..., description="The username for whom data is retrieved")
    plan: Literal['normal', 'premium', 'ultra'] = Field(..., description="Plan level: normal, premium, or ultra")
    data: str = Field(..., description="Distinct, plan-specific user data/description.")

# PUBLIC_INTERFACE
class UserFeatureResponse(BaseModel):
    """Response for /user/feature: always includes username, plan, and plan-specific feature info."""
    username: str = Field(..., description="The username requesting feature info")
    plan: Literal['normal', 'premium', 'ultra'] = Field(..., description="User's plan")
    features: str = Field(..., description="Textual summary of features unique to this plan.")

# --- Helper: Plan lookup and error management ---

def get_plan_for_username(username: str) -> str:
    """
    Utility: return plan for a username or raise a ValueError if unknown.
    """
    key = username.strip().lower()
    plan = USER_PLANS.get(key)
    if not plan:
        raise ValueError(
            f"Username not recognized: '{username}'. Must be one of: {', '.join(USER_PLANS.keys())}"
        )
    return plan

# --- Endpoints ---

# PUBLIC_INTERFACE
@app.get("/user/data", response_model=UserDataResponse, tags=["UserPlanDemo"], summary="Get user data (plan-specific, by username)")
async def get_user_data(username: Optional[str] = Query(None, description="The username (alice, bob, or carol)")):
    """
    Returns plan-specific data summary for the given username.

    The 'plan' in the response reflects the user's assigned plan.
    Response content is *meaningfully* different for each plan (normal, premium, ultra).
    No authentication needed.
    """
    if not username:
        return {
            "username": "",
            "plan": "",
            "data": "You must provide a username as query parameter (?username=alice, bob, or carol)."
        }
    try:
        plan = get_plan_for_username(username)
    except ValueError as e:
        return {"username": username.lower(), "plan": "", "data": str(e)}
    uname = username.strip().lower()
    if plan == "normal":
        data = (
            "Welcome, alice! You're on the NORMAL plan. "
            "You can access basic features, view standard data, and use the app with limited support. "
            "Your daily quota: 10 data items. Upgrade for more!"
        )
    elif plan == "premium":
        data = (
            "Hello, bob! You're on the PREMIUM plan. "
            "In addition to everything in 'normal', you get access to premium-only reports, priority support, and a 5x data quota (50 daily items)."
        )
    elif plan == "ultra":
        data = (
            "Hi, carol! You're on the ULTRA plan. "
            "Enjoy all features: unlimited data, exclusive beta features, one-on-one onboarding, and 24/7 direct support. The app experience is fully unlocked."
        )
    else:
        data = "Unknown plan."
    return UserDataResponse(username=uname, plan=plan, data=data)

# PUBLIC_INTERFACE
@app.post("/user/data", response_model=UserDataResponse, tags=["UserPlanDemo"], summary="Get user data (plan-specific, via JSON)")
async def post_user_data(request: UserDataRequest = Body(...)):
    """
    Returns plan-specific data for the given username supplied in JSON.
    """
    return await get_user_data(username=request.username)

# PUBLIC_INTERFACE
@app.get("/user/feature", response_model=UserFeatureResponse, tags=["UserPlanDemo"], summary="Get feature info for plan (by username, query param)")
async def get_user_feature(username: Optional[str] = Query(None, description="The username (alice, bob, or carol)")):
    """
    Returns descriptive summary of accessible features for the given username's plan.
    Response content is *clearly distinct* for normal/premium/ultra.
    """
    if not username:
        return {
            "username": "",
            "plan": "",
            "features": "Provide ?username=alice, bob, or carol."
        }
    try:
        plan = get_plan_for_username(username)
    except ValueError as e:
        return {"username": username.lower(), "plan": "", "features": str(e)}
    uname = username.strip().lower()
    if plan == "normal":
        features = (
            "NORMAL plan: Access standard dashboard, community forum, and API rate limited to 10 calls/day. No analytics, no premium reports."
        )
    elif plan == "premium":
        features = (
            "PREMIUM plan: Includes all 'normal' features, plus premium analytics, early feature previews, increased API rate limit (50/day), email support, and monthly data exports."
        )
    elif plan == "ultra":
        features = (
            "ULTRA plan: All premium features plus unlimited API usage, direct access to product team, custom integrations, exclusive VIP tools, priority bugfixes, and white-glove onboarding."
        )
    else:
        features = "Unknown plan."
    return UserFeatureResponse(username=uname, plan=plan, features=features)

# PUBLIC_INTERFACE
@app.post("/user/feature", response_model=UserFeatureResponse, tags=["UserPlanDemo"], summary="Get feature info for plan (by username, JSON)")
async def post_user_feature(request: FeatureRequest = Body(...)):
    """
    Returns feature info for the username/plan specified as JSON.
    """
    return await get_user_feature(username=request.username)

# --- User directory for demo/testing ---

@app.get("/users", tags=["UserPlanDemo"], summary="Get a list of all usernames and their plan (demo)")
async def list_users():
    """
    Returns a mapping of all available usernames to their plan.
    """
    return USER_PLANS.copy()

# --- OpenAPI customization for demo notes and usage help ---

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description +
            (
                "\n\nUsage:\n"
                "- Provide a username via query (?username=alice, bob, or carol) or as a JSON field {\"username\": ...}.\n"
                "- /user/data and /user/feature will reply distinctly for each user's plan.\n"
                "- Users: alice (normal), bob (premium), carol (ultra).\n"
                "- No login, authentication, or headers required."
            ),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- Entrypoint ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)
