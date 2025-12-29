from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import os

# Input target URL
user_url = str(input('[+] Enter Target URL To Scan with (http or https): '))
urls = deque([user_url])
scraped_urls = set()
emails = {}  # email -> set of URLs
written_entries = set()  # to prevent duplicate writing

# Extract original domain
parts = urllib.parse.urlsplit(user_url)
base_domain = parts.netloc

# Create report directory
report_dir = os.path.expanduser('~/Reports/email_scraper')
os.makedirs(report_dir, exist_ok=True)
output_file = os.path.join(report_dir, 'emails.txt')

print(f"[+] Starting scan for {user_url}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}

try:
    while urls:
        url = urls.popleft()
        # Strip fragment identifiers from current URL
        url = urllib.parse.urldefrag(url)[0]
        scraped_urls.add(url)

        print(f'[*] Processing {url}')

        try:
            response = requests.get(url, timeout=10, headers=headers)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            print(f"[-] Failed to retrieve {url}")
            continue

        # Extract emails
        found_emails = re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",
            response.text,
            re.I
        )

        # Log emails immediately, avoid duplicates
        if found_emails:
            print(f"[+] Found {len(found_emails)} emails at {url}:")
        with open(output_file, 'a') as f:
            for email in found_emails:
                email = email.lower()
                emails.setdefault(email, set()).add(url)
                entry = (email, url)
                if entry not in written_entries:
                    written_entries.add(entry)
                    print(f"    {email}")
                    f.write(f"{email} | {url}\n")

        # Parse links from this page and add to queue (same domain only)
        page_parts = urllib.parse.urlsplit(url)
        page_base = f"{page_parts.scheme}://{page_parts.netloc}"
        path = url[:url.rfind('/') + 1] if '/' in page_parts.path else url

        soup = BeautifulSoup(response.text, "lxml")
        for anchor in soup.find_all("a", href=True):
            link = anchor['href']

            if link.startswith('/'):
                link = page_base + link
            elif not link.startswith('http'):
                link = path + link

            # Strip fragment identifiers
            link = urllib.parse.urldefrag(link)[0]

            # Only add links from the same domain
            link_domain = urllib.parse.urlsplit(link).netloc
            if link_domain == base_domain and link not in urls and link not in scraped_urls:
                urls.append(link)

        # Stop if the original URL has been fully processed
        if url == user_url and not any(user_url in u for u in urls):
            break

except KeyboardInterrupt:
    print('[-] Scan interrupted by user!')

print(f"[+] Total unique emails found: {len(emails)}")
print(f"[+] Results saved to {output_file}")

