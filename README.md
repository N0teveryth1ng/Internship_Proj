
---

# 🛠 Alibaba RFQ Scraper (Stealth Mode)

This script scrapes RFQ (Request for Quotation) data from Alibaba using Selenium with stealth mode enabled to bypass bot detection.

### 🚀 Features

* Extracts buyer name, country, quantity, inquiry time, and more
* Uses `selenium-stealth` to avoid being blocked
* Scrapes up to **50 pages** safely
* Outputs data to a clean CSV (`alibaba_rfq_stealth.csv`) ready for Excel

### 🔐 Why Stealth?

Alibaba has strict bot protection. Regular Selenium requests were getting blocked after a few pages.
We added stealth automation to mimic human behavior and ensure uninterrupted data collection.

### ⚠️ Why Only 50 Pages?

Scraping too many pages can raise red flags and get the IP blacklisted.
50 pages offer a solid data sample without crossing risk thresholds.

### 📦 Requirements

* Python 3.8+
* Selenium
* webdriver-manager
* selenium-stealth
* pandas

```bash
pip install selenium webdriver-manager selenium-stealth pandas
```

### ▶️ Run

```bash
python rfq_scraper.py
```

The data will be saved as `alibaba_rfq_stealth.csv`.

---
