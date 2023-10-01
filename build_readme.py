import os
import re
import urllib.parse

def count_rss_sources(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        # Corrected regular expression to count RSS source URLs
        rss_count = len(re.findall(r'<outline[^>]*xmlUrl="[^"]+"', content))
        return rss_count

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
                readme_content += "| File | RSS Source Count |\n"
                readme_content += "|------|------------------|\n"

                for file in files:
                    file_path = os.path.join(relative_path, file)
                    rss_count = count_rss_sources(file_path)
                    # Encode the file_path for the URL
                    file_path_encoded = urllib.parse.quote(file_path.replace("\\", "/"))
                    readme_content += f"| [{file}]({file_path_encoded}) | {rss_count} |\n"

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

# Specify the directory you want to create the README for
directory_to_document = ""

template_file = "readme1.md"

create_readme(directory_to_document, template_file)
