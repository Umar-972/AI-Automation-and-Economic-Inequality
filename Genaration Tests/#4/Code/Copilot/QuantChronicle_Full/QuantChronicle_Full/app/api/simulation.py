from fastapi import APIRouter
router=APIRouter(prefix="/simulation")
@router.get("/forecast")
def forecast(): return {"projected_balance":10000}
