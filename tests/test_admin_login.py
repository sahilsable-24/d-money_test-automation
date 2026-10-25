from playwright.sync_api import Page, expect
import re
from pages.login_page import LoginPage
from config.settings import ADMIN_EMAIL,ADMIN_PASSWORD

def test_admin_can_log_in(page:Page, login_page: LoginPage) -> None:
    login_page.submit_credentials(ADMIN_EMAIL,ADMIN_PASSWORD)

    expect(page).to_have_url(re.compile(r"/profile$"))
    expect(page.get_by_role("link", name="User List")).to_be_visible()