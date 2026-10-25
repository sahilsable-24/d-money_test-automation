# dMoney Exploration Notes
Source: BRD v1.2 (salmansrabon/dmoney-web-react). [BRD] = not yet verified on the live site.

## 1. Entry points
- UI: https://dmoneyportal.roadtocareer.net  (/login, /register)
- API base URL: ??? (verify in DevTools; lead: https://dmoney.roadtocareer.net)
- Swagger: /api-docs/user and /api-docs/transaction on the API host [BRD]
- Auth headers: `Authorization: Bearer <jwt>` + `X-AUTH-SECRET-KEY` [BRD]

## 2. Auth rules [BRD]
- POST /user/login -> Admin/SYSTEM get JWT directly; others get otpRequired:true
- POST /user/verify-otp -> JWT. OTP: 4 digits, 2 min, one-time, Gmail-only email
- 401 = no/expired token, wrong password, bad OTP; 403 = insufficient role

## 3. Roles and status [BRD]
- Roles: Admin, Agent, Customer, Merchant (+ internal SYSTEM)
- Self-register: Customer/Agent/Merchant only, @gmail.com only, starts "pending"
- Status: pending / active / suspended. Only active accounts can transact (403 otherwise)
- Seeded accounts (password 1234): admin@dmoney.com, agent@dmoney.com,
  customer1@dmoney.com, customer2@dmoney.com, merchant@dmoney.com

## 4. Business rules [BRD]
- Min amount 10 BDT for all transactions
- Deposit (Agent -> Customer): max 10,000; customer wallet cap 10,000; agent commission 2.5%
- Withdraw (Customer/Merchant -> Agent): fee 1% (min 5)
- Send money (Customer -> Customer only): flat 5 fee
- Payment (Customer/Agent -> Merchant): fee 1% (min 5); optional discount code
- Customer outgoing limits: daily 5,000 Tk / 10 txns; monthly 50,000 / 50
- Balance is computed from ledger entries (credits - debits), not stored

## 5. RBAC matrix [BRD] (verify on live site)
| Feature               | Admin | Agent | Customer | Merchant |
|-----------------------|-------|-------|----------|----------|
| Create/update/delete user | Yes | No  | No       | No       |
| View all transactions | Yes   | No    | No       | No       |
| Deposit to SYSTEM     | Yes   | No    | No       | No       |
| Agent cash-in (deposit) | No  | Yes   | No       | No       |
| Stripe cash-in        | No    | No    | Yes      | No       |
| Cash-out (withdraw)   | No    | No    | Yes      | Yes      |
| Send money (P2P)      | No    | No    | Yes      | No       |
| Payment to merchant   | No    | Yes   | Yes      | No       |
| Own statement         | No    | Yes   | Yes      | Yes      |

## 6. Quirks worth testing [BRD]
- "Soft" failures (insufficient balance, wallet cap, duplicates) return HTTP 208, not 4xx
- Customer limit errors return 400
- Passwords are stored/compared in plain text (security finding, not a test target)
- Protected accounts can't be updated/deleted

## 7. Verified on live site (fill in myself)
- [ Yes ] Login as admin@dmoney.com / 1234 works, no OTP
- [ Yes ] Sidebar for Admin matches BRD (User List, Create User, Transaction List, Deposit to SYSTEM)
- [ ] Network tab: API base URL = ?
- [ ] Network tab: X-AUTH-SECRET-KEY header present? value?
- [ ] Customer login with seeded account: what happens at the OTP step?
- [ ] Anything that differs from the BRD:

## 8. Open questions
- OTP strategy for Customer/Agent/Merchant: Gmail API vs local Docker vs other?
- Hosted site vs local instance as the SUT?