from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
# Setup Chrome options (modify path only if needed to use custom browser binary)
options = Options()
# options.binary_location = r"C:\Users\hp\Downloads\chrome.exe"  # Uncomment if using custom Chrome binary

# Initialize the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the Spotify playlist
PLAYLIST_URL = "https://open.spotify.com/playlist/37i9dQZF1DWUAOn5dYbrDa"
driver.get(PLAYLIST_URL)

time.sleep(7)  # Wait for the page and playlist to load
# -------------------- Extract playlist metadata --------------------

try:
    # playlist_name =   driver.find_element(By.CSS_SELECTOR, 'h1[data-encore-id="text"]').text
    playlist_name = driver.find_element(By.XPATH,'(//h1[@data-encore-id="text"])[2]').text
except:
    playlist_name = ''

try:
    # description = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="entityDescription"]').text
    
    description = driver.find_element(By.CSS_SELECTOR, 'div.xgmjVLxjqfcXK5BV_XyN.fUYMR7LuRXv0KJWFvRZA').text
    
except:
    description = ''

saves = ''
num_songs = ''
total_duration = ''

try:
    spans = driver.find_elements(
        By.CSS_SELECTOR,
        'span[data-encore-id="text"].encore-text-body-small.encore-internal-color-text-subdued'
    )
    print(spans)
    for span in spans:
        text = span.text.strip().lower()
        match = re.search(r'(\d+)\s*hr', text)
        if 'saves' in text:
            saves = span.text.strip()
        elif 'songs' in text and 'about' not in text:
            num_songs = span.text.strip()
        elif match:
            if 'songs' not in text:
                total_duration = span.text.strip()
except:
    pass

# -------------------- Print playlist metadata --------------------

print(f"\nPLAYLIST: {playlist_name}")
print(f"Description: {description}")
print(f"Saves/Followers: {saves}")
print(f"Number of Songs: {num_songs}")
print(f"Total Duration: {total_duration}")
# Grab track rows
track_rows = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tracklist-row"]')

print("\nTop Tracks:\n")
print("No | Track Name | Album | Date Added | Duration | Artists")

for i, row in enumerate(track_rows[:20], start=1):
    try:
        # Track Name
        title = row.find_element(By.CSS_SELECTOR, 'a[data-testid="internal-track-link"] div').text.strip()

        # Album Name
        try:
            album = row.find_element(By.CSS_SELECTOR, 'a[data-testid="internal-album-link"]').text.strip()
        except:
            album = ''

        # Date Added
        try:
            date_added = row.find_element(By.XPATH, './/div[last()]/span/time').get_attribute('datetime')
        except:
            try:
                date_added = row.find_element(By.XPATH, './/div[last()]/span').text
            except:
                date_added = ''

        # Duration
        try:
            duration = row.find_element(By.XPATH, './/div[contains(@aria-colindex,"5") or contains(@aria-colindex,"6")]').text.strip()
        except:
            try:
                duration = row.find_elements(By.CSS_SELECTOR, 'div[role="gridcell"]')[-1].text.strip()
            except:
                duration = ''

        # Artists
        try:
            artist_elements = row.find_elements(By.CSS_SELECTOR, 'span[data-encore-id="text"] a[href*="/artist/"]')
            artists = ', '.join([a.text.strip() for a in artist_elements])
        except:
            artists = ''

        print(f"{i} | {title} | {album} | {date_added} | {duration} | {artists}")

    except Exception as e:
        print(f"{i}. [Failed to extract track info]")

# Close browser
driver.quit()