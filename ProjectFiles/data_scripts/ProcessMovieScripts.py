# This script will remove the <b> and </b> tags from a selected movie script in the raw data
# directory and save the cleaned script in the processed data directory.

import os
import re

raw_dir = '../data/raw/'
processed_dir = '../data/processed/'

# Get the list of movie scripts in the raw data directory
movie_scripts = os.listdir(raw_dir)
movie_scripts = [script for script in movie_scripts if script.endswith('.txt')] # Only the txt files

for script in movie_scripts:
    i =+ 1
    print(f"{i}) {script}")

# Select a movie script to process
choice = int(input('Which Movie script would you like to process: '))
to_process = movie_scripts[choice - 1]
print(f"Processing {to_process}...")
print()

# Edit the selected movie script
with open(raw_dir + to_process, 'r') as file:
    script = file.read()
    script = re.sub(r'<b>', '', script)
    script = re.sub(r'</b>', '', script)
    script = re.sub(r'</pre>', '', script)

# Save the cleaned movie script in the processed data directory
with open(processed_dir + to_process, 'w') as file:
    file.write(script)
