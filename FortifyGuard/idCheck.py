
def check_idor_vulnerabilities(content, url):
    if '/admin/' in url or 'id=' in url:
        print("Insecure Direct Object Reference found at:", url)