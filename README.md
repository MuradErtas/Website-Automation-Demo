# Website Login Automation

A config-driven web automation framework with multiple automation patterns using Selenium.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Chrome browser and ChromeDriver are installed and in your PATH.

## Usage

Run automations via CLI:
```bash
python main.py --task login
python main.py --task download
python main.py --task form
python main.py --task scrape
python main.py --task dynamic
```

Default task is `login` if `--task` is not specified.

## Available Tasks

- **login** - Login to secure area with credential validation
- **download** - Download file and verify file exists with size > 0
- **form** - Fill form fields and submit with success validation
- **scrape** - Scrape paginated table data to CSV with de-duplication
- **dynamic** - Handle dynamically loaded content with explicit waits and retries

## Structure

- `config.py` - Centralized configuration (URLs, selectors, credentials)
- `main.py` - CLI entry point with task selection
- `automations/` - Automation modules
  - `login.py` - Login automation
  - `download_file.py` - File download automation
  - `fill_form.py` - Form fill automation
  - `scrape_paginated_table.py` - Table scraping automation
  - `dynamic_loading.py` - Dynamic content handling
  - `utils.py` - Shared utility functions
- `artifacts/` - Output directories
  - `screenshots/` - Screenshot captures
  - `html/` - HTML page source on failures
  - `downloads/` - Downloaded files
  - `data/` - Scraped CSV data

## Output

All tasks return JSON with:
- `success`: boolean
- Task-specific fields (URL, file paths, row counts, etc.)
- `timestamp`: ISO timestamp
- `screenshot`: path to screenshot file
- `html`: path to HTML file (on failure only)

