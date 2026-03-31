"""
Translate uploaded text files to Hindi and save the translated file
back to the same directory in the repository.
"""

import os
import sys
from pathlib import Path

from googletrans import Translator


def translate_file_to_hindi(file_path: str) -> str:
    """Read a text file and return its Hindi translation."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print(f"Skipping empty file: {file_path}")
        return ""

    translator = Translator()
    # Split into chunks of ~4000 chars to avoid API limits
    chunk_size = 4000
    chunks = [content[i : i + chunk_size] for i in range(0, len(content), chunk_size)]

    translated_chunks = []
    for chunk in chunks:
        result = translator.translate(chunk, dest="hi")
        translated_chunks.append(result.text)

    return "".join(translated_chunks)


def save_translated_file(file_path: str, translated_content: str) -> str:
    """Save translated content as <original_name>_hindi.txt in hindi_translated/ folder."""
    p = Path(file_path)
    output_dir = Path("hindi_translated")
    output_dir.mkdir(exist_ok=True)
    translated_path = output_dir / (p.stem + "_hindi.txt")
    with open(translated_path, "w", encoding="utf-8") as f:
        f.write(translated_content)
    print(f"Saved translated file: {translated_path}")
    return str(translated_path)


def main():
    changed_files = os.environ.get("CHANGED_FILES", "").strip()

    if not changed_files:
        print("No new .txt files found in uploads/. Nothing to do.")
        sys.exit(0)

    for file_path in changed_files.splitlines():
        file_path = file_path.strip()
        if not file_path or not file_path.endswith(".txt"):
            continue
        # Skip already-translated files
        if file_path.endswith("_hindi.txt"):
            continue

        print(f"Translating: {file_path}")
        translated = translate_file_to_hindi(file_path)
        if not translated:
            continue

        save_translated_file(file_path, translated)

    print("All files processed.")


if __name__ == "__main__":
    main()
