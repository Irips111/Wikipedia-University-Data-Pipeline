# Libraries Used
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd


# Constants
URL = "https://en.wikipedia.org/wiki/List_of_largest_universities"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}


# Helper Functions
def fetch_page(url: str) -> BeautifulSoup:
    """Fetch Wikipedia page and return BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_table(soup: BeautifulSoup):
    """Locate the sortable universities table."""
    return soup.find("table", class_="sortable")


def extract_columns(table):
    """Extract column headers from table."""
    columns = [th.text.strip() for th in table.find_all("th")]
    columns[-1] = "Link"  # Rename last column
    return columns


def extract_row(tr):
    """Extract a single row of university data."""
    cells = tr.find_all("td")
    row = [cell.text.strip() for cell in cells]

    # Ensure row has correct length
    if len(row) < 6:
        row.append("")

    # Extract Wikipedia link
    try:
        link = cells[1].a["href"].lstrip("/")
        row[-1] = f"https://en.wikipedia.org/{link}"
    except (IndexError, TypeError):
        row[-1] = ""

    return row


def extract_data(table):
    """Extract all data rows from table."""
    rows = table.find_all("tr")[1:]  # Skip header row
    return [extract_row(row) for row in rows]


def save_csv(filename, columns, data):
    """Save data to CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(data)


def save_json(filename, data):
    """Save data to JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Main Execution
def main():
    soup = fetch_page(URL)
    table = get_table(soup)

    columns = extract_columns(table)
    data = extract_data(table)

    save_csv("universities.csv", columns, data)
    save_json("universities.json", data)

    df = pd.DataFrame(data, columns=columns)
    print(df.head())


if __name__ == "__main__":
    main()
