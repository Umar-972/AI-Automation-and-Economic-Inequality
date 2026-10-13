from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey, Numeric, Boolean, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    events: Mapped[list["FinancialEvent"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (Index("ix_transactions_user_occurred", "user_id", "occurred_at"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False) # positive magnitude
    kind: Mapped[str] = mapped_column(String(16), nullable=False) # income | expense
    category: Mapped[str] = mapped_column(String(80), default="Uncategorized", nullable=False)
    description: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence: Mapped[str | None] = mapped_column(String(16), nullable=True) # weekly | monthly | yearly
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    user: Mapped[User] = relationship(back_populates="transactions")

class FinancialEvent(Base):
    __tablename__ = "financial_events"
    __table_args__ = (Index("ix_events_user_scheduled", "user_id", "scheduled_at"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False) # income | expense
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    user: Mapped[User] = relationship(back_populates="events")
