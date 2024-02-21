import requests
from bs4 import BeautifulSoup
from sklearn.ensemble import IsolationForest
import numpy as np
import openai

print('✴.·´¯·.·★  𝓕𝓞𝓡𝓣𝓘𝓕𝓨𝓖𝓤𝓐𝓡𝓓.𝓐𝓘  ★·.·¯´·.✴')


openai.api_key = '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'


def prioritize_threats_with_openai(text_data):
    try:

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text_data,
            max_tokens=50
        )
        threat_likelihood = response.choices[0].text
        print("Threat likelihood from OpenAI:", threat_likelihood)
    except Exception as e:
        print("Successful in prioritizing threats with OpenAI: ")
        print(e)


#
def detect_anomalies(data):
    try:
        # Create Isolation Forest model
        clf = IsolationForest(contamination=0.1)
        clf.fit(data.reshape(-1, 1))

        anomalies = clf.predict(data.reshape(-1, 1))
        return anomalies
    except Exception as e:
        print("Error in detecting anomalies:")
        print(e)
        return None


def crawl_and_scan(url, recursion_level=1):

    visited_urls = {}


    def crawl(url, depth):
        if depth > recursion_level:
            return
        if url in visited_urls:
            return
        visited_urls[url] = True

        try:
            response = requests.get(url)
            if response.status_code == 200:

                soup = BeautifulSoup(response.text, 'html.parser')


                check_security_headers(response)


                check_xss_vulnerabilities(soup, url)

                check_csrf_vulnerabilities(soup, url)


                check_sql_injection_vulnerabilities(response.text, url)


                check_idor_vulnerabilities(response.text, url)

                text_data = soup.get_text()

                prioritize_threats_with_openai(text_data)


                text_data_lengths = np.array([len(text_data)])
                anomalies = detect_anomalies(text_data_lengths)
                if -1 in anomalies:
                    print("Anomalies detected in text data")

                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    if href.startswith('/') or href.startswith(url):
                        new_url = href if href.startswith(url) else url + href
                        crawl(new_url, depth + 1)
            else:
                print("Failed to fetch:", url)
        except Exception as e:
            print("Error fetching:", url)
            print(e)


    crawl(url, 1)


def check_security_headers(response):
    headers = response.headers
    required_headers = ['X-Content-Type-Options', 'X-Frame-Options', 'Content-Security-Policy']
    missing_headers = [header for header in required_headers if header not in headers]
    if missing_headers:
        print("It has security headers file :", missing_headers)


def check_xss_vulnerabilities(soup, url):

    script_tags = soup.find_all('script')
    for script_tag in script_tags:

        if 'document' in script_tag.text and 'getElementById' in script_tag.text:
            print("Potential XSS vulnerability found at:", url)


def check_csrf_vulnerabilities(soup, url):
    forms = soup.find_all('form')
    for form in forms:
        if not form.find('input', {'name': 'csrf_token'}):
            print("CSRF vulnerability found in form at:", url)


def check_sql_injection_vulnerabilities(content, url):
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE']
    for keyword in sql_keywords:
        if keyword in content:
            print("SQL injection vulnerability found at:", url)


def check_idor_vulnerabilities(content, url):

    if '/admin/' in url or 'id=' in url:
        print("Insecure Direct Object Reference found at:", url)


if _name_ == "_main_":
    try:
        website_url = input("Enter the website URL: ")
        recursion_level = int(input("Recursion Level (Between 1-3 | Default = 1): ") or 1)


        crawl_and_scan(website_url,recursion_level)
    except Exception as e:
        print("An error occurred:")
        print(e)