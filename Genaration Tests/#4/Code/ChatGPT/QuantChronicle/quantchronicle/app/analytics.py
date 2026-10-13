from datetime import datetime, timezone, timedelta
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from app.models import Transaction, FinancialEvent

def transaction_frame(db: Session, user_id: int) -> pd.DataFrame:
    rows = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    data = [{"amount": float(x.amount), "kind": x.kind, "category": x.category,
             "description": x.description, "occurred_at": x.occurred_at} for x in rows]
    if not data:
        return pd.DataFrame(columns=["amount", "kind", "category", "description", "occurred_at"])
    frame = pd.DataFrame(data)
    frame["occurred_at"] = pd.to_datetime(frame["occurred_at"], utc=True)
    frame["month"] = frame["occurred_at"].dt.to_period("M").astype(str)
    frame["signed_amount"] = np.where(frame["kind"].eq("income"), frame["amount"], -frame["amount"])
    return frame

def summary(db: Session, user_id: int) -> dict:
    df = transaction_frame(db, user_id)
    if df.empty:
        return {"income_total": 0, "expense_total": 0, "net": 0, "transaction_count": 0,
                "by_category": [], "monthly": []}
    income = float(df.loc[df.kind == "income", "amount"].sum())
    expenses = float(df.loc[df.kind == "expense", "amount"].sum())
    categories = (df[df.kind == "expense"].groupby("category", as_index=False)["amount"]
                  .sum().sort_values("amount", ascending=False))
    monthly = df.groupby(["month", "kind"], as_index=False)["amount"].sum()
    return {"income_total": round(income, 2), "expense_total": round(expenses, 2),
            "net": round(income-expenses, 2), "transaction_count": int(len(df)),
            "by_category": [{"category": r.category, "amount": round(float(r.amount), 2)} for r in categories.itertuples()],
            "monthly": [{"month": r.month, "kind": r.kind, "amount": round(float(r.amount), 2)} for r in monthly.itertuples()]}

def anomalies(db: Session, user_id: int) -> list[dict]:
    df = transaction_frame(db, user_id)
    expenses = df[df.kind == "expense"].copy()
    if len(expenses) < 8:
        return []
    model = IsolationForest(contamination=0.08, random_state=42)
    expenses["anomaly"] = model.fit_predict(expenses[["amount"]])
    return [{"amount": float(r.amount), "category": r.category, "description": r.description,
             "occurred_at": r.occurred_at.isoformat(), "score": round(float(model.decision_function([[r.amount]])[0]), 4)}
            for r in expenses[expenses.anomaly == -1].itertuples()]

def forecast(db: Session, user_id: int, months: int = 3) -> dict:
    df = transaction_frame(db, user_id)
    now = datetime.now(timezone.utc)
    history = []
    if not df.empty:
        monthly = df[df.kind == "expense"].groupby("month")["amount"].sum().sort_index()
        history = [{"month": str(k), "expense": round(float(v), 2)} for k, v in monthly.items()]
        values = monthly.tail(6).to_numpy(dtype=float)
    else:
        values = np.array([])
    baseline = float(np.mean(values)) if len(values) else 0.0
    # Conservative baseline forecast; with sufficient history use a simple linear trend.
    slope = float(np.polyfit(np.arange(len(values)), values, 1)[0]) if len(values) >= 3 else 0.0
    predictions = []
    for i in range(1, max(1, min(months, 24)) + 1):
        future = (now.replace(day=1) + pd.DateOffset(months=i)).strftime("%Y-%m")
        predictions.append({"month": future, "expense": round(max(0.0, baseline + slope*i), 2)})
    return {"history": history, "forecast": predictions, "method": "six-month mean with linear trend when available"}

def simulate(db: Session, user_id: int, opening_balance: float, months: int = 6) -> dict:
    """Project a month-end balance using recurring transactions and dated events."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=min(max(months, 1), 24) * 31)
    recurring = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.recurring.is_(True)).all()
    events = db.query(FinancialEvent).filter(FinancialEvent.user_id == user_id,
                                              FinancialEvent.scheduled_at >= now,
                                              FinancialEvent.scheduled_at <= end).all()
    balance = float(opening_balance)
    rows = []
    for i in range(1, min(max(months, 1), 24) + 1):
        month_start = (now.replace(day=1) + pd.DateOffset(months=i-1)).to_pydatetime()
        month_end = (now.replace(day=1) + pd.DateOffset(months=i)).to_pydatetime()
        delta = 0.0
        for t in recurring:
            # Recurrence is a planning assumption: weekly=4.345 occurrences/month; monthly/yearly=1/12.
            count = 4.345 if t.recurrence == "weekly" else (1/12 if t.recurrence == "yearly" else 1.0)
            if t.recurrence:
                delta += float(t.amount) * count * (1 if t.kind == "income" else -1)
        for e in events:
            when = e.scheduled_at
            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
            if month_start <= when < month_end:
                delta += float(e.amount) * (1 if e.kind == "income" else -1)
        balance += delta
        rows.append({"month": month_start.strftime("%Y-%m"), "projected_change": round(delta, 2),
                     "projected_balance": round(balance, 2)})
    return {"opening_balance": round(float(opening_balance), 2), "projection": rows,
            "assumptions": ["Recurring entries are treated as active for every projected month.",
                            "Weekly recurrence uses 4.345 occurrences per month; yearly uses 1/12 per month.",
                            "Only scheduled events within the projection window are included."]}
