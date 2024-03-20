from src.repositorys import program_referal_repo, rate_repo, user_repo
from fastapi import HTTPException
from starlette import status
from src.models import program_referal
from datetime import datetime
import threading


class ProgramReferalService:
    def __init__(self) -> None:
        self.entity = "program_referals"

    def update(self, user: dict, id: str, data: program_referal.UpdateProgramReferal):
        """Update referal code data."""
        try:
            referal_code = program_referal_repo.get(id)
            if not referal_code:
                raise Exception("referal code not found.")
            elif referal_code.get("consumer_id") != user.get("consumer_id"):
                raise Exception("referal code not found")
            program_referal_repo.update(id, **data.model_dump())
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": str(ex)}
            )

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

            data["name"] = data.get("name").replace(" ", "").lower()
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
            name_exists = program_referal_repo.filter_query(
                name=data.get("name"), consumer_id=consumer
            )
            if name_exists:
                raise Exception("name already registred")

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
        rates = {}
        default_referal = program_referal_repo.filter_query(
            consumer_id=user.get('consumer'), principal=True)
        if not default_referal:
            return
        else:
            default_referal = default_referal[0]
            rate = rate_repo.get(default_referal.get('rate_id'))
            if not rate:
                rates["main"] = {}
            else:
                rates["main"] = rate
                rates["main"]["user_id"] = default_referal.get('user_id')
        rates["users"] = {}
        referal = program_referal_repo.get(user.get('referal_id'))
        if not referal:
            return rates
        elif referal:
            user_inviter = user_repo.get(referal.get('user_id'))
            if user_inviter:
                rates["users"][user_inviter.get("id")] = referal.get("rate")
                invited_referal = program_referal_repo.get(
                    user_inviter.get('referal_id'))
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
        referal_id = user.get('referal_id')

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
        if not result:
            data = self.create(user, program_referal.InProgramReferal(
                consumer_id=user.get("consumer"),
                user_id=user.get('id'),
            ))

            result = [{
                "id": data.get("detail"),
                "name": data.get("name")
            }]

        return {"data": result, "total": len(result)}

    def validate_code(self, consumer_id: str, code: str):
        """Validate code referal."""
        try:
            user_code = program_referal_repo.filter_query(
                name=code.lower(),
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
            if consumer_id:
                if not user_data.get('consumer') == consumer_id:
                    raise Exception("291 - referal code not available")
            return {"valid": True, "referal_id": user_code.get('id')}
        except Exception as ex:
            return {"valid": False, "referal_id": None}

    def get_program_referal_consumer(self, user: dict):
        """Get all referal codes of user."""
        codes = program_referal_repo.filter_query(
            consumer_id=user.get('consumer_id'),
        )
        for each in codes:
            each["rate"] = rate_repo.get(each.get("rate_id"))
            each["user"] = user_repo.get(each.get("user_id"))
            each.pop("rate_id"), each.pop("user_id")
        return codes

    def bulk_update_referal_code_users(self, users: list, referal: dict):
        for each in users:
            user_repo.update(each.get("id"), {"referal_id": referal.get("id")})

    def __delete_referal_code(self, referal_code: dict, default_code: dict):
        """Delete referal code async."""

        users_use_code = user_repo.filter_query(
            referal_id=id, consumer=default_code.get("consumer_id"))
        if users_use_code:
            self.bulk_update_referal_code_users(users_use_code, default_code)

        program_referal_repo.delete(referal_code.get("id"))

    def delete(self, user: str, id: str):
        """Delete referal code."""
        try:
            default_program_referal = program_referal_repo.filter_query(
                consumer_id=user.get("consumer_id"), principal=True)
            if not default_program_referal:
                raise Exception("default code not configurated.")

            delete_code = program_referal_repo.get(id)
            if not delete_code:
                raise Exception("referal code not found")

            threading.Thread(target=self.__delete_referal_code(), args=(
                delete_code, default_program_referal)).start()
            return {"detail": True}
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": str(ex)}
            )
