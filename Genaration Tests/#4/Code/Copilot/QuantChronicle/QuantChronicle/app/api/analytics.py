from fastapi import APIRouter
router=APIRouter(prefix="/analytics",tags=["analytics"])

@router.get("/summary")
def summary():
    return {"message":"analytics summary"}
