import requests
import xml.etree.ElementTree as ET
import glob
import csv
from tqdm import tqdm # pip install tqdm


'''
This script reads a list of OPML files and checks if the RSS feeds are valid.
'''


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
                # Check for common RSS tags
                rss_tags = ['rss', 'feed', 'rdf:RDF', 'channel'] 
                if any(tree.tag.lower().endswith(tag.lower()) for tag in rss_tags):
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
    
    outlines = root.findall(".//outline")
    
    total_outlines = len(outlines) - 1
    progress_bar = tqdm(total = total_outlines, desc=f"Processing {file_path}", unit="link")
   

    for outline in root.findall(".//outline"):
        if 'xmlUrl' in outline.attrib:
            url = outline.attrib['xmlUrl']
            reason = test_rss_content(url)
            success = 1 if reason == "Success" else 0
            csv_writer.writerow([url, success, reason])
            
            progress_bar.set_postfix({"Success": success, "Reason": reason})
            progress_bar.update(1) 


# Directory containing the XML files to process
directory_path = 'recommended'

# Get the list of XML files in the directory
file_paths = glob.glob(directory_path + '/*.opml')

# Open the CSV file in write mode
with open('countries_report.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['URL', 'Success', 'Reason'])  # Write the CSV header

    for file_path in file_paths:
        process_file(file_path, csv_writer)
