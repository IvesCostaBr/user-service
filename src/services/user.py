from src.repositorys import user_repo, login_repo
from src.models import user
from starlette import status
from fastapi import HTTPException
from src.utils.encrypt import (
    encrypt_key,
    generate_tokens,
    validate_refresh_token,
    generate_otp,
    verify_otp,
)
from datetime import datetime
from src.infra.grpc_clients import notifier_grpc_client, admin_grpc_client
from src.infra.cache import cache_manager
import json


class UserService:
    def __init__(self) -> None:
        self.entity = "user"

    def create(self, data: user.InUser):
        """Create user."""
        data.password = encrypt_key(data.password)
        user_data = data.model_dump()
        docid = None
        if user_data.get("extra_data"):
            user_exists = user_repo.get(
                f'{user_data.get("extra_data").get("consumer")}|{user_data.get("extra_data").get("user_id")}'
            )
            if not user_exists:
                user_data.update(user_data.get("extra_data"))
                user_data.pop("extra_data")
                docid = f'{user_data.get("consumer")}|{user_data.get("user_id")}'
            else:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "user already exists"},
            )
        doc_id = user_repo.create(user_data, docid)
        return {"detail": doc_id}

    def get_consumer(self, consumer_id: str):
        """Get consumer by id."""
        cached_data = cache_manager.get(id)
        cached_data = None
        if not cached_data:
            result = admin_grpc_client.unary_call(
                "GetConsumers", "FindConsumers", {"ids": [consumer_id]}
            )
            if not result:
                return None
            result = result.get("consumers")[0]
            return result
        else:
            return cached_data

    def create_admin(self, data: user.InUserAdmin):
        """Create user."""
        data.password = encrypt_key(data.password)
        data = data.model_dump()
        data["is_admin"] = True
        doc_id = user_repo.create(data)
        return {"detail": doc_id}

    def update(self, data):
        return

    def get(self, id):
        return None

    def forget_password(self, email: str):
        """Send email to reset password."""
        return True

    def recovery_password(self, email: str, code: str):
        return True

    def login(self, data: user.LoginUser):
        """Login and generete token of user."""
        if data.email:
            user = user_repo.filter_query(email=data.email)
        elif data.phone:
            user = user_repo.filter_query(phone=data.phone)
        elif data.document:
            user = user_repo.filter_query(document=data.document)

        if not len(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "unauthorized"},
            )
        user = user[0]
        data.password = encrypt_key(data.password)
        if data.password != user.get("password"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "email or password incorrect."},
            )
        tokens = generate_tokens(user)
        return tokens

    def __verify_request_login_in_open(self, phone: str):
        """Verify exists login otp in open."""
        login_code = login_repo.filter_query(phone=phone, is_validated=False)
        if login_code:
            not_used = False
            for each in login_code:
                last_login = datetime.utcfromtimestamp(each.get("created_at"))
                date_now = datetime.now()
                diff_minutes = (date_now - last_login).total_seconds() / 60
                if diff_minutes >= 5:
                    login_repo.update(each.get("_id"), {"is_validated": True})
                else:
                    not_used = True
            if not_used:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "already exists code."},
                )

    def login_passwordless(self, data: user.LoginUser):
        """Send login code with phone or email."""
        # self.__verify_request_login_in_open(data.phone)
        if not data.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "phone is required."},
            )
        user = user_repo.filter_query(phone=data.phone)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "error login user."},
            )
        user = user[0]
        payload = {
            "email": user.get("email"),
            "phone": user.get("phone"),
            "is_validated": False,
            "code": generate_otp(),
            "created_at": datetime.now(),
        }

        send_result = notifier_grpc_client.call(
            "Send",
            "SendEvent",
            {
                "consumer": user.get("consumers")[0],
                "template_type": "login",
                "channel": "sms",
                "payload": json.dumps(
                    {
                        "otp_value": payload.get("code"),
                        "to_number": user.get("phone"),
                    }
                ),
            },
        )
        if not send_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "error send code.please try again."},
            )
        id = login_repo.create(payload)
        return {"id": id}

    def verify_login_code(self, otp: str, id: str):
        """Verify login code."""
        login_code = login_repo.get(id)
        if (
            not login_code
            or login_code.get("code") != otp
            or login_code.get("is_validated")
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "code not valid."},
            )
        if verify_otp(login_code.get("code")):
            login_repo.update(login_code.get("_id"), {"is_validated": True})
            return generate_tokens(login_code)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "invalid code or expired."},
            )

    def refresh_token(self, token: str):
        """Refresh token."""
        tokens = validate_refresh_token(token)
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "error generete new token"},
            )
        return tokens
