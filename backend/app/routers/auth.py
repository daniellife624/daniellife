from fastapi import APIRouter, HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from ..config import settings
from ..auth import create_access_token
from ..schemas.auth import GoogleLoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=TokenResponse)
def google_login(body: GoogleLoginRequest):
    # Verify Google ID token
    try:
        idinfo = id_token.verify_oauth2_token(
            body.credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Google token: {e}")

    email: str = idinfo.get("email", "")
    if not idinfo.get("email_verified", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google email not verified")
    if email != settings.ADMIN_EMAIL:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not authorized")

    token = create_access_token(subject=email)
    name: str = idinfo.get("name", "Daniel")
    return TokenResponse(access_token=token, name=name, email=email)
