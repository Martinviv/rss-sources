import os
import json
import urllib.parse

"""
Script to generate a README file from a list of JSON feed files.

"""


def extract_rss_sources(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    rss_sources = []

    for feed in data.get("feeds", []):
        title = feed.get("title")
        url = feed.get("url")

        if title and url:
            title = title.replace("|", r"\|")
            rss_sources.append((title, url))

    return rss_sources


def create_readme(directory, template_file):
    with open(template_file, "r", encoding="utf-8") as template:
        readme_content = template.read()

    for root, dirs, files in os.walk(directory):

        # Ignore Git folders
        dirs[:] = [d for d in dirs if d not in (".git", ".github", "__pycache__", "venv")]

        if root == directory:
            continue

        relative_path = os.path.relpath(root, directory)

        json_files = sorted(
            [f for f in files if f.lower().endswith(".json")]
        )

        if not json_files:
            continue

        readme_content += f"\n## {relative_path}\n\n"

        for file in json_files:
            file_path = os.path.join(root, file)

            rss_sources = extract_rss_sources(file_path)

            if not rss_sources:
                continue

            file_name = os.path.splitext(file)[0]

            relative_file_path = os.path.relpath(file_path, directory)
            relative_file_path = urllib.parse.quote(
                relative_file_path.replace("\\", "/")
            )

            readme_content += f"### [{file_name}]({relative_file_path})\n\n"
            readme_content += "| Title | URL |\n"
            readme_content += "|-------|-----|\n"

            for title, url in sorted(rss_sources, key=lambda x: x[0].lower()):
                readme_content += f"| {title} | [{url}]({url}) |\n"

            readme_content += "\n"

    with open(
        os.path.join(directory, "README.md"),
        "w",
        encoding="utf-8"
    ) as readme_file:
        readme_file.write(readme_content)


if __name__ == "__main__":
    directory_to_document = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(directory_to_document, "readme_header.md")

    create_readme(directory_to_document, template_file)

    print("✅ README.md generated successfully")