import os
import re
import urllib.parse
import xml.etree.ElementTree as ET

def extract_rss_sources(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        opml_content = ET.fromstring(content)
        opml_items = opml_content.findall(".//outline")

        rss_sources = []
        for item in opml_items:
            title = item.get("title")
            xml_url = item.get("xmlUrl")
            if title and xml_url:
                title = title.replace("|", r"\|")
                rss_sources.append((title, xml_url))
        
        return rss_sources

def create_readme(directory, template_file):
    with open(template_file, "r") as template:
        readme_content = template.read()

    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')  # Exclude the .git directory from further processing
        if root != directory:
            # Get the relative path for the directory
            relative_path = os.path.relpath(root, directory)

            readme_content += f"## {relative_path}\n\n"

            if files:
                for file in files:
                    file_path = os.path.join(root, file)
                    file_name = os.path.splitext(file)[0]  # Get the file name without extension
                    rss_sources = extract_rss_sources(file_path)
                    relative_file_path = os.path.relpath(file_path, directory)
                    relative_file_path = relative_file_path.replace(" ", "%20")


                    if rss_sources:
                        readme_content += f"### [{file_name}]({relative_file_path})\n\n"
                        readme_content += "| Title | URL |\n"
                        readme_content += "|-------|-----|\n"

                        for title, url in rss_sources:
                            readme_content += f"| {title} | [{url}]({url}) |\n"

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

# TODO : Specify the directory you want to create the README for
directory_to_document = ""

template_file = "readme1.md"

create_readme(directory_to_document, template_file)
