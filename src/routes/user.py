from fastapi.routing import APIRouter

router = APIRouter(tags=["User"])

@router.get("/user")
async def get_user():
    return {"message": "Hello World"}