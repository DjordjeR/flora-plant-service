from pydantic.types import UUID4
from app.core.config import settings

from keycloak.keycloak_admin import KeycloakAdmin
from keycloak.keycloak_openid import KeycloakOpenID


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

_KEYCLOAK_PUBLIC_KEY = keycloak_openid.certs()
_KEYCLOAK_VERIFY_OPTIONS = {
    "verify_signature": True,
    "verify_aud": True,
    "verify_exp": True,
}


def verify_user(token_in: UUID4):
    try:
        keycloak_openid.userinfo(str(token_in))
        return True
    except:
        return False
