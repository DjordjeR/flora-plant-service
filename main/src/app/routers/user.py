from fastapi import APIRouter, HTTPException
from ..schema import user

from ..authentication import keycloak_openid, keycloak_openid_admin, verify_user

router = APIRouter()

# Configure client


@router.post(
    "/user/login",
    tags=["user"],
    response_model=user.UserLoginResponse,
    responses={401: {"model": user.UserKeycloackDetail}},
)
def user_login(user_in: user.UserLoginRequest):
    try:
        ret = user.UserLoginResponse(
            **keycloak_openid.token(user_in.username, user_in.password)
        )

        verify_user(ret.access_token)
        return ret
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login not possible {e}")


@router.get(
    "/user/logout",
    tags=["user"],
    response_model=user.UserKeycloackDetail,
    responses={401: {"model": user.UserKeycloackDetail}},
)
def user_logout():
    try:
        keycloak_openid.logout()
    except:
        raise HTTPException(status_code=401, detail="Logout not possible")


@router.post(
    "/user/register",
    tags=["user"],
    response_model=user.UserOut,
    responses={401: {"model": user.UserKeycloackDetail}},
)
def user_register(user_in: user.UserIn):
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
        raise HTTPException(status_code=401, detail=f"Could not create user {e}")
