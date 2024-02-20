def check_security_headers(response):
    headers = response.headers
    required_headers = ['X-Content-Type-Options', 'X-Frame-Options', 'Content-Security-Policy']
    missing_headers = [header for header in required_headers if header not in headers]
    if missing_headers:
        print("It has security headers file :", missing_headers)