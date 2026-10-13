from fastapi import FastAPI
from app.api import auth,transactions,events,analytics,simulation
app=FastAPI(title="QuantChronicle")
for r in [auth.router,transactions.router,events.router,analytics.router,simulation.router]: app.include_router(r)
@app.get("/")
def root(): return {"app":"QuantChronicle"}
