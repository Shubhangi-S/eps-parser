import os
import re
import csv
import sys
from bs4 import BeautifulSoup

# Cleans up messy formatting: extra spaces, weird unicode, and (1.23) → -1.23
def normalize(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\(([\d.]+)\)', r'-\1', text)
    return text

# Filters out adjusted/non-GAAP EPS lines
def is_adjusted(text):
    keywords = ['adjusted', 'non-gaap', 'core', 'excluding', 'pro forma']
    return any(k in text.lower() for k in keywords)

# Trustworthy labels — used to allow higher EPS values (e.g., > 20)
def is_trusted_label(text):
    return any(k in text.lower() for k in ['basic', 'gaap', 'diluted'])

# Sanity-check EPS value: filters out extreme or unlikely numbers
def is_valid_eps(value, label):
    try:
        val = float(value)
        if abs(val) > 100:
            return False
        if abs(val) > 20 and not is_trusted_label(label):
            return False
        return True
    except:
        return False

# Searches for EPS using regex in raw text
def extract_eps_from_text(text):
    text = normalize(text)
    patterns = [
        r'GAAP net income per share[^:\d\-]{0,20}(-?\d+\.\d+)',
        r'Basic earnings per share[^:\d\-]{0,20}(-?\d+\.\d+)',
        r'Diluted earnings per share[^:\d\-]{0,20}(-?\d+\.\d+)',
        r'Net income per share[^:\d\-]{0,20}(-?\d+\.\d+)',
        r'Loss per share[^:\d\-]{0,20}(-?\d+\.\d+)',
        r'\bEPS\b[^:\d\-]{0,20}(-?\d+\.\d+)',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            line = match.group(0)
            value = match.group(1)
            if is_adjusted(line):
                continue
            if is_valid_eps(value, line):
                return round(float(value), 2)
    return None

# Checks all <tr> rows in tables for EPS-looking values next to trusted labels
def extract_eps_from_tables(soup):
    for row in soup.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        for i in range(len(cells) - 1):
            label = normalize(cells[i].get_text())
            value = normalize(cells[i + 1].get_text())
            if not label or not value:
                continue
            if is_adjusted(label):
                continue
            if is_trusted_label(label) and is_valid_eps(value, label):
                return round(float(value), 2)
    return None

# Tries text-based first, falls back to table scan if needed
def extract_eps(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text(separator=' ')
            eps = extract_eps_from_text(text)
            return eps if eps is not None else extract_eps_from_tables(soup)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

# Loops over all .html files and extracts EPS
def process_all(input_dir):
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.html')])
    result = []
    for file in files:
        full_path = os.path.join(input_dir, file)
        eps = extract_eps(full_path)
        result.append({'filename': file, 'EPS': eps if eps is not None else ''})
    return result

# Writes output to CSV with headers: filename, EPS
def write_to_csv(rows, output_csv):
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'EPS'])
        writer.writeheader()
        writer.writerows(rows)

# Entry point
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python parser.py <input_dir> <output_csv>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_csv = sys.argv[2]

    rows = process_all(input_dir)
    write_to_csv(rows, output_csv)
