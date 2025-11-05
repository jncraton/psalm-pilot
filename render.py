import json
from jinja2 import Environment, FileSystemLoader
import subprocess

# Read in JSON hymn data
with open('data/hymns.json', 'r') as file:
    hymns = json.load(file)

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

sw_template = env.get_template('service-worker.jinja')
    
version = get_git_short_hash()
rendered = sw_template.render(version=version)

with open('service-worker.js', 'w') as f:
    f.write(rendered)

print(f"Built service-worker.js with version: {version}")