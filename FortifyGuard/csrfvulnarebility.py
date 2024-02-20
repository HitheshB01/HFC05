def check_csrf_vulnerabilities(soup, url):
    forms = soup.find_all('form')
    for form in forms:
        if not form.find('input', {'name': 'csrf_token'}):
            print("CSRF vulnerability found in form at:", url)