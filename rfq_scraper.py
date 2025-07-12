
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time
import random

# --- CONFIG --- #
MAX_PAGES = 50  # Adjust based on site limit (can go up to 100 safely)
WAIT_TIME = (2, 5)

options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Anti-bot
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
]
options.add_argument(f"user-agent={random.choice(user_agents)}")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
})

wait = WebDriverWait(driver, 20)
base_url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&page={}"
data = []

def extract_cards():
    cards = driver.find_elements(By.CSS_SELECTOR, "div.brh-rfq-item")
    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "a.brh-rfq-item__subject-link").text.strip()
            buyer_name = card.find_element(By.CSS_SELECTOR, "div.text").text.strip()
            country = card.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__country").text.strip()
            quantity = card.find_element(By.CSS_SELECTOR, "span.brh-rfq-item__quantity-num").text.replace("Quantity Required:", "").strip()

            inquiry_time = "N/A"
            spans = card.find_elements(By.CSS_SELECTOR, "span")
            for span in spans:
                if any(k in span.text.lower() for k in ["ago", "days", "hours", "minutes", "yesterday"]):
                    inquiry_time = span.text.strip()
                    break

            quotes_left = card.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__quote-left").text.replace("Quotes Left", "").strip()
            inquiry_url = card.find_element(By.CSS_SELECTOR, "a.brh-rfq-item__subject-link").get_attribute("href")

            email_confirmed = 'Yes' if "Email Confirmed" in card.text else 'No'
            experienced = 'Yes' if "Experienced buyer" in card.text else 'No'
            typical_replies = 'Yes' if "Typically replies" in card.text else 'No'
            interactive = 'Yes' if "Interactive User" in card.text else 'No'

            data.append({
                "Title": title,
                "Buyer Name": buyer_name,
                "Country": country,
                "Quantity Required": quantity,
                "Inquiry Time": inquiry_time,
                "Quotes Left": quotes_left,
                "Inquiry URL": inquiry_url,
                "Email Confirmed": email_confirmed,
                "Experienced Buyer": experienced,
                "Typical Replies": typical_replies,
                "Interactive User": interactive,
                "Scraping Date": datetime.today().strftime("%d/%m/%Y")
            })

        except Exception as e:
            print(f"⚠️ Card error: {e}")

# ========== MAIN PAGINATION LOOP ========== #
for page in range(1, MAX_PAGES + 1):
    print(f"📄 Scraping page {page}...")
    driver.get(base_url.format(page))
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.brh-rfq-item")))
        time.sleep(random.uniform(*WAIT_TIME))
        extract_cards()
    except Exception as e:
        print(f"⚠️ Failed to load page {page}: {e}")
        break

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("alibaba_rfq_stealth.csv", index=False)
print("💾 Saved as alibaba_rfq_stealth.csv")

driver.quit()









