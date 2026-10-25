# Test Strategy

SUT: hosted dMoney portal. Requirements come from BRD v1.2.
Verified on live site: admin login (no OTP), customer login (OTP arrives by email).
Not yet verified: API base URL, secret-key header, plus-addressed emails.

## Principles
- Automate what protects money, permissions, and core entry points.
- Use the API for setup and verification, the UI for user-facing behavior.
- Every test creates its own users. No shared accounts, no test-order dependencies.

## Smoke suite (run on every push, target < 3 min)
1. Admin can log in and sees the admin menu (UI)
2. Customer can log in with OTP (UI)
3. Admin can create a user via API
4. One deposit works end to end and the balance updates (API)

## Regression: API layer
| Candidate | Type | Why |
|---|---|---|
| Ledger and balance correctness after each transaction type | Regression | Wrong debits/credits/fees are the worst fintech bug |
| Role-based transaction authorization (e.g. Customer calling admin endpoints) | RBAC / Negative | The API, not the UI, must enforce permissions |
| No token / bad token returns 401 | Auth / Negative | Cheapest security check |
| Min amount 10 and deposit max 10,000 (9, 10, 10,000, 10,001) | Boundary | Rules are numeric and precise |
| Fees and commissions (including the 5 BDT minimum fee) | Boundary | Percentage logic with a floor |
| Insufficient balance and wallet cap (assert real status codes: 208, not 4xx) | Negative | Failed transactions must not change balances |
| Pending / suspended accounts cannot transact | Negative | Status gates all money movement |
| Own statement shows only own transactions | RBAC | Privacy of transaction history |
| Daily customer limit (fresh customer, small amounts) | Boundary | Cumulative limits are easy to break |

## Regression: UI layer
| Candidate | Why |
|---|---|
| Invalid OTP shows an error, wrong password shows an error | Login error handling |
| Role-based menus (Customer does not see admin pages; direct URL access is blocked) | UI-side RBAC |
| End-to-end: register, admin activates, agent deposits, customer sees balance | The core business flow. Setup via API where possible, key steps via UI |

## OTP approach
Option A. A dedicated test Gmail inbox read over IMAP; credentials in `.env`.
- OTP gates all non-admin API tokens, so the OTP step must be minimal: log in once
  per role per session and reuse the token (fixture, later phase).
- Test users need @gmail.com addresses. Gmail plus-addressing
  (name+cust1@gmail.com) gives unique emails that all land in one inbox.
  Verify the portal accepts "+" in emails before relying on it.

## Not automating (yet)
- Stripe cash-in: external payment system, needs a controlled environment.
- Photo upload: low financial risk, check manually.
- Discount-code combinations: until core payment rules are covered.
- Monthly limit (50 transactions): too slow and heavy on a shared instance.
- OTP expiry (2 min): slow; consider later with a patient test or skip.

## Test data
- Admin (seeded, no OTP) creates users and activates them via API.
- SYSTEM funds agents, agents fund customers, so each test builds its own money.
- Unique data per run (timestamp or counter in names/emails/phones).
- Risks: daily limits reset at midnight UTC, so avoid running limit tests near it.
  Limits are per customer, so a fresh customer starts at zero.

## Top three priorities
Ledger/balance correctness, role-based authorization, amount boundaries.