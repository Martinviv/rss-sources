import xml.etree.ElementTree as ET
import glob
import csv

def extract_http_links(file_path):
    http_links = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    outlines = root.findall(".//outline")
    
    for outline in outlines:
        if 'xmlUrl' in outline.attrib:
            url = outline.attrib['xmlUrl']
            if url.startswith("http://"):
                http_links.append((url, file_path))
    
    return http_links

# Directory containing the XML files to process
directory_path = 'countries'

# Get the list of XML files in the directory
file_paths = glob.glob(directory_path + '/*.opml')

# Extract HTTP links and their corresponding OPML files
http_links_list = []
for file_path in file_paths:
    http_links_list.extend(extract_http_links(file_path))

# Write the HTTP links and their corresponding OPML files to a CSV file
with open('http_links_report.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['HTTP URL', 'OPML File'])  # Write the CSV header
    csv_writer.writerows(http_links_list)
