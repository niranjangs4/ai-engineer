def open_url(page, url):
    page.goto(url,timeout=10000)

def go_back(page):
    page.go_back()

def refresh(page):
    page.reload()