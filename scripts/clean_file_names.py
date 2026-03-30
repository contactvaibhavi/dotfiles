import os
import re
import argparse

def clean_filenames(directory=".", dry_run=True):
    """
    Scans a directory and removes extraneous Libgen tags, Z-Library tags, 
    bracketed strings, formats author lists safely, and cleans up dates.
    """
    
    # Regex 1: Matches " - libgen.li", " - libgen.rs", etc.
    libgen_pattern = re.compile(r'\s*-\s*libgen\.[a-z]+$', re.IGNORECASE)
    
    # Regex 2: Matches any square-bracketed text like "[10.1017_9781316779309]"
    bracket_pattern = re.compile(r'\s*\[.*?\]')
    
    # Regex 3: Matches leading or trailing single quotes and stray question marks
    quote_pattern = re.compile(r"^'|'$|^\?|\?$")
    
    # Regex 4: Matches (YYYY, Publisher) and keeps only the (YYYY)
    year_pattern = re.compile(r'\(\s*(\d{4})\s*(?:,[^)]*)?\)')

    # Regex 5: Matches Z-Library tags inside parentheses e.g., "(z-library.sk, 1lib.sk)"
    zlib_pattern = re.compile(r'\s*\([^)]*(z-lib|1lib|z-library)[^)]*\)', re.IGNORECASE)

    changes_made = 0
    print(f"--- Starting in {'DRY RUN' if dry_run else 'RENAME'} mode ---")

    for filename in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue

        name, ext = os.path.splitext(filename)

        # Apply regex cleanups sequentially
        cleaned_name = libgen_pattern.sub('', name)
        cleaned_name = zlib_pattern.sub('', cleaned_name) 
        cleaned_name = bracket_pattern.sub('', cleaned_name)
        cleaned_name = quote_pattern.sub('', cleaned_name).strip()
        cleaned_name = year_pattern.sub(r'(\1)', cleaned_name)
        
        # Safely format authors ONLY if the file uses the "Authors - Title" format
        if ' - ' in cleaned_name:
            parts = cleaned_name.split(' - ', 1)
            parts[0] = parts[0].replace('_', '; ')
            cleaned_name = ' - '.join(parts)

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

    print(f"--- Finished. {changes_made} files {'would be ' if dry_run else ''}updated. ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up extraneous tags from PDF filenames.")
    
    parser.add_argument(
        "--rename", 
        action="store_true", 
        help="Execute the actual file renaming (disables dry-run mode)."
    )
    
    parser.add_argument(
        "-d", "--directory", 
        default=".", 
        help="Target directory containing the PDFs (default: current directory)."
    )
    
    args = parser.parse_args()
    
    # If --rename is passed, dry_run becomes False
    is_dry_run = not args.rename
    
    clean_filenames(directory=args.directory, dry_run=is_dry_run)