def click(page, selector):

    locator = page.locator(selector)

    count = locator.count()

    if count == 0:
        raise Exception(f"Element not found: {selector}")

    if count > 1:
        print(f"Multiple elements found for {selector}, clicking first match")

    locator.first.click(timeout=5000)


def hover(page, selector):
    locator = page.locator(selector)

    count = locator.count()

    if count == 0:
        raise Exception(f"Element not found: {selector}")

    if count > 1:
        print(f"Multiple elements found for {selector}, clicking first match")

    locator.first.hover(timeout=5000)