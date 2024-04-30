# Central Bank Firm Data Scraper

This Python script allows you to scrape firm data from the Central Bank of Ireland's website. It utilizes Selenium for web scraping, BeautifulSoup for parsing HTML content, Google Translate API for language translation, and JSON for data storage.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup
- googletrans
- Chrome WebDriver

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Alan69/central-bank-firm-scraper.git
```

2. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

3. Download the Chrome WebDriver compatible with your Chrome browser version and place it in the project directory.

## Usage

1. Open a terminal and navigate to the project directory.

2. Run the script:

```bash
python main.py
```

3. The script will scrape firm data from the Central Bank of Ireland's website and store the translated data in a JSON file named `main_extracted_data.json`.

## Configuration

- You can modify the `search_url` variable in `main()` function to change the search criteria for the firms.
- Adjust the `test_num` variable in `main()` function to specify the number of pages to scrape for testing purposes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
