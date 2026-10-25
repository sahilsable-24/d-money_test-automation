import os 
from playwright.sync_api import Page,expect
from utils.gmail_otp import get_latest_otp, mark_old_otps_as_read
import re 
from pages.login_page import LoginPage
from config.settings import CUSTOMER_EMAIL,CUSTOMER_PASSWORD


def test_customer_can_log_in_with_otp(page:Page, login_page:LoginPage) -> None:
    mark_old_otps_as_read(CUSTOMER_EMAIL)
    #step-1 : enter email and password
    login_page.submit_credentials(CUSTOMER_EMAIL,CUSTOMER_PASSWORD)

    #step-2: the site now asks for otp. fetch it from gmail
    otp = get_latest_otp(CUSTOMER_EMAIL)
    login_page.submit_otp(otp)

    #step-3: check we landed in the customer area, not admin area
    expect(page).to_have_url(re.compile(r"/profile$"))
    expect(page.get_by_role("link", name="Send Money")).to_be_visible()
    expect(page.get_by_role("link", name="User List")).to_have_count(0)


def test_customer_login_rejects_wrong_otp(page: Page, login_page: LoginPage) -> None:
    mark_old_otps_as_read(CUSTOMER_EMAIL)

    login_page.submit_credentials(CUSTOMER_EMAIL,CUSTOMER_PASSWORD)

    login_page.submit_otp(otp="0000")

    expect(login_page.error_alert).to_be_visible()
    expect(page).not_to_have_url(re.compile(r"/profile$"))


