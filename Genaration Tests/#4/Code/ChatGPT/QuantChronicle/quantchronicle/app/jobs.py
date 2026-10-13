"""Background analytics task hooks.

For a single-process starter, FastAPI BackgroundTasks can run refresh_analytics.
For production, replace this with a durable queue (Celery/RQ/Arq) and persisted result cache.
"""
from app.analytics import summary

def refresh_analytics(db_factory, user_id: int) -> dict:
    db = db_factory()
    try:
        return summary(db, user_id)
    finally:
        db.close()
