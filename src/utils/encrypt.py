from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64, os, jwt, pyotp

SECRET_KEY = os.environ.get("SECRET_KEY")
totp = pyotp.TOTP("base32secret3232", interval=900)


def encrypt_key(key):
    secret_key_bytes = SECRET_KEY.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=secret_key_bytes,
        length=32,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(key.encode("utf-8")))
    return key.decode("utf-8")


def verify_key(input_key, stored_key):
    derived_key = encrypt_key(input_key)
    return derived_key == stored_key


def generate_tokens(user_data: dict):
    # Configuração do token de acesso
    total_seconds = (
        (datetime.utcnow() + timedelta(minutes=15)) - datetime.now()
    ).total_seconds()
    access_token_payload = {
        "sub": str(user_data.get("_id")),
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow(),
        "nbf": datetime.utcnow(),
    }

    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm="HS256")

    refresh_token_payload = {
        "sub": str(user_data.get("_id")),
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
        "nbf": datetime.utcnow(),
    }

    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm="HS256")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": int(total_seconds),
        "user_id": user_data.get("user_id"),
    }


def validate_access_token(access_token):
    try:
        decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])

        if datetime.utcnow() < datetime.utcfromtimestamp(decoded_token["exp"]):
            return True, decoded_token

    except jwt.ExpiredSignatureError:
        return False, None

    except jwt.InvalidTokenError:
        return False, None


def validate_refresh_token(refresh_token):
    try:
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        total_seconds = (
            (datetime.utcnow() + timedelta(minutes=15)) - datetime.now()
        ).total_seconds()
        if datetime.utcnow() < datetime.utcfromtimestamp(decoded_token["exp"]):
            new_access_token
            new_access_token = jwt.encode(
                {
                    "sub": decoded_token["sub"],
                    "exp": datetime.utcnow() + timedelta(minutes=15),
                },
                SECRET_KEY,
                algorithm="HS256",
            )

            return {"access_token": new_access_token, "expires_in": total_seconds}
    except jwt.ExpiredSignatureError:
        # O refresh token expirou
        return None

    except jwt.InvalidTokenError:
        # Token inválido
        return None


def generate_otp():
    return totp.now()


def verify_otp(otp: str):
    """Verify otp code."""
    is_valid = totp.verify(otp)
    return is_valid
