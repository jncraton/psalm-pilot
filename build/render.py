import json
from jinja2 import Environment, FileSystemLoader
import subprocess
from pathlib import Path

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

# Read in JSON hymn data
with open('data/hymns.json', 'r') as file:
    hymns = json.load(file)

# Set environment to templates folder
template_env = Environment(loader=FileSystemLoader('build/templates'))

# Load the index template and fill with data
index_template = template_env.get_template('index.jinja')
filled_index_template = index_template.render(hymns=hymns)

# Write out the template as `index.html`
with open('www/index.html', 'w', encoding='utf8') as hymns_page:
    hymns_page.write(filled_index_template)

# Load the recommendations page template
recommendations_template = template_env.get_template('recommendations.jinja')
filled_recommendations_template = recommendations_template.render(hymns=hymns)

with open('www/recommendations.html', 'w', encoding='utf8') as rec_page:
    rec_page.write(filled_recommendations_template)

# Load the hymn page template
hymn_template = template_env.get_template('hymn.jinja')

# Write out the hymn page for each hymn
for hymn in hymns:
    # Fill out the template for the hymn
    filled_hymn_template = hymn_template.render(hymn=hymn)

    # Write out the template with custom file name in hymns directory
    with open(f"www/hymns/{hymn['titleId']}.html", 'w', encoding='utf8') as hymn_page:
        hymn_page.write(filled_hymn_template)

# Create hymns list json file
hymns = sorted(
    str(p.relative_to(Path("www")).as_posix())
    for p in Path("www/hymns").rglob("*")
    if p.is_file())
Path("www/hymns_list.json").write_text(json.dumps(hymns, indent=2), encoding="utf-8")

# Load and write out service worker template with updated version
sw_template = template_env.get_template('service-worker.jinja')

version = get_git_short_hash()
rendered = sw_template.render(version=version)

with open('www/service-worker.js', 'w', encoding='utf8') as f:
    f.write(rendered)

print(f"Built service-worker.js with version: {version}")

