import json
from jinja2 import Environment, FileSystemLoader

# Read in JSON hymn data
with open('data/hymns.json', 'r') as file:
    hymns = json.load(file)

# Set environment to templates folder
env = Environment(loader=FileSystemLoader('templates'))

# Load the index template and fill with data
index_template = env.get_template('index.jinja')
filled_index_template = index_template.render(hymns=hymns)

# Write out the template as `index.html`
with open('index.html', 'w') as hymns_page:
    hymns_page.write(filled_index_template)