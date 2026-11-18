
# Architecture and data flow

## Request flow

1. A user signs in through the React login form.
2. Django REST Framework Simple JWT returns an access token and a refresh token. The frontend requests `/api/auth/me/` to read the current username and Django Groups for role-aware navigation.
3. Protected React pages call the API with the access token.
4. Django checks the user's Django Group before returning protected data.
5. Analytics services query the trusted reservation layer and room inventory.
6. The frontend presents results and can export a resort summary as CSV.

## Reservation processing flow

```text
Source reservation payload
          |
          v
StagedReservation (raw JSON + source metadata)
          |
          v
Validate required fields and dates
          |
          v
Map source resort/status values and normalize names, countries, dates, amounts
          |
          v
Check the resort exists and is active
          |
          v
TrustedReservation
          |
          v
Analytics services
          |
          v
React dashboard, analytics pages, and CSV export
```

A failed validation updates the staged record with a failure status and error details. The current project has a JSON API ingestion workflow. A live external property-management-system (PMS) connection and scheduled source synchronisation are outside the current scope.

## Authorization matrix

| Group | Dashboard / reservation value / alerts | Occupancy / country summary | Trusted reservation listing / ingestion |
|---|---|---|---|
| Administrator | Yes | Yes | Yes |
| Executive | Yes | Yes | No |
| Manager | Yes | Yes | No |
| Analyst | No | Yes | Yes |
| Other authenticated user | No | No | No |

The Django Group names must match exactly. A superuser is not automatically in a custom group.

## Current metric rules

- Date filters on check-in-based metrics include both start and end dates.
- Revenue endpoints currently aggregate reservation amounts, not verified payments.
- Occupancy counts `Checked In` and `Checked Out` stays. `Confirmed` bookings are not treated as actual occupancy; cancelled bookings are excluded.
- Occupancy is based on room-nights; active room inventory is assumed available throughout the range.
- Visitor counts represent reservation records. They are not a deduplicated count of guests or people.
