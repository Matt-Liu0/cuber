# CUBER – Colgate University Ride-Sharing & Campus Errand App
> **Helping car-less students get rides & essentials, while enabling car owners to earn on campus.**
---
## ■ Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [System Architecture](#system-architecture)
4. [Repository Structure](#repository-structure)
5. [Local Development](#local-development)
6. [Environment Variables](#environment-variables)
7. [Testing & Quality](#testing--quality)
8. [CI / CD](#ci--cd)
9. [Contributing](#contributing)
10. [License](#license)
---
## Project Overview
CUBER is a campus-focused **ride-sharing and on-demand delivery** platform designed for Colgate
University. It connects:
* **Passengers** who need a ride to off-campus locations or delivery of food / supplies.
* **Student Drivers** who own cars and want to earn money.
The app provides secure Colgate SSO login, real-time order matching, Stripe-based payments, and
rating / dispute resolution.
---
## Tech Stack
| Layer | Technology | Why We Chose It |
|-------|------------|-----------------|
| **Mobile** | **Swift 5.9 + SwiftUI + Combine (iOS 16+)** | Native performance, modern declarative
UI, seamless Apple Pay integration. |
| **Backend API** | **FastAPI ( Python 3.12 )** | Type-safe, async, auto-generated OpenAPI docs,
great performance. |
| **Database** | **Supabase-managed Postgres 15 + PostGIS 3.4** | Strong consistency, geo-queries
(`ST_DWithin`), row-level security, instant REST & Realtime APIs. |
| **Auth** | **Colgate Secure Sign-In (Shibboleth SSO) + JWT** | Single source of truth for student
identity; stateless tokens for mobile. |
| **Payments** | **Stripe Connect + Stripe Issuing** | Handles KYC, holds pre-auth funds, splits
payouts to drivers & platform. |
| **Realtime / Notifications** | **Supabase Realtime (PG → websocket)**, **FCM / APNS** | Live
order list for drivers; push notifications to both parties. |
| **Cloud / IaC** | **Docker Compose (local)**, **Render.com / Fly.io** (prod), **Terraform**
(optional) | Simple developer onboarding, repeatable envs. |
| **Maps & Geolocation** | **Apple MapKit** (iOS), **PostGIS** (server) | Accurate campus mapping +
efficient distance filtering. |
| **Testing** | **XCTest** (mobile), **PyTest** (backend) | Unit & integration tests in CI. |
| **Lint / Format** | **SwiftLint**, **Black + Ruff** | Keep code style consistent. |
| **CI / CD** | **GitHub Actions**, **Fastlane** (iOS build) | Automated checks, TestFlight, backend
deploy. |
---
## System Architecture
```
■■■■■■■■■■■■■■■■ HTTPS / JWT ■■■■■■■■■■■■■■■■
■ iOS App ■ ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ ■ FastAPI ■
■ SwiftUI ■ ■ API ■
■■■■■■■■■■■■■■■■ ■■■■■■■■■■■■■■■■
▲ WebSocket Realtime updates ■ Stripe ■
■ ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ Webhooks ■
APNS / ■ ■■■■■■■■■■■■■■■■
FCM ■ Supabase Edge Functions / RLS ■ Postgres ■
▼ ■ + PostGIS ■
■■■■■■■■■■■■■■■■ ■■■■■■■■■■■■■■■■
■ Drivers ■ same mobile codebase
■■■■■■■■■■■■■■■■
```
* **Edge Functions** (Supabase) handle Stripe webhook → DB writes.
* **Row-Level Security** restricts each `order` record to rider + assigned driver.
* **Realtime channel** pushes `orders` table changes to subscribed drivers.
---
## Repository Structure
```
cuber/
■■■ mobile/ # iOS SwiftUI project
■ ■■■ Core/ # Networking, Auth, Extensions
■ ■■■ Features/ # Auth/, Orders/, Driver/, Payment/
■
■■■ backend/
■ ■■■ app/
■ ■ ■■■ api/v1/ # Routers (auth.py, orders.py ...)
■ ■ ■■■ services/ # Business logic
■ ■ ■■■ models/ # SQLModel ORM entities
■ ■ ■■■ core/ # config.py, security.py
■ ■■■ alembic/ # DB migrations
■
■■■ infra/ # Docker, Terraform
■■■ docs/ # Architecture diagrams, ADRs
■■■ .github/workflows/ # Lint / Test / Deploy pipelines
```
---
## Local Development
### Prerequisites
- **Xcode 15+** (Swift 5.9)
- **Python 3.12** + **Poetry** (or `pipx`)
- **Docker 24+**
- **Stripe CLI** (for webhook testing)
### 1. Clone & bootstrap
```bash
$ git clone https://github.com/colgate-coders/cuber.git
$ cd cuber
$ make bootstrap # sets up Python venv & pre-commit hooks
$ make dev-up # docker-compose: postgres, pgadmin, redis
```
### 2. Run the backend
```bash
$ cd backend
$ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Test: <http://localhost:8000/docs>
### 3. Run the iOS app
Open **`mobile/Cuber.xcodeproj`**, select *iPhone 15 Pro* simulator, press ■■.
### 4. Seed data (optional)
```bash
$ python backend/scripts/seed_demo.py
```
---
## Environment Variables
Create `.env` at repo root (sample below):
```dotenv
# Backend
API_URL=http://localhost:8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cuber
SECRET_KEY=super-secret
COLGATE_SSO_METADATA_URL=https://sso.colgate.edu/metadata
STRIPE_SECRET=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
# iOS (xcconfig)
BACKEND_BASE_URL=http://10.0.2.2:8000 # Simulator → host
STRIPE_PUBLISHABLE_KEY=pk_test_...
```
---
## Testing & Quality
| Layer | Command |
|-----------|-----------------------------|
| Backend | `make test` (pytest + cov) |
| Mobile | `■U` in Xcode (XCTest) |
| Lint | `make lint` (ruff, swiftlint)|
---
## CI / CD
* **GitHub Actions**
* `backend.yml` – lint → pytest → Docker image → Render deployment.
* `ios.yml` – build-and-test → sign → upload to TestFlight via Fastlane.
* Secrets managed through **GitHub OIDC** → cloud providers.
---
## Contributing
1. Fork → create feature branch → commit with Conventional Commits.
2. Ensure `make lint test` passes.
3. Open PR, fill template, request review.
We follow the [Colgate Coders Style Guide](docs/STYLE_GUIDE.md).
---
## License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.