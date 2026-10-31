# Bug Reports

## BUG-001: Customer can view the admin User List (broken access control)
- Severity: High (exposes other users' personal data and balances)
- Environment: https://dmoneyportal.roadtocareer.net, 31 Oct 2026
- Steps:
  1. Log in as a Customer (OTP login)
  2. Open /admin/users directly in the address bar
- Expected: access denied or redirect (BRD role matrix: Customer cannot view User List)
- Actual: the User List renders with names, emails, phones, balances, and View/Delete buttons
- Evidence: tests/test_customer_access.py::test_customer_cannot_open_admin_page_by_url (xfail)
- Notes: not yet checked whether the API itself returns the data to a customer token (Phase 9)