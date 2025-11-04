import json
from jinja2 import Environment, FileSystemLoader
import subprocess

# Read in JSON hymn data
with open('data/hymns.json', 'r') as file:
    hymns = json.load(file)

# Service worker versioning logic
SW_TEMPLATE_PATH = 'service-worker-template.js'
SW_OUTPUT_PATH = 'service-worker.js'

def get_git_short_hash():
    try:
        # Use subprocess to run the git command
        git_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.STDOUT
        ).strip().decode('utf-8')
        return git_hash
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: Could not get git commit hash. Error: {e}")
        return 'dev'

def version_service_worker(version_string):
    try:
        with open(SW_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Replace the placeholder with the actual version string
        versioned_content = template_content.replace('%%HASH%%', version_string)

        with open(SW_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(versioned_content)

        print(f"Created {SW_OUTPUT_PATH} with cache version: psalm-pilot-cache-{version_string}")
    except FileNotFoundError:
        print(f"Error: {SW_TEMPLATE_PATH} not found. Service worker was not versioned.")

# Main rendering process
if __name__ == "__main__":
    print("Starting build process...")

    # Get the git hash
    version_hash = get_git_short_hash()
    
    # Version the service worker using the git hash
    version_service_worker(version_hash)

# Set environment to templates folder
env = Environment(loader=FileSystemLoader('templates'))

# Load the index template and fill with data
index_template = env.get_template('index.jinja')
filled_index_template = index_template.render(hymns=hymns)

# Write out the template as `index.html`
with open('index.html', 'w') as hymns_page:
    hymns_page.write(filled_index_template)

# Load the hymn page template
hymn_template = env.get_template('hymn.jinja')

# Write out the hymn page for each hymn
for hymn in hymns:
    # Fill out the template for the hymn
    filled_hymn_template = hymn_template.render(hymn=hymn)

    # Write out the template with custom file name in hymns directory
    with open(f"hymns/{hymn['titleId']}.html", 'w') as hymn_page:
        hymn_page.write(filled_hymn_template)