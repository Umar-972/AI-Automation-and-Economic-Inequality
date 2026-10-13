from fastapi import APIRouter
router=APIRouter(prefix="/transactions")
@router.get("")
def list_transactions(): return []
