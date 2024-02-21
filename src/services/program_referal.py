from src.repositorys import program_referal_repo, rate_repo, user_repo
from fastapi import HTTPException
from starlette import status
from src.models import program_referal
from datetime import datetime


class ProgramReferalService:
    def __init__(self) -> None:
        self.entity = "program_referal"

    def __get_rate_consumer_default(self, consumer_id: str):
        """Get rate default of consumer."""
        consumer_rate = rate_repo.filter_query(
            consumer_id=consumer_id, is_default=True
        )
        if consumer_rate:
            return consumer_rate[0].get('id')
        raise Exception(
            "error in create new referal code, rate default not found")

    def create(self, user: dict, data: program_referal.InProgramReferal):
        """Create new referal code user."""
        try:
            data = data.model_dump()

            if not user.get('is_admin'):
                consumer = user.get("consumer")
                data["user_id"] = user.get('id')
                data["rate_id"] = self.__get_rate_consumer_default(consumer)
            else:
                consumer = user.get("consumer_id")
                data["admin"] = {
                    "id": user.get("id"),
                    "email": user.get("email")
                }
                data["principal"] = data.get("principal")
            data["consumer_id"] = consumer
            docid = program_referal_repo.create(**data)
            return {"detail": docid, "name": data.get('name')}
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": str(ex)}
            )

    def get_referals_data(self, user: dict):
        """"""
        default_referal = program_referal_repo.filter_query(
            consumer_id=user.get('consumer'), principal=True)
        if not default_referal:
            return
        else:
            default_referal = default_referal[0]
        rates = {"main": default_referal, "users": {}}
        referal = program_referal_repo.get(user.get('invitation_id'))
        if not referal:
            return rates
        elif referal and not referal.get('admin'):
            user_inviter = user_repo.get(referal.get('user_id'))
            if user_inviter:
                rates["users"][user_inviter.get("id")] = referal.get("rate")
                invited_referal = program_referal_repo.get(
                    user_inviter.get('invitation_id'))
                if invited_referal and not invited_referal.get('admin'):
                    invited_user = user_repo.get(
                        invited_referal.get('user_id'))
                    rates["users"][invited_user.get(
                        "id")] = invited_referal.get("rate")

        return rates

    def get_list(self, filter: dict):
        """"""
        return []

    def get_all_user_invited(self, user: dict, user_id: str):
        """Get all user invited."""
        user = user_repo.get(user_id)
        if not user:
            return []
        referal_id = user.get(user.get('referal_id'))

        invites = user_repo.filter_query(
            referal_id=referal_id, get_fields=[
                "id", "document", "name", "created_at"
            ]
        )

        return invites

    def get_user_referal_codes(self, user: dict):
        """Get referal code of user."""
        result = program_referal_repo.filter_query(
            user_id=user.get('id'),
            consumer_id=user.get("consumer")
        )
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not found referal code"}
        )

    def validate_code(self, consumer_id: str, code: str):
        """Validate code referal."""
        try:
            user_code = program_referal_repo.filter_query(
                name=code,
                consumer_id=consumer_id,
                is_active=True
            )
            if not user_code:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": "not found referal code or not valid"}
                )
            user_code = user_code[0]
            # validate if expired_at já venceu
            if user_code.get('expired_at') and user_code.get('expired_at') < datetime.now():
                raise Exception("Referal code expired")
            user_data = user_repo.get(user_code.get('user_id'))
            if not user_data:
                raise Exception("user not found")
            result = False
            if consumer_id:
                if not user_data.get('consumer') == consumer_id:
                    raise Exception("291 - referal code not available")
            return {"valid": result, "referal_id": user_code.get('id')}
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": str(ex)}
            )
