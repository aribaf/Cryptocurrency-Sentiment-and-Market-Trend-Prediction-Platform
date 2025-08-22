from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from datetime import datetime

# Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_experimental_option("detach", True)
options.add_argument(
    r"user-data-dir=C:\Users\ariba\AppData\Local\Google\Chrome\User Data Selenium"
)

# Start driver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# Open #btc search page
print("🔍 Opening Twitter search for #btc...")
driver.get("https://twitter.com/search?q=%23btc&src=typed_query&f=live")
time.sleep(5)

# CSV setup
with open("btc_tweets.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["username", "tweet", "date", "time"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    collected_texts = set()
    scrolls = 0
    target_count = 1000  # number of tweets to collect

    while len(collected_texts) < target_count:
        tweets = driver.find_elements(By.XPATH, "//article[@role='article']")
        print(f"🔄 Scroll {scrolls+1}: {len(tweets)} tweet elements found.")

        for tweet in tweets:
            try:
                text = tweet.text.replace("\n", " ").strip()

                # Basic spam filter: skip empty, very short, or repeated link-only tweets
                if (
                    not text
                    or text in collected_texts
                    or len(text) < 10
                    or text.lower().startswith("http")
                ):
                    continue

                # Extract username
                try:
                    username_elem = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']//span")
                    username = username_elem.text.strip()
                except:
                    username = "Unknown"

                # Extract timestamp
                try:
                    time_elem = tweet.find_element(By.XPATH, ".//time")
                    tweet_datetime = datetime.fromisoformat(time_elem.get_attribute("datetime").replace("Z", "+00:00"))
                    tweet_date = tweet_datetime.strftime("%Y-%m-%d")
                    tweet_time = tweet_datetime.strftime("%H:%M:%S")
                except:
                    tweet_date = "Unknown"
                    tweet_time = "Unknown"

                collected_texts.add(text)

                writer.writerow({
                    "username": username,
                    "tweet": text,
                    "date": tweet_date,
                    "time": tweet_time
                })
                print(f"{len(collected_texts)}. {username} [{tweet_date} {tweet_time}]: {text[:80]}...")

                if len(collected_texts) >= target_count:
                    break

            except Exception as e:
                print(f"⚠ Error reading tweet: {e}")

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scrolls += 1
        time.sleep(2.5)

print(f"\n✅ Done! Collected {len(collected_texts)} tweets containing #btc. Saved to btc_tweets.csv")
driver.quit()
