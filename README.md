````markdown
# EPS Parser – Take-Home

## Overview

This script extracts Earnings Per Share (EPS) values from a set of SEC 8-K HTML filings. It looks for GAAP-based EPS values (Basic, Net, or Diluted) and saves them in a CSV file.


## Files

- `parser.py` – main script  
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
python3 parser.py /path/to/Training_Filings output.csv
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

## Why some EPS values were not extracted

Not every EPS value gets picked up by the script, and that’s expected. This is a quick summary of why:

1. **HTML formats vary a lot**  
   Every filing looks different. Some use clean tables, others have messy inline text or custom layouts. The script handles common patterns, but it’s not built to cover every possible format.

2. **Non-GAAP and adjusted EPS are skipped**  
   If the label includes words like “adjusted”, “non-GAAP”, “core”, or “excluding”, it’s skipped on purpose. The goal is to only extract clear GAAP-compliant values like “Basic” or “Diluted EPS”.

3. **EPS hidden in footnotes or narratives**  
   Some filings mention EPS only once, deep inside a paragraph or a footnote. The script doesn’t dig that deep to avoid pulling noisy or irrelevant text.

4. **Value filters**  
   The script ignores values above 100, or above 20 if the label isn’t something like “GAAP” or “Basic”. This helps avoid pulling totals or misread numbers.

In short — this script is written to be cautious and only pull clearly labeled, reliable EPS values. It’s okay if a few edge cases are missed. That’s by design.

```
