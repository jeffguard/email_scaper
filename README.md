This Email Scraper Tool is a Python-based utility designed to extract email addresses from a specified website and its internal pages. It provides an efficient and automated way to collect contact information for research, marketing outreach, or cybersecurity assessments.

Key Features:

Targeted Scanning:

Explicitly scans the user-specified URL and internal pages within the same domain.

Prevents crawling unrelated external domains.

Real-time Logging:

Displays found email addresses on the console immediately as they are discovered.

Writes results to a structured file (emails.txt) for easy reference.

Duplicate Prevention:

Avoids writing duplicate email + URL combinations to the output file.

Ensures a clean and organized dataset of unique email addresses.

Fragment Handling:

Ignores URL fragments (#...) to prevent infinite loops on pages with repeated fragment identifiers.

Robust and Reliable:

Handles connection errors, timeouts, and invalid URLs gracefully.

Supports modern web servers with a configurable User-Agent header.

Easy-to-Use Output:

Results are stored in ~/Reports/email_scraper/emails.txt.

Each entry is formatted as email | source URL for traceability.

Use Cases:

Collect contact emails for business or networking purposes.

Conduct cybersecurity reconnaissance or testing.

Extract data for research or outreach campaigns.

Requirements:

Python 3.x

Packages: requests, beautifulsoup4, lxml
