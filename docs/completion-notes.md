
# Completion pass notes

This document records the completion state of ResortBI, an independent hospitality BI portfolio prototype.

## Implemented

- Corrected occupancy to use room-nights and to count actual `Checked In` / `Checked Out` stays, not merely confirmed future bookings.
- Standardized analytics API date parsing and inclusive check-in date filters.
- Excluded cancelled reservations from reservation-value analytics and separated unknown country from foreign country.
- Added dashboard revenue-decline alert output and made the frontend display it when triggered.
- Replaced placeholder analytics pages with API-connected dashboard, reservation-value, occupancy, visitor, and CSV report views.
- Added shared frontend date/resort filters, loading/error handling, refresh controls, and session-expiry handling.
- Added role permissions for analytics and ingestion endpoints, plus a current-user endpoint so the frontend can show navigation appropriate to the user’s Django Groups.
- Fixed reservation validation for room-count defaults, date formats, non-object payloads, and amount parsing.
- Moved the Django secret key and host/CORS configuration to environment variables and added safe example environment files.
- Added backend tests for reservation-value calculations, occupancy room-nights, country classification, and input validation.
- Added setup, API, architecture, metric-definition, and security documentation.

## Verification status

- Python source compilation completed successfully.
- Standalone validation, transformation, mapping, and reconciliation scripts ran successfully.
- Full Django tests were not run in this workspace because Django and the project dependencies are not installed here; the local database connection was not available for verification.
- The React production build/lint were not verified because the frontend dependencies could not be installed in the workspace.
- The user should run the documented Django tests and frontend lint/build after installing dependencies and configuring `config/.env`.

## Known scope limits

- No live external property-management-system (PMS) API or scheduled source synchronisation is configured in this repository.
- Reservation amounts are not reconciled against actual payments; the UI labels them reservation value.
- Temporary room closures and guest headcounts are not represented in the current source models.
- Session tokens are stored in `sessionStorage` for this prototype. A production deployment needs a security review and a stronger token-storage approach.
