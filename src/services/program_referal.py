from src.repositorys import program_referal_repo, user_repo
from fastapi import HTTPException
from starlette import status


class ProgramReferalService:
    def __init__(self) -> None:
        self.entity = "program_referal"

    def create(self, user: dict):
        """Create new referal code user."""
        result = program_referal_repo.create(user_id=user.get('id'))
        return {"code": result}

    def get_list(self, filter: dict):
        """"""

    def get(self, code: str):
        """"""

    def get_user_referal_code(self, user: dict):
        """Get referal code of user."""
        result = program_referal_repo.filter_query(
            user_id=user.get('id'),
            is_active=True
        )
        if result:
            return {"code": result[0].get("code")}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not found referal code"}
        )

    def validate_code(self, consumer_id: str, code: str):
        """Validate code referal."""
        user_code = program_referal_repo.filter_query(
            code=code,
            is_active=True
        )
        if not user_code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "not found referal code or not valid"}
            )
        user_code = user_code[0]
        user_data = user_repo.get(user_code.get('user_id'))
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "user not found"}
            )
        result = False
        if consumer_id:
            if user_data.get('consumer') == consumer_id:
                result = True
            else:
                result = False
        return {"valid": result, "name": user_code.get('name')}
