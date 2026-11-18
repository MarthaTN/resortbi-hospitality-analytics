
# ResortBI — Hospitality Business Intelligence Portal

ResortBI is an independent portfolio project demonstrating how hospitality reservation data can be validated, processed, and presented through a business intelligence dashboard. It is built with Django REST Framework, PostgreSQL, and React.

**Project status:** portfolio prototype using demonstration data and a JSON API ingestion workflow. It is not commissioned, endorsed, or affiliated with NWR, any hospitality operator, or any property-management-system vendor. It does not contain proprietary business data, third-party logos, or a live external PMS integration.

## Current scope

- JWT sign-in and protected frontend routes.
- Role-based API permissions using Django Groups.
- Reservation ingestion into a staging layer and processing into trusted reservations.
- Dashboard summary, reservation value by resort, occupancy room-night calculations, country breakdown, revenue-decline alerts, and CSV report export (output only).
- PostgreSQL configuration through environment variables.

## Technology

- Backend: Python, Django, Django REST Framework, Simple JWT.
- Database: PostgreSQL.
- Frontend: React, Vite, React Router.
- Data pipeline: staging, validation, mapping/transformation, and trusted reservation records.

## Setup

### 1. Backend

Use Python 3.12+ and PostgreSQL. Create a PostgreSQL database and user, then create a local environment file:

```bash
copy config\.env.example config\.env
```

On macOS/Linux:

```bash
cp config/.env.example config/.env
```

Edit `config/.env` and enter your database credentials. Set `SECRET_KEY` to a long, random value. Do not commit `config/.env`.

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

### 2. Create the role groups

Log in to Django admin at `/admin/` and create these exact Groups:

- `Administrator`
- `Executive`
- `Manager`
- `Analyst`

Assign users to groups according to the intended access policy. Users without a permitted group may sign in but will receive `403 Forbidden` from restricted endpoints. A Django superuser is not automatically a member of these custom groups.

### 3. Frontend

In a second terminal:

```bash
cd frontend
npm ci
```

Optionally copy `.env.example` to `.env` and change `VITE_API_BASE_URL` if the backend is hosted elsewhere. Then run:

```bash
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## Main API endpoints

All analytics endpoints require a JWT access token.

| Method | Endpoint | Intended access |
|---|---|---|
| POST | `/api/auth/token/` | Obtain access and refresh tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |
| GET | `/api/auth/me/` | Current username and Django Groups |
| GET | `/api/analytics/dashboard/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Administrator, Executive, Manager |
| GET | `/api/analytics/revenue/` | Administrator, Executive, Manager |
| GET | `/api/analytics/revenue/comparison/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Administrator, Executive, Manager |
| GET | `/api/analytics/occupancy/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Administrator, Executive, Manager, Analyst |
| GET | `/api/analytics/visitors/` | Administrator, Executive, Manager, Analyst |
| GET | `/api/analytics/alerts/revenue/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Administrator, Executive, Manager |
| GET | `/api/trusted-reservations/` | Administrator, Analyst |
| POST | `/api/ingestion/reservations/` | Administrator, Analyst |

Analytics dates use `YYYY-MM-DD`. The start and end dates are inclusive for check-in-based summaries. Occupancy counts nights within the selected date range; a reservation's check-out date itself is not an occupied night.

## Metric definitions and limitations

- **Reservation value:** sum of reservation amounts on trusted reservation records, grouped by check-in date. It is not verified cash collected or audited accounting revenue. Payment reconciliation must be implemented before presenting it as actual collected revenue.
- **Occupancy:** occupied room-nights divided by active-room available room-nights. The current model assumes active rooms were available throughout the period; it does not yet track temporary room closures.
- **Visitor overview:** counts reservation records by country, not unique people. A guest may have more than one reservation, and the source model does not contain a guest headcount.
- **Booking statuses:** reservation-value and country summaries count `Confirmed`, `Checked In`, and `Checked Out` records, excluding `Cancelled`. Actual occupancy counts only `Checked In` and `Checked Out` stays; `Confirmed` bookings are not treated as actual occupancy.
- **Resort matching:** trusted reservations store a resort name as text, while room inventory uses a foreign key. Source resort naming must be kept consistent for resort-specific metrics.
- **Data integration:** the current prototype accepts reservation records through its JSON ingestion API. It does not connect to a live property management system (PMS), run scheduled external synchronisation, or include a CSV/Excel import workflow.

## Security and deployment notes

- Never commit `.env`, database credentials, or production secret keys.
- `DEBUG=True` and the listed CORS origins are for local development. Configure `DEBUG=False`, a strong `SECRET_KEY`, `ALLOWED_HOSTS`, and production CORS origins before deployment.
- Frontend tokens currently use `sessionStorage`. This is a practical prototype approach, not the preferred storage strategy for a production application handling sensitive business data. Consider secure HttpOnly cookies, CSRF protections, HTTPS, and a formal security review before production.
- Role names are enforced by custom permission classes and must match the Django Group names exactly.

## Checks

Run backend tests with:

```bash
python manage.py test
```

Run frontend lint and production build with:

```bash
cd frontend
npm run lint
npm run build
```

These checks should be run in an environment with the dependencies installed and a configured test database.
