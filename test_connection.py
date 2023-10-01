import requests
import xml.etree.ElementTree as ET
import glob
import csv

def test_rss_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and 'xml' in response.headers['content-type']:
            # Check if the content is in XML format (RSS)
            try:
                tree = ET.fromstring(response.text)
                if tree.tag.lower() == 'rss' or tree.tag.lower() == 'feed':
                    return "Success"
                else:
                    return "The content is not a valid RSS feed."
            except ET.ParseError:
                return "XML parsing error."
        else:
            return "The server returned an invalid response."
    except requests.exceptions.RequestException as e:
        return f"HTTP request error: {str(e)}"

def process_file(file_path, csv_writer):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for outline in root.findall(".//outline"):
        if 'xmlUrl' in outline.attrib:
            url = outline.attrib['xmlUrl']
            reason = test_rss_content(url)
            success = 1 if reason == "Success" else 0
            csv_writer.writerow([url, success, reason])

# Directory containing the XML files to process
directory_path = 'recommended'

# Get the list of XML files in the directory
file_paths = glob.glob(directory_path + '/*.opml')

# Open the CSV file in write mode
with open('recommended_report.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['URL', 'Success', 'Reason'])  # Write the CSV header

    for file_path in file_paths:
        process_file(file_path, csv_writer)
