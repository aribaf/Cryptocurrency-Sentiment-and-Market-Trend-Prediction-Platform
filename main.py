from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_experimental_option("detach", True)
options.add_argument(
    r"user-data-dir=C:\Users\ariba\AppData\Local\Google\Chrome\User Data Selenium"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

users = [
    "TTrades_edu", "OmarAgag6", "WeAreM7DR", "ICT_Concepts", "YusufTrader1",
    "seacrestfunded_", "innercirclemorp", "umairs02", "I_Am_The_ICT", "tradingview",
    "May_Nigam_Bybit", "netblocks", "ph0rt0n", "CJ_Reim", "crypticworld7", "CapHillCrypto",
    "BinanceFutures", "Bybit_NFT", "SkyNity_io", "MarekStiller", "BitgetIndia",
    "MaciejTomczyk3", "youngparrotnft", "Bybit_Offiicial", "Dennis_Porter_",
    "jackmallers", "GoingParabolic", "natbrunell", "DaanCrypto", "blumcrypto",
    "0xGenie", "cryptosmerkis", "gleb_crypto", "4UAICrypto"
]

with open("tweets.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["username", "tweet"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for user in users:
        print(f"\n📄 Opening profile: @{user}")
        driver.get(f"https://twitter.com/{user}")
        time.sleep(5)

        collected_texts = set()
        scrolls = 50

        for scroll in range(scrolls):
            tweets = driver.find_elements(By.XPATH, "//article[@role='article']")
            print(f"🔄 Scroll {scroll+1}: {len(tweets)} tweet elements found.")

            for tweet in tweets:
                try:
                    text = tweet.text.replace("\n", " ").strip()
                    if text and text not in collected_texts:
                        collected_texts.add(text)
                        writer.writerow({"username": user, "tweet": text})
                        print(f"{len(collected_texts)}. {text[:100]}...")
                        if len(collected_texts) >= 100:
                            break
                except Exception as e:
                    print(f"⚠ Error reading tweet: {e}")

            if len(collected_texts) >= 100:
                break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)

print(f"\n✅ Done! Collected {len(collected_texts)} tweets from each user. Saved to tweets.csv")
driver.quit()
