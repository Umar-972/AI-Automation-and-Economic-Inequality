from app.analytics import summary
from app.models import Transaction
from datetime import datetime, timezone

class FakeQuery:
    def __init__(self, rows): self.rows = rows
    def filter(self, *args): return self
    def all(self): return self.rows
class FakeDB:
    def __init__(self, rows): self.rows = rows
    def query(self, model): return FakeQuery(self.rows)

def test_empty_summary():
    result = summary(FakeDB([]), 1)
    assert result["income_total"] == 0
    assert result["transaction_count"] == 0
