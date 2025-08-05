````markdown
# EPS Parser – Trexquant Take-Home

## Overview

This script extracts Earnings Per Share (EPS) values from a set of SEC 8-K HTML filings. It looks for GAAP-based EPS values (Basic, Net, or Diluted) and saves them in a CSV file.


## Files

- `parser_1.py` – main script  
- `output.csv` – extracted EPS values  
- `README.md` – instructions and notes  


## How to Run

### Requirements
- Python 3.x
- BeautifulSoup

Install the required package:
```bash
pip install beautifulsoup4
````

### Run the script

```bash
python3 parser_1.py /path/to/Training_Filings output.csv
```

Replace `/path/to/Training_Filings` with the folder containing the 50 HTML files.



## How It Works

* Opens and parses each `.html` file using BeautifulSoup
* Extracts EPS values using two methods:

  * Matches phrases in text like:

    * "Basic earnings per share: \$1.23"
    * "GAAP net income per share"
  * Looks for labels in tables like "Basic", "GAAP", or "Net income"
* Ignores EPS values marked as "Adjusted", "Non-GAAP", or similar
* Filters out EPS values that are too high unless clearly labeled as GAAP or Basic


## Limitations

* Some adjusted EPS values may be included if not clearly labeled
* Some GAAP EPS may be missed due to inconsistent formatting
* EPS values above 20 are skipped unless the label includes GAAP, Basic, or Diluted


## Output Example

```csv
filename,EPS
0000008947-20-000044.html,2.71
0000046080-20-000050.html,
0000314808-20-000062.html,
...
```

## Notes

* One EPS value is extracted per file
* Values in brackets (e.g., `(0.48)`) are treated as negative
* EPS values are rounded to 2 decimal places
* All 50 files were processed

```
