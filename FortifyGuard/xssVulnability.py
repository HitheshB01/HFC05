def check_xss_vulnerabilities(soup, url):
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        if 'document' in script_tag.text and 'getElementById' in script_tag.text:
            print("Potential XSS vulnerability found at:", url)