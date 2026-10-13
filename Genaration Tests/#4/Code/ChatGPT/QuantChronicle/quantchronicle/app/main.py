from datetime import datetime, timezone
from io import BytesIO
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from app.database import Base, engine, get_db, SessionLocal
from app.models import User, Transaction, FinancialEvent
from app.schemas import UserCreate, UserOut, TokenOut, TransactionCreate, TransactionOut, EventCreate, EventOut
from app.security import hash_password, verify_password, create_access_token
from app.deps import current_user
from app.analytics import summary, anomalies, forecast, simulate
from app.jobs import refresh_analytics

app = FastAPI(title="QuantChronicle API", version="1.0.0",
              description="Personal finance tracking, analytics, forecasting and simulation.")
Base.metadata.create_all(bind=engine)

def utc(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise HTTPException(status_code=422, detail="Timestamp must include timezone")
    return dt.astimezone(timezone.utc)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "QuantChronicle"}

@app.post("/api/auth/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        ZoneInfo(payload.timezone)
    except ZoneInfoNotFoundError:
        raise HTTPException(status_code=422, detail="Unknown IANA timezone")
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password), timezone=payload.timezone)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")
    return user

@app.post("/api/auth/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username.lower()).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user

@app.get("/api/transactions", response_model=list[TransactionOut])
def list_transactions(limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0),
                      user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id == user.id).order_by(Transaction.occurred_at.desc()).offset(offset).limit(limit).all()

@app.post("/api/transactions", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate, user: User = Depends(current_user), db: Session = Depends(get_db),
                       background_tasks: BackgroundTasks = None):
    if payload.recurring and not payload.recurrence:
        raise HTTPException(status_code=422, detail="recurrence is required for recurring transactions")
    item = Transaction(user_id=user.id, amount=payload.amount, kind=payload.kind, category=payload.category,
                       description=payload.description, occurred_at=utc(payload.occurred_at),
                       recurring=payload.recurring, recurrence=payload.recurrence)
    db.add(item); db.commit(); db.refresh(item)
    if background_tasks:
        background_tasks.add_task(refresh_analytics, SessionLocal, user.id)
    return item

@app.delete("/api/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(item); db.commit()

@app.get("/api/events", response_model=list[EventOut])
def list_events(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(FinancialEvent).filter(FinancialEvent.user_id == user.id).order_by(FinancialEvent.scheduled_at).all()

@app.post("/api/events", response_model=EventOut, status_code=201)
def create_event(payload: EventCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = FinancialEvent(user_id=user.id, title=payload.title, amount=payload.amount, kind=payload.kind,
                         scheduled_at=utc(payload.scheduled_at), notes=payload.notes)
    db.add(item); db.commit(); db.refresh(item)
    return item

@app.delete("/api/events/{event_id}", status_code=204)
def delete_event(event_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    item = db.query(FinancialEvent).filter(FinancialEvent.id == event_id, FinancialEvent.user_id == user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Event not found")
    db.delete(item); db.commit()

@app.get("/api/analytics/summary")
def analytics_summary(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return summary(db, user.id)

@app.get("/api/analytics/forecast")
def analytics_forecast(months: int = Query(3, ge=1, le=24), user: User = Depends(current_user), db: Session = Depends(get_db)):
    return forecast(db, user.id, months)

@app.get("/api/analytics/anomalies")
def analytics_anomalies(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return {"anomalies": anomalies(db, user.id), "note": "Statistical flags are indicators, not fraud determinations."}

@app.post("/api/analytics/simulate")
def analytics_simulate(opening_balance: float = Query(..., ge=-1_000_000_000, le=1_000_000_000),
                       months: int = Query(6, ge=1, le=24), user: User = Depends(current_user), db: Session = Depends(get_db)):
    return simulate(db, user.id, opening_balance, months)

@app.get("/api/visualizations/monthly.png")
def monthly_chart(user: User = Depends(current_user), db: Session = Depends(get_db)):
    data = summary(db, user.id)["monthly"]
    months = sorted(set(x["month"] for x in data))
    income = {x["month"]: x["amount"] for x in data if x["kind"] == "income"}
    expenses = {x["month"]: x["amount"] for x in data if x["kind"] == "expense"}
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor="#111827")
    ax.set_facecolor("#111827")
    xs = list(range(len(months)))
    width = 0.38
    ax.bar([x-width/2 for x in xs], [income.get(m, 0) for m in months], width, label="Income", color="#34d399")
    ax.bar([x+width/2 for x in xs], [expenses.get(m, 0) for m in months], width, label="Expenses", color="#fb7185")
    ax.set_xticks(xs, months, rotation=35, ha="right")
    ax.tick_params(colors="#cbd5e1")
    ax.spines[:].set_color("#475569")
    ax.grid(axis="y", alpha=.18)
    ax.legend(facecolor="#1f2937", labelcolor="#e5e7eb")
    ax.set_title("Monthly cash flow", color="#f8fafc")
    fig.tight_layout()
    buf = BytesIO(); fig.savefig(buf, format="png", dpi=140); plt.close(fig); buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/", include_in_schema=False)
def dashboard():
    from fastapi.responses import FileResponse
    import os
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))
