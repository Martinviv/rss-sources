import os
import json
import csv
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

"""
Check all RSS/Atom feeds contained in JSON files.
"""


def test_rss_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True
        )

        if response.status_code != 200:
            return f"HTTP {response.status_code}"

        try:
            root = ET.fromstring(response.content)

            tag = root.tag.lower()

            if (
                tag.endswith("rss")
                or tag.endswith("feed")
                or tag.endswith("rdf")
                or tag.endswith("rdf:rdf")
            ):
                return "Success"

            return f"Unknown feed type ({root.tag})"

        except ET.ParseError:
            return "Invalid XML"

    except requests.exceptions.Timeout:
        return "Timeout"

    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"


def extract_urls_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    feeds = data.get("feeds", [])

    urls = []

    for feed in feeds:
        url = feed.get("url")

        if url:
            urls.append(url)

    return urls


def process_file(file_path, csv_writer):
    urls = extract_urls_from_json(file_path)

    progress_bar = tqdm(
        urls,
        desc=os.path.basename(file_path),
        unit="feed"
    )

    for url in progress_bar:
        reason = test_rss_content(url)
        success = 1 if reason == "Success" else 0

        csv_writer.writerow([
            file_path,
            url,
            success,
            reason
        ])

        progress_bar.set_postfix(
            success=success,
            reason=reason[:40]
        )


def find_json_files(directory):
    json_files = []

    for root, dirs, files in os.walk(directory):

        dirs[:] = [
            d for d in dirs
            if d not in (".git", ".github", "__pycache__", "venv")
        ]

        for file in files:
            if file.lower().endswith(".json"):
                json_files.append(
                    os.path.join(root, file)
                )

    return sorted(json_files)


if __name__ == "__main__":

    directory_path = "countries"

    json_files = find_json_files(directory_path)

    report_file = f"{directory_path}_report.csv"

    with open(
        report_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        csv_writer = csv.writer(csv_file)

        csv_writer.writerow([
            "File",
            "URL",
            "Success",
            "Reason"
        ])

        for file_path in json_files:
            process_file(file_path, csv_writer)

    print(f"\n✅ Report generated: {report_file}")