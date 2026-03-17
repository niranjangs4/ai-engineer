def fill_input(page, selector, value):
    page.fill(selector, value, timeout=5000)


def clear_input(page, selector):
    page.locator(selector).fill("")