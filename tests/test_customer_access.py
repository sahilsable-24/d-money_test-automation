from playwright.sync_api import Page,expect
import re
import pytest

def test_customer_sees_customer_menu_only(customer_page: Page) -> None:
    customer_page.goto("/profile")

    expect(customer_page.get_by_role("link", name="Send Money")).to_be_visible()
    expect(customer_page.get_by_role("link", name="User List")).to_have_count(0)


@pytest.mark.xfail(
    reason="BUG: a customer can open /admin/users and see the full user list",
    strict=True,
)
def test_customer_cannot_open_admin_page_by_url(customer_page: Page) -> None:
    customer_page.goto("/admin/users")

    expect(customer_page).not_to_have_url(re.compile(r"/admin/users$"))
    expect(customer_page.get_by_role("heading", name="User List")).not_to_be_visible()