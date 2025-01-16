import os
import re
import json

def lines():
    print(60 * "-")

def Second():
    raw_dir = '../data/preprocessed - using script/'
    processed_dir = '../data/processed/'

    # Get the list of movie scripts in the raw data directory
    movie_scripts = os.listdir(raw_dir)
    movie_scripts = [script for script in movie_scripts if script.endswith('.txt')]  # Only the txt files
    print("Any input that isn't a number will exit the program.")
    i = 0
    for script in movie_scripts:
        i += 1
        print(f"{i}) {script}")

    lines()

    while True:
        try:
            # Select a movie script to process
            choice = input('Which Movie script would you like to process again: ')
            if not choice.isdigit():
                print("Exiting...")
                lines()
                exit()
            to_process = movie_scripts[int(choice) - 1]
            print(f"Processing {to_process}...")
            lines()
            break
        except (ValueError, IndexError):
            print("Invalid input.")
            continue

    # Read the selected movie script
    with open(os.path.join(raw_dir, to_process), 'r') as file:
        script = file.read()

    # Split the script into chunks based on blank lines
    chunks = script.split('\n\n')

    # Process each chunk for all-caps words
    cleaned_chunks = []
    for chunk_idx, chunk in enumerate(chunks, start=1):
        print(f"\nProcessing Chunk {chunk_idx}/{len(chunks)}...")

        # Extract all-caps words from the chunk
        all_caps_words = re.findall(r'\b[A-Z]{2,}\b', chunk)
        unique_caps = sorted(set(all_caps_words))

        if not unique_caps:
            print("No all-caps words found in this chunk.")
            cleaned_chunks.append(chunk)
            continue

        # Display the unique all-caps words to the user
        print("The following all-caps words were found in this chunk:")
        for idx, word in enumerate(unique_caps, start=1):
            print(f"{idx}. {word}")

        # Allow the user to select words to remove
        to_remove = input("\nEnter the numbers of the words to remove for this chunk, separated by commas (e.g., 1,3,5): ")
        to_remove_indices = [int(num.strip()) for num in to_remove.split(',') if num.strip().isdigit()]
        words_to_remove = [
            unique_caps[idx - 1]
            for idx in to_remove_indices
            if 0 < idx <= len(unique_caps)
        ]

        # Remove the selected words and lowercase the others
        for word in unique_caps:
            if word in words_to_remove:
                chunk = re.sub(rf'\b{word}\b', '', chunk)
            else:
                chunk = re.sub(rf'\b{word}\b', word.lower(), chunk)

        # Append the cleaned chunk
        cleaned_chunks.append(chunk)
        print("Selected words have been removed, and remaining words have been converted to lowercase.")

    # Combine all cleaned chunks into a single text
    combined_script = '\n\n'.join(cleaned_chunks)

    # Re-chunk the combined script into new chunks of approximately 5000 characters
    chunk_size = 5000
    new_chunks = []
    current_chunk = ""
    for sentence in re.split(r'(?<=\.)\s+', combined_script):
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + " "
        else:
            new_chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        new_chunks.append(current_chunk.strip())

    print("Script has been re-chunked successfully!")

    # Save the re-chunked script
    cleaned_script_path = os.path.join(processed_dir, to_process.replace('.txt', '_rechunked.txt'))
    with open(cleaned_script_path, 'w') as file:
        file.write('\n\n'.join(new_chunks))
        print("Re-chunked script saved successfully!")

    # Save the re-chunked script as JSON
    scenes = []
    for idx, chunk in enumerate(new_chunks, start=1):
        scenes.append({
            "chunk_number": idx,
            "chunk_length": len(chunk),
            "content": chunk
        })

    json_data = {
        "script_title": to_process,
        "scenes": scenes
    }

    json_output_path = os.path.join(processed_dir, to_process.replace('.txt', '_rechunked.json'))
    with open(json_output_path, 'w') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)
        print("Re-chunked script saved in JSON format successfully!")


Second()