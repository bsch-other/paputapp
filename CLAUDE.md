# CLAUDE.md

## Project: Pet Library — Automated Testing Demo

A small, fully-local web application built to demonstrate automated UI and REST API testing to non-technical and low-technical audiences. The application itself is intentionally simple; its purpose is to be a clear, visually engaging target for a parallel test suite.

## Goals

- **Pedagogical clarity over feature richness.** Every feature must justify itself as a teaching opportunity. If a feature doesn't generate an interesting test case, it doesn't belong in v1.
- **Visual legibility.** State changes must be obvious on screen so Allure screenshots tell a story to non-technical viewers.
- **Parallel test stories.** Every user-facing flow should map cleanly to both a Selenium UI test and a REST API test, so the demo can contrast the two approaches side by side.

## Constraints

- Runs entirely on `localhost`. No remote services, no cloud dependencies.
- Runs under a standard user account with no elevated permissions. No system-level installs.
- No containers (Docker, Podman, etc.) in v1. Dependency isolation via Python virtual environments only.
- Python-first stack. No JavaScript frameworks. Server-rendered HTML only.
- Test stack is fixed: **pytest + Selenium + Allure**.

## Stack

- **Language:** Python (managed via `uv` or plain `venv`)
- **API service:** FastAPI + SQLAlchemy (port 8000)
- **UI service:** FastAPI + Jinja2Templates (port 8001, consumes the API service over HTTP)
- **Database:** SQLite (single file on disk)
- **Image storage:** Local `media/` directory on disk
- **Auth:** Session cookies, shared between API and UI
- **Server:** Uvicorn for both services
- **Process model:** Two processes on two localhost ports (API and UI)

The two-service split is deliberate: it makes the testing-layers story visible. API tests hit the API service directly; UI tests drive the UI frontend through Selenium.

Flask was considered and rejected: Werkzeug's dev server has reliability issues on Windows (reloader conflicts, port binding quirks). Both services use FastAPI + Uvicorn for a consistent, stable runtime. The UI service uses FastAPI's `Jinja2Templates` for server-rendered HTML — no Flask-specific patterns (`current_app`, `g`, application context) to learn or debug.

## v1 Functional Scope

### Users

- Two pre-seeded users via fixture script: `alice` (has pets) and `bob` (starts empty).
- No self-registration.
- No multi-session control. Login replaces any existing session.

### Authentication flows

1. **Login** — username + password, generic "invalid credentials" error for both wrong-password and unknown-user cases.
2. **Logout** — accessible from the side menu. Protected pages redirect to login after logout.

### Navigation

A persistent side menu with four items:

- My Pets
- Add Pet
- Settings
- Logout

A header on every page shows the logged-in user (e.g. "Logged in as alice").

### Pet management flows

3. **My Pets (list view)** — grid of the current user's pets showing photo (or placeholder), name, species, age. Empty state copy when the user has no pets. Each entry links to the detail page.
4. **Pet detail page** (`/pets/<id>`) — full pet info, with Edit and Delete buttons. Returns 404 when the pet doesn't exist; returns 403/404 when the pet belongs to another user (authorization, not just navigation).
5. **Add Pet form** — five fields:
   - Name (required, text, max 50 chars)
   - Species (required, dropdown: Dog / Cat / Rabbit / Bird / Other)
   - Age (required, number, 0–30 inclusive)
   - Photo (optional, image upload)
   - Notes (optional, free text)

   Server-side validation only in v1. On success, redirect to the new pet's detail page with a flash message.
6. **Edit Pet** — same form as Add Pet, pre-filled with current values.
7. **Delete Pet** — requires confirmation (modal or confirmation page).

### Settings

8. **Change password** — three fields: current password, new password (min 8 chars), confirm new password. Three distinct failure modes plus one success case.

## Out of scope for v1

These are explicitly excluded to keep the demo tight. Several are candidates for a "phase 2" demo about how test suites evolve as features grow.

- Self-registration, email verification, password reset
- Search, filtering, sorting, pagination on the pet list
- Bulk operations
- Multiple sessions per user, session management UI
- Email change, avatar, theme, notifications, account deletion
- Client-side / HTML5 form validation (server-side only in v1)
- Sharing pets between users, public profiles
- Audit logs, activity feeds

## Test surface (the actual deliverable)

Each of the eight flows above must have:

- An **API test** hitting the FastAPI service directly (fast, no browser).
- A **UI test** driving the UI frontend via Selenium (slower, with screenshots).

Cross-cutting tests to include explicitly:

- **Authorization test:** Bob attempts to access Alice's pet by ID via the API. The UI never linked him there, but the API must refuse. This is the headline demo for "why API tests matter even when you have UI tests."
- **Validation boundary tests:** age = -1, 0, 30, 31. Classic boundary-value teaching example.
- **Server-rejects-what-UI-allowed test:** bypass any client-side niceties and confirm the API still validates.
- **File upload test:** image upload via Selenium and via API, with assertions that the file actually lands in `media/`.
- **Session / logout test:** after logout, protected pages redirect.

Test fixtures must reset both the SQLite database and the `media/` directory between tests. The reset itself is a teachable moment about test isolation.

## Documentation deliverables

- This file (`CLAUDE.md`) — scope and constraints.
- A **component diagram** — DB ↔ API ↔ UI ↔ Tests, showing what talks to what.
- A **sequence diagram** for one representative flow (recommended: "user uploads a pet image"), showing the round trip across all components.

Two diagrams total. More is for the developer's benefit, not the audience's.

## Non-goals

This project is **not** trying to be:

- A production-quality application
- A reference implementation of FastAPI best practices
- A security-hardened system (though it should not be embarrassingly insecure)
- A scalable architecture

It is trying to be: **the clearest possible target for explaining automated testing to people who have never written a test.**
