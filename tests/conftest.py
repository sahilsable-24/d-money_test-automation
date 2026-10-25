import re
from collections.abc import Generator

import pytest
from playwright.sync_api import Page, Browser ,expect

from pages.login_page import LoginPage
from utils.gmail_otp import get_latest_otp, mark_old_otps_as_read

from config.settings import CUSTOMER_EMAIL,CUSTOMER_PASSWORD



@pytest.fixture
def login_page(page:Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.open()
    return login_page



@pytest.fixture(scope="session")
def customer_storage_state(browser:Browser, base_url: str, tmp_path_factory) -> str:
    email = CUSTOMER_EMAIL
    password= CUSTOMER_PASSWORD

    mark_old_otps_as_read(email)

    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.submit_credentials(email,password)
    login_page.submit_otp(get_latest_otp(email))

    expect(page).to_have_url(re.compile(r"/profile$"))

    state_file = tmp_path_factory.mktemp("auth") / "customer.json"
    context.storage_state(path=state_file)
    context.close()
    return str(state_file)


@pytest.fixture
def customer_page(browser:Browser, base_url:str, customer_storage_state:str) -> Generator[Page,None,None]:

    context = browser.new_context(base_url=base_url, storage_state=customer_storage_state)
    yield context.new_page()
    context.close()


