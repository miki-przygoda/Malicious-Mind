# This script will remove the <b> and </b> tags from a selected movie script in the raw data
# directory and save the cleaned script in the processed data directory.
# This is just basic preprcoessing to make the scripts more readable and easier to work with.
# It's not going to perfeclty prepare a script for usability with a model.

import os
import re
import json

raw_dir = '../data/raw/'
processed_dir = '../data/processed/'

# Get the list of movie scripts in the raw data directory
movie_scripts = os.listdir(raw_dir)
movie_scripts = [script for script in movie_scripts if script.endswith('.txt')] # Only the txt files

i = 0
for script in movie_scripts:
    i += 1
    print(f"{i}) {script}")

# Select a movie script to process
choice = int(input('Which Movie script would you like to process: '))
to_process = movie_scripts[choice - 1]
print(f"Processing {to_process}...")
print()

# Edit the selected movie script
with open(os.path.join(raw_dir, to_process), 'r') as file:  # Processing for the txt file
    script = file.read()
    # Remove the <b> and </b> tags as well as the <pre> tag
    script = re.sub(r'<b>', '', script)
    script = re.sub(r'</b>', '', script)
    script = re.sub(r'</pre>', '', script)
    # Remove the extra spaces and empty lines
    script = re.sub(r'\s+', ' ', script)
    script = re.sub(r'\n+', '\n', script)
    script = re.sub(r'\n', ' ', script)
    # Remove special characters
    script = re.sub(r'[^\x00-\x7F]+', ' ', script)  # Non-ASCII
    script = re.sub(r'[\\/]', ' ', script)  # Forward and backslashes

    # Split the script into chunks of approximately 5000 characters
    chunk_size = 5000  # Approximate number of characters
    chunks = []
    current_chunk = ""
    for sentence in re.split(r'(?<=\.)\s+', script):
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    print("Script cleaned successfully!")

# Save the cleaned movie script in the processed data directory
cleaned_script_path = os.path.join(processed_dir, to_process)
with open(cleaned_script_path, 'w') as file:
    file.write('\n\n'.join(chunks))
    print("Processed script saved successfully!")

# Save the processed script in a JSON file with scenes
scenes = []
for idx, chunk in enumerate(chunks, start=1):
    scenes.append({
        "chunk_number": idx,
        "chunk_length": len(chunk),
        "all_caps_used": sum(1 for word in chunk.split() if word.isupper()),
        "content": chunk
    })

json_data = {
    "script_title": to_process,
    "scenes": scenes
}

json_output_path = os.path.join(processed_dir, to_process.replace('.txt', '.json'))
with open(json_output_path, 'w') as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)
    print("Processed script saved in JSON format successfully!")
