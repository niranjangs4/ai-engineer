def assert_visible(page, selector):

    element = page.locator(selector)

    if element.count() == 0:
        raise Exception("Element not found")

    if not element.first.is_visible(timeout=5000):
        raise Exception("Element not visible")

    return True