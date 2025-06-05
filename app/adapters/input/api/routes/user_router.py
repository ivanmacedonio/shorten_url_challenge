from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_all_users():
    return [1,2,3,4,5]