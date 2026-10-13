from fastapi import APIRouter
from app.services.analytics_service import AnalyticsService
router=APIRouter(prefix="/analytics")
@router.get("/summary")
def summary(): return AnalyticsService().summary([10,20,30])
