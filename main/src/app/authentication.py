import json
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Header
from fastapi.routing import APIRouter
from fastapi.security.base import SecurityBase
from fastapi.security.http import HTTPAuthorizationCredentials
from keycloak.keycloak_admin import KeycloakAdmin
from keycloak.keycloak_openid import KeycloakOpenID
from pydantic.main import BaseModel
from starlette.requests import Request

from app.core.config import settings

from .schema import user

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM_NAME,
)

keycloak_openid_admin = KeycloakAdmin(
    server_url=settings.KEYCLOAK_URL,
    username=settings.KEYCLOAK_ADMIN_USER,
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    realm_name=settings.KEYCLOAK_REALM_NAME,
)


auth_router = APIRouter()


class AuthModel(BaseModel):
    bearer: str


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthBase(SecurityBase):
    def __init__(
        self,
        *,
        scheme_name: Optional[str] = None,
        realm: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = AuthModel(bearer="Bearer <your token here>")
        self.scheme_name = scheme_name or self.__class__.__name__
        self.realm = realm
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        return authorization


auth_bearer = AuthBase()


def _verify_user(token_in: str) -> user.UserLoggedIn:
    try:
        user_info = keycloak_openid.userinfo(str(token_in))
        print(user_info)
        return user.UserLoggedIn(**user_info)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Not authorized1")


def get_current_user(
    authorization: str = Depends(auth_bearer),
) -> user.UserLoggedIn:
    try:
        token = authorization.split(" ")[1]
        return _verify_user(token)
    except:
        raise HTTPException(status_code=403, detail="Not authorized")


@auth_router.post(
    "/auth/token",
    tags=["auth"],
    response_model=user.UserLoginResponse,
    responses={401: {"model": user.UserKeycloackDetail}},
)
def auth_token(user_in: user.UserLoginRequest):
    try:
        return user.UserLoginResponse(
            **keycloak_openid.token(user_in.username, user_in.password)
        )
    except Exception as e:
        try:
            msg = json.loads(e.error_message.decode("utf-8"))
            msg = msg.get("error_description", "Unkown error")
        except:
            msg = "Undown error"
        raise HTTPException(status_code=401, detail=msg)


@auth_router.post(
    "/auth/refresh",
    tags=["auth"],
    response_model=user.UserLoginResponse,
    responses={401: {"model": user.UserKeycloackDetail}},
)
def auth_token_refresh(rr: RefreshRequest):
    try:
        return user.UserLoginResponse(**keycloak_openid.refresh_token(rr.refresh_token))
    except Exception as e:
        try:
            msg = json.loads(e.error_message.decode("utf-8"))
            msg = msg.get("error_description", "Unkown error")
        except:
            msg = "Undown error"
        raise HTTPException(status_code=401, detail=msg)


@auth_router.post(
    "/auth/register",
    tags=["auth"],
    response_model=user.UserOut,
    responses={401: {"model": user.UserKeycloackDetail}},
)
def auth_user_register(user_in: user.UserIn):
    try:
        new_user = keycloak_openid_admin.create_user(
            {
                "email": user_in.email,
                "username": user_in.username,
                "enabled": True,
                "firstName": user_in.firstName,
                "lastName": user_in.lastName,
                "credentials": [
                    {
                        "value": "secret",
                        "type": user_in.password,
                    }
                ],
            }
        )
        keycloak_openid_admin.set_user_password(
            user_id=new_user, password=user_in.password, temporary=False
        )

        user_out = user.UserOut(id=new_user, **user_in.dict())
        user_out.id = new_user
        return user_out
    except Exception as e:
        try:
            msg = json.loads(e.error_message.decode("utf-8"))
            msg = msg.get("error_description", "Unkown error")
        except:
            msg = "Undown error"
        raise HTTPException(status_code=401, detail=msg)
