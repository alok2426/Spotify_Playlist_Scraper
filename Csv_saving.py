import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# Setup Chrome options
options = Options()
# options.binary_location = r"C:\Path\To\Chrome.exe"  # Uncomment if needed

# Initialize driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open the Spotify playlist
PLAYLIST_URL = "https://open.spotify.com/playlist/37i9dQZF1DWUAOn5dYbrDa"
driver.get(PLAYLIST_URL)
time.sleep(7)  # Wait for content to load

# -------------------- Extract Playlist Metadata --------------------
try:
    playlist_name = driver.find_element(By.XPATH, '(//h1[@data-encore-id="text"])[2]').text
except:
    playlist_name = ''

try:
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

# -------------------- Extract Top Tracks --------------------
track_rows = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tracklist-row"]')

tracks_data = []

for i, row in enumerate(track_rows[:20], start=1):
    try:
        title = row.find_element(By.CSS_SELECTOR, 'a[data-testid="internal-track-link"] div').text.strip()
        try:
            album = row.find_element(By.CSS_SELECTOR, 'a[data-testid="internal-album-link"]').text.strip()
        except:
            album = ''
        try:
            date_added = row.find_element(By.XPATH, './/div[last()]/span/time').get_attribute('datetime')
        except:
            try:
                date_added = row.find_element(By.XPATH, './/div[last()]/span').text
            except:
                date_added = ''
        try:
            duration = row.find_element(By.XPATH, './/div[contains(@aria-colindex,"5") or contains(@aria-colindex,"6")]').text.strip()
        except:
            try:
                duration = row.find_elements(By.CSS_SELECTOR, 'div[role="gridcell"]')[-1].text.strip()
            except:
                duration = ''
        try:
            artist_elements = row.find_elements(By.CSS_SELECTOR, 'span[data-encore-id="text"] a[href*="/artist/"]')
            artists = ', '.join([a.text.strip() for a in artist_elements])
        except:
            artists = ''

        tracks_data.append([i, title, album, date_added, duration, artists])
    except:
        tracks_data.append([i, '[Failed to extract track info]', '', '', '', ''])

# -------------------- Save to CSV --------------------
with open('Spotify Featured Playlist Data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write Playlist Metadata
    writer.writerow(['Playlist Name', playlist_name])
    writer.writerow(['Description', description])
    writer.writerow(['Saves/Followers', saves])
    writer.writerow(['Number of Songs', num_songs])
    writer.writerow(['Total Duration', total_duration])
    writer.writerow([])

    # Write Header for Tracks
    writer.writerow(['No', 'Track Name', 'Album', 'Date Added', 'Duration', 'Artists'])

    # Write Track Rows
    writer.writerows(tracks_data)

print("CSV file 'Spotify Featured Playlist Data.csv' created successfully.")

# Close browser
driver.quit()
