from starlette import status
from src.repositorys import rate_repo
from fastapi import HTTPException
from src.models import rate


class RateService:
    def __init__(self) -> None:
        self.repo = rate_repo
        self.entity = "rate"

    def __validate_default_rate(self, consumer_id: str):
        """Validate if exists one rate already configured."""
        result = rate_repo.filter_query(
            consumer_id=consumer_id, is_default=True)
        if result:
            raise Exception("already rate default configured.")

    def create(self, data: rate.InRate, admin_user: dict = None):
        """Create a new rate of consumer."""
        try:
            self.__validate_default_rate(admin_user.get("consumer_id"))

            payload = data.model_dump()
            payload["consumer_id"] = admin_user.get("consumer_id")
            payload["admin_user"] = {
                "id": admin_user.get("id"),
                "email": admin_user.get("email"),
            }

            return {"detail": rate_repo.create(payload)}
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ex),
            )

    def get_all(self):
        """List all rate."""
        rates = rate_repo.get_all()
        return {"data": rates, "total": len(rates)}

    def get(self, user: dict, id: str):
        """Get detail credential."""
        rate = rate_repo.get(id)
        if not rate or rate.get('consumer_id') != user.get('consumer_id'):
            raise self.__exception_rate_not_found()
        return rate

    def __exception_rate_not_found(self):
        """Exception rate not found."""
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rate not found",
        )

    def processor_rate_values(self, user: dict, amount: float):
        """Process tax of user."""
        receivers = []

    def list_rates(self, user: dict):
        """List all rates of consumer."""
        rates = rate_repo.filter_query(consumer_id=user.get("consumer_id"))
        return rates

    def update(self, user: dict, rate_id: str, data: rate.InRate):
        """Update rate."""
        try:
            data = data.model_dump()
            for each in data.keys():
                if not data.get(each):
                    data.pop(each)
            rate = rate_repo.get(rate_id)
            if not rate:
                raise Exception("rate not found.")
            rate_repo.update(rate_id, data)
            return {"detail": True}
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": str(ex)}
            )
