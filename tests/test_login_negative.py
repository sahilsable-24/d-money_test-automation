import re 

import pytest
from playwright.sync_api import Page, expect

from config.settings import ADMIN_EMAIL
from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "email, password",
    [
        (ADMIN_EMAIL, "wrong_password"),
        ("nobody@dmoney.com", "1234"),
        ("",""),
    ],
    ids=["wrong-password", "unknown-user", "empty-fields"],
)

def test_login_with_invalid_credentials_is_rejected(
    page:Page, login_page: LoginPage, email: str, password: str
) -> None:
    login_page.submit_credentials(email,password)

    expect(page).not_to_have_url(re.compile(r"/profile$"))
    expect(page).to_have_url(re.compile(r"/login$"))