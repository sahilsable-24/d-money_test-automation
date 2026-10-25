from playwright.sync_api import Page,expect

def test_customer_sees_customer_menu_only(customer_page: Page) -> None:
    customer_page.goto("/profile")

    expect(customer_page.get_by_role("link", name="Send Money")).to_be_visible()
    expect(customer_page.get_by_role("link", name="User List")).to_have_count(0)