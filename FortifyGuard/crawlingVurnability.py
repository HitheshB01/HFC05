import requests
from bs4 import BeautifulSoup
import numpy as np

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