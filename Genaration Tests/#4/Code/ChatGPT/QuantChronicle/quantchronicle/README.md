# QuantChronicle

QuantChronicle is a full-stack personal finance analytics starter built with FastAPI, PostgreSQL, SQLAlchemy, Pandas, NumPy, scikit-learn, Matplotlib, and Python's timezone-aware `datetime` APIs. It includes a responsive dark dashboard served by FastAPI and a documented REST API.

## Features

- Account registration, password hashing (Argon2), and JWT bearer authentication.
- Transaction ledger with categories, income/expense types, and recurrence metadata.
- Scheduled financial events for future income and expenses.
- Spending summaries, monthly cash-flow aggregation, category breakdowns, spending forecast, and Isolation Forest anomaly flags.
- Cash-position simulation using recurring entries and scheduled events.
- Monthly cash-flow PNG visualization endpoint.
- UTC-normalized timestamp storage and user IANA timezone preferences.
- SQLAlchemy indexes for common user/date queries, dependency-injected sessions, and background analytics refresh hook.
- Responsive dark dashboard with sign-in, transaction/event forms, metrics, charts, forecast, anomalies, and simulation.

## Quick start (Docker Compose)

Requirements: Docker and Docker Compose.

```bash
cp .env.example .env
# Change JWT_SECRET_KEY to a long random secret before exposing the app.
docker compose up --build
```

Open http://localhost:8000. API documentation is at http://localhost:8000/docs.

## Local development

Use Python 3.11+ and a reachable PostgreSQL instance.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The application calls `Base.metadata.create_all()` at startup to make local onboarding easy. For production, replace this with Alembic migrations.

## Configuration

Copy `.env.example` to `.env` and set:

- `DATABASE_URL`: SQLAlchemy PostgreSQL URL (psycopg 3 driver).
- `JWT_SECRET_KEY`: long, randomly generated secret; never use the development default in production.
- `JWT_ALGORITHM`: HS256 by default.
- `ACCESS_TOKEN_MINUTES`: token lifetime in minutes.
- `DEFAULT_TIMEZONE`: default preference for new users (currently the API schema defaults to UTC unless supplied).

## API outline

All routes except health, registration, login, and dashboard require `Authorization: Bearer <access_token>`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Obtain JWT; OAuth2 form field `username` is the email |
| GET | `/api/auth/me` | Current account |
| GET/POST | `/api/transactions` | List/create transactions |
| DELETE | `/api/transactions/{id}` | Delete a transaction |
| GET/POST | `/api/events` | List/create scheduled events |
| DELETE | `/api/events/{id}` | Delete an event |
| GET | `/api/analytics/summary` | Totals, category spending, monthly data |
| GET | `/api/analytics/forecast?months=3` | Expense forecast (1–24 months) |
| GET | `/api/analytics/anomalies` | Unusual expense candidates |
| POST | `/api/analytics/simulate?opening_balance=5000&months=6` | Future cash position projection |
| GET | `/api/visualizations/monthly.png` | Monthly income/expense chart |

### Example requests

Register:

```bash
curl -X POST http://localhost:8000/api/auth/register \\
  -H 'Content-Type: application/json' \\
  -d '{"email":"you@example.com","password":"a-long-unique-password","timezone":"Europe/London"}'
```

Login:

```bash
curl -X POST http://localhost:8000/api/auth/login \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
  -d 'username=you@example.com&password=a-long-unique-password'
```

Create a transaction (timestamps must include a timezone offset):

```bash
curl -X POST http://localhost:8000/api/transactions \\
  -H 'Authorization: Bearer YOUR_TOKEN' -H 'Content-Type: application/json' \\
  -d '{"amount":42.50,"kind":"expense","category":"Food","description":"Lunch","occurred_at":"2026-10-12T12:30:00+01:00"}'
```

## Timestamp and timezone policy

- Incoming transaction/event timestamps must include an offset or timezone; naive timestamps are rejected.
- API input is converted to UTC before persistence. PostgreSQL `TIMESTAMP WITH TIME ZONE` is used via SQLAlchemy `DateTime(timezone=True)`.
- The user's IANA timezone (for example, `Europe/London`) is stored on the account. The frontend renders dates in the browser's local timezone; a production UI should use the account's saved timezone explicitly for consistent cross-device display.
- Use aware `datetime` values and `zoneinfo.ZoneInfo`; never assume server-local time.
- PostgreSQL normalizes `TIMESTAMPTZ` internally; clients may receive equivalent UTC offsets based on connection/session configuration.

## Analytics notes

- Forecasting uses a transparent baseline: mean expense across up to six recent months, with a linear trend if there are at least three monthly observations. This is a baseline forecast, not financial advice.
- Isolation Forest flags potentially unusual expenses. It needs at least eight expense rows and can generate false positives; it does not determine fraud.
- Simulation treats recurring entries as active in each forecast month and uses 4.345 occurrences per month for weekly recurrence. Yearly recurrence is modeled as one-twelfth of an occurrence each month. Events are applied to the month in which they are scheduled. This is a planning estimate, not a guarantee.
- Background analytics refresh is a lightweight FastAPI `BackgroundTasks` hook. For durable, retriable jobs at scale, use Celery/RQ/Arq with Redis and a persisted analytics cache.

## Security and production hardening

Before deployment:
1. Set a strong unique `JWT_SECRET_KEY` from a secret manager.
2. Serve behind HTTPS; configure trusted hosts and restrictive CORS if the frontend is hosted separately.
3. Add rate limiting, login throttling, email verification, password reset, audit logging, and account deletion workflows.
4. Add Alembic migrations and a migration release process.
5. Use a durable background queue and observability/alerting.
6. Review retention, backups, encryption at rest, and applicable privacy/regulatory requirements.
7. Add integration tests against PostgreSQL and a CI pipeline. The included tests cover password/JWT utilities and the empty analytics summary only.

## Tests

```bash
pytest
```

## Project structure

```text
app/
  analytics.py     # Pandas/NumPy/sklearn analytics and simulation
  config.py        # Environment-based configuration
  database.py      # SQLAlchemy engine/session
  deps.py          # JWT-authenticated user dependency
  jobs.py          # Background refresh hook
  main.py          # REST API, dashboard, Matplotlib chart
  models.py        # SQLAlchemy models
  schemas.py       # Pydantic request/response validation
  security.py      # Argon2 hashing and JWT utilities
  static/index.html
tests/
  test_analytics.py
  test_security.py
```

## License

MIT-style starter template; add a formal license before redistribution.
