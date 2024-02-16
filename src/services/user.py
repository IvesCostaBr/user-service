from src.repositorys import (
    user_repo,
    login_repo,
    login_token_repo,
    blacklist_repo,
    program_referal_repo,
    rate_repo
)
from src.models import user, program_referal as program_referal_model
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
from src.infra.grpc_clients import notifier_grpc_client
from src.utils.helper import remove_special_character
import json

from src.services import program_referal_service


class UserService:
    def __init__(self) -> None:
        self.entity = "user"
        self.program_referal_service = program_referal_service

    def create(self, data: user.InUser, user_admin: dict = None, consumer_id: str = None):
        """Create user."""
        tokens = {}
        data.password = encrypt_key(data.password)
        user_data = data.model_dump()
        user_data["is_admin"] = False
        docid = None
        if user_data.get("extra_data"):
            user_exists = user_repo.get(
                f'{user_data.get("extra_data").get("consumer")}|{user_data.get("extra_data").get("user_id")}'
            )
            if not user_exists:
                user_data.update(user_data.get("extra_data"))
                document = user_data.get('document')
                if document:
                    user_data["document"] = remove_special_character(document)
                user_data.pop("extra_data")
                docid = f'{user_data.get("consumer")}|{user_data.get("user_id")}'
                if consumer_id:
                    user_data["consumer"] = consumer_id
                    tokens = self.generate_unique_token(docid)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "user already exists"},
                )
        elif user_admin or consumer_id:
            # validar se não existe outro usuario admin com o mesmo email, documento ou telefone.
            user_data["is_admin"] = True
            user_data["consumers"] = [user_admin.get(
                "consumer_id") if user_admin else consumer_id]
            docid = user_repo.create(user_data, docid)
            tokens = self.generate_unique_token(docid)
            return {"detail": docid, "access_token": tokens.get("access_token", '')}

        # create referal code
        user_data["invitation_id"] = data.referal_id
        docid = user_repo.create(user_data, docid)
        user_data["id"] = docid
        self.__create_referal_code(user_data)
        return {"detail": docid, "access_token": tokens.get("access_token", '')}

    def __create_referal_code(self, user: dict):
        """Create referal code and rate."""
        try:
            consumer_id = user.get('consumer') or user.get('consumer_id')
            consumer_rate = rate_repo.filter_query(
                consumer_id=consumer_id, is_default=True
            )
            if consumer_rate:
                consumer_rate = consumer_rate[0]
            else:
                consumer_rate = {}
            payload = program_referal_model.InProgramReferal(
                user_id=user.get("id"),
                consumer_id=consumer_id,
                rate_id=consumer_rate.get('id')
            )
            self.program_referal_service.create(user, payload)
        except Exception as ex:
            self.__raise_http_error(status.HTTP_400_BAD_REQUEST, {
                "error": "error in create referal code.", "description": str(ex)})

    def create_admin(self, data: user.InUserAdmin):
        """Create user."""
        data.password = encrypt_key(data.password)
        data = data.model_dump()
        data["is_admin"] = True
        data["is_super"]
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

    def __raise_http_error(self, status_code: int, msg: dict):
        """Generate http error."""
        raise HTTPException(
            status_code=status_code,
            detail=msg
        )

    def login(self, data: user.LoginUser):
        """Login and generete token of user."""
        query = {"consumer": data.consumer_id} if data.consumer_id else {}
        query["is_admin"] = data.is_admin
        if data.email:
            query["email"] = data.email
        elif data.phone:
            query["phone"] = data.phone
        elif data.document:
            query["document"] = data.document
        else:
            self.__raise_http_error(status.HTTP_401_UNAUTHORIZED, {
                                    "error": "unauthorized"})

        user = user_repo.filter_query(**query)
        if not user:
            self.__raise_http_error(status.HTTP_401_UNAUTHORIZED, {
                                    "error": "unauthorized"})
        user = user[0]
        data.password = encrypt_key(data.password)
        if data.password != user_repo.get_password(user.get("id")):
            self.__raise_http_error(status.HTTP_401_UNAUTHORIZED, {
                                    "error": "incorrect credentials"})
        tokens = generate_tokens(user)
        if not tokens:
            self.__raise_http_error(status.HTTP_401_UNAUTHORIZED, {
                                    "error": "error generete new token"})
        return tokens

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

    def get_user_admin(self, user_admin: dict):
        """List user admin."""
        consumer_id = user_admin.get("consumer_id")
        result = user_repo.filter_query(
            consumers__in=[consumer_id], is_admin=True)
        return {"data": result, "total": len(result)}

    def get_super_admin(self):
        """List super admin."""

        result = user_repo.filter_query(is_super_admin=True)
        return {"data": result, "total": len(result)}

    def get_user(self, id: str, user_admin: dict):
        """Get user admin."""
        user = user_repo.get(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "user not found"},
            )
        if user.get("is_admin") and user_admin.get("consumer_id") in user.get(
            "consumers"
        ):
            return user
        elif user.get("is_super_admin") and user_admin.get("is_super_admin"):
            return user

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "user not found"},
        )

    def generate_unique_token(self, user: dict):
        """Generate unique token to user."""
        if type(user) != str:
            user_id = user.get("_id") if user.get("_id") else user.get("id")
        else:
            user_id = user
        result = login_token_repo.filter_query(user_id=user_id, is_active=True)
        if result:
            for each in result:
                login_token_repo.update(each.get("id"), {"is_active": False})
                blacklist_repo.create({"access_token": each.get("token")})
        tokens = generate_tokens(user, 4000)
        login_token_repo.create(
            {"user_id": user_id, "token": tokens.get("access_token")})
        return {"access_token": tokens.get("access_token")}
