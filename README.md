# Spotify Featured Playlist Data Scraper

This project contains Python scripts to scrape metadata and track details from a Spotify playlist using **Selenium WebDriver**.  
It extracts playlist information (name, description, followers, number of songs, total duration) and details of the top 20 tracks, then saves the data to a CSV file.

---

## 📂 Project Structure
- **Spotify Featured Playlist Data.py**  
  - Extracts and prints playlist metadata and top track details to the console.

- **Csv_saving.py**  
  - Extracts the same information but saves it to a CSV file (`Spotify Featured Playlist Data.csv`).

- **spotify_playlist.csv**  
  - Sample CSV file containing extracted playlist data.

---

## 🔧 Requirements
Make sure you have the following installed:
- Python 3.7+
- Google Chrome browser
- [ChromeDriver](https://chromedriver.chromium.org/) (automatically managed by `webdriver_manager`)

Install dependencies:
```bash
pip install selenium webdriver-manager
