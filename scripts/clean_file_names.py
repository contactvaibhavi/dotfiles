import os
import re


def clean_filenames(directory=".", dry_run=False):
    """
    Scans a directory and removes extraneous Libgen tags, bracketed strings,
    formats author lists safely, and keeps only the year in parentheses.
    """

    # Regex 1: Matches " - libgen.li", " - libgen.rs", etc. at the end of the name
    libgen_pattern = re.compile(r"\s*-\s*libgen\.[a-z]+$", re.IGNORECASE)

    # Regex 2: Matches any bracketed text like "[10.1017_9781316779309]"
    bracket_pattern = re.compile(r"\s*\[.*?\]")

    # Regex 3: Matches leading or trailing single quotes
    quote_pattern = re.compile(r"^'|'$")

    # Regex 4: Matches (YYYY, Publisher) and keeps only the (YYYY)
    year_pattern = re.compile(r"\(\s*(\d{4})\s*(?:,[^)]*)?\)")

    changes_made = 0
    print(f"--- Starting in {'DRY RUN' if dry_run else 'RENAME'} mode ---")

    for filename in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue

        name, ext = os.path.splitext(filename)

        # Apply regex cleanups
        cleaned_name = libgen_pattern.sub("", name)
        cleaned_name = bracket_pattern.sub("", cleaned_name)
        cleaned_name = quote_pattern.sub("", cleaned_name).strip()
        cleaned_name = year_pattern.sub(r"(\1)", cleaned_name)

        # Safely format authors ONLY if the file uses the "Authors - Title" format
        if " - " in cleaned_name:
            parts = cleaned_name.split(" - ", 1)
            # Replace underscores with semicolons only in the first part (the authors)
            parts[0] = parts[0].replace("_", "; ")
            cleaned_name = " - ".join(parts)

        new_filename = cleaned_name + ext

        if filename != new_filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            if dry_run:
                print(f"[Would Rename]\n  Old: {filename}\n  New: {new_filename}\n")
            else:
                os.rename(old_path, new_path)
                print(f"[Renamed]\n  Old: {filename}\n  New: {new_filename}\n")

            changes_made += 1

    print(
        f"--- Finished. {changes_made} files {'would be ' if dry_run else ''}updated. ---"
    )


if __name__ == "__main__":
    target_directory = "."

    # Change to False when you are ready to actually rename the files
    clean_filenames(target_directory, dry_run=False)
