# OMP Custom Distribution Strategy — High-Level Architecture (Draft)

## 1. Business & Legal Model

- Base software: Open Monograph Press (OMP), licensed under GPLv3.
- Legal facts to respect:
  - Using and modifying OMP internally does NOT require publishing source code, as long as the modified version is not conveyed/distributed outside my organization.
  - Once a modified version is installed on a customer server, it is considered “conveyed/distributed” and the recipient has GPL rights, including redistribution.
- Business goal:
  - Keep maximum control over the customized OMP version.
  - Minimize the risk and incentive for customers to redistribute the customized version.

### 1.1. Service Model Decision

- Preferred model:
  - SaaS / Hosted model when possible (no code leaves my infrastructure).
- When on‑prem deployment is mandatory:
  - Accept that I cannot fully prevent redistribution.
  - Focus on:
    - Minimizing exposed intellectual property.
    - Maximizing dependence on my services (support, updates, external APIs).

## 2. Repository Strategy (Private Git, Self-Hosted)

- Setup:
  - Self‑hosted Git server (e.g., Gitea or GitLab CE).
- Repositories:
  - `omp-gpl-core`
    - Fork of official OMP.
    - Kept in sync with upstream.
    - All modifications clearly marked as GPL code.
  - `omp-custom-business`
    - Proprietary scripts, deployment tooling, integration logic, and external services.
    - Designed to interact with OMP via HTTP/API where possible to keep coupling low.

- Access policy:
  - Only my team has access.
  - No direct Git access is ever granted to customer servers.

## 3. Localization Handling Strategy

- Source translation files (`.po`):
  - Stored ONLY in my private dev environment and private Git.
  - Never shipped inside Docker images.
  - Never copied to customer servers.

- Compiled translation files (`.mo`):
  - Generated locally using `msgfmt` in my environment.
  - Only `.mo` files are copied into the Docker image layers.
  - Acknowledge:
    - Text content can still be read from `.mo`, but the richer `.po` metadata (comments, history, etc.) is not exposed.

## 4. Docker & Deployment Strategy

### 4.1. Image Build (only on my side)

- Build custom OMP image locally:
  - Base: `pkpofficial/omp:<matching version>`
  - Layers:
    - Copy my compiled `.mo` files into `/var/www/html/locale/fa_IR` and `/var/www/html/lib/pkp/locale/fa_IR`.
    - Apply any PHP/theme customizations required.
  - Tag example: `myorg/omp-custom:<customer-code>-<version>`

- Never run `docker build` on customer servers.
- Never give customers direct access to my Dockerfile or build scripts.

### 4.2. Image Transfer to Customer

- Use `docker save` / `docker load` flow:
  - On my side:
    - `docker save myorg/omp-custom:<tag> -o omp-custom-<tag>.tar`
  - Transfer `*.tar` via secure channel (SCP, SFTP, encrypted storage).
  - On customer server:
    - `docker load -i omp-custom-<tag>.tar`
    - `docker compose up -d` using a pre-prepared `docker-compose.prod.yml`.

- Customer never pulls from Docker Hub or my registry.
- Customer never needs Git access to my repositories.

## 5. Application Architecture to Reduce IP Exposure

- Design principles:
  - Keep the most business-specific logic in:
    - External microservices hosted by me, or
    - Modules that are not strictly tied to OMP’s GPL code (where legally defensible).
  - OMP on customer side acts more as:
    - Presentation layer.
    - Workflow engine.
    - Integrator with my external services.

- Examples (to refine later):
  - Recommendations, pricing, or analytics logic implemented as separate API services.
  - Customer’s OMP instance calls these services over HTTPS.
  - If the customer clones/copies the OMP instance, they lose access to these external services unless they have a valid contract with me.

## 6. Contractual Layer (Non-technical)

- Service agreement (not drafted here, but principles):
  - Clear separation:
    - GPL obligations for OMP code (customer retains GPL freedoms).
    - Commercial terms for:
      - Support.
      - Upgrades.
      - Access to external services / APIs.
  - Clause examples (informal description for now):
    - Support and updates are provided only to registered, officially deployed instances.
    - If the customer redistributes the software, those redistributed instances are not covered by my support or update commitments.
  - Goal:
    - Do NOT try to override GPL.
    - Use economics and support terms to make unauthorized redistribution unattractive.

## 7. Next Steps (for future automation)

- [ ] Define the exact repository structure in detail.
- [ ] Define the Dockerfile template for `myorg/omp-custom`.
- [ ] Define a standardized `docker-compose.prod.yml` for customer servers.
- [ ] Define a build-and-package script that:
      - Builds the image.
      - Runs tests.
      - Produces a versioned `*.tar` bundle.
- [ ] Define a minimal “installation guide” for customer-side ops, based on `docker load` + `docker compose up`.