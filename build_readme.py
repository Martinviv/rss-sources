import os

def create_readme(directory):
    readme_content = "# rss-sources\nRSS sources used in the StreamSphere app\n\n" \
                    "## Goal\n" \
                    "The StreamSphere RSS Reader Android application aims to simplify the process " \
                    "of discovering and subscribing to RSS feeds on smartphones. To enhance user experience, " \
                    "the app provides a curated list of suggested sources spanning various topics and regions, " \
                    "making it easier for users to get started or explore new interests.\n\n" \
                    "## Suggest New Relevant Sources\n" \
                    "If you have recommendations for new sources or topics, please feel free to share them. " \
                    "Your suggestions can help to improve the app and other apps related to this project.\n\n" \
                    "## Multilingual Support\n" \
                    "Currently, our suggested sources for topics are primarily in English. However, " \
                    "you can also include sources in other languages as well.\n\n"
    
    for root, dirs, files in os.walk(directory):
        if root != directory:
            readme_content += f"## {os.path.basename(root)}\n\n"
        
        if files:
            readme_content += "| File | Description |\n"
            readme_content += "|------|-------------|\n"
            
            for file in files:
                file_path = os.path.join(root, file)
                readme_content += f"| [{file}]({file_path}) |  |\n"
                
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

# Specify the directory you want to create the README for
directory_to_document = ""

create_readme(directory_to_document)
