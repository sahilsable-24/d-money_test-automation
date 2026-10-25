from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page:Page) -> None:
        self.page = page
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.otp_input = page.get_by_label("OTP")
        self.verify_button = page.get_by_role("button", name="Verify")
        self.error_alert = page.get_by_role("alert")

    def open(self) -> None:
        self.page.goto("/login")

    def submit_credentials(self,email:str,password:str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def submit_otp(self,otp:str) -> None:
        self.otp_input.fill(otp)
        self.verify_button.click()