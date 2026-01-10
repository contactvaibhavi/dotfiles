# Script Manager

Easily install scripts to `~/bin` and make them executable.

## Structure
```
script-manager/
├── install-script.sh       # Install single script
├── install-all.sh          # Install all scripts in scripts/
├── scripts/                # Put your scripts here
│   └── example.sh
└── README.md
```

## Usage

### Install Single Script
```bash
# Install with original name (minus .sh)
./install-script.sh scripts/my-script.sh

# Install with custom name
./install-script.sh scripts/my-script.sh custom-name
```

### Install All Scripts
```bash
./install-all.sh
```

### Add New Script

1. Create your script in `scripts/` folder:
```bash
   nano scripts/my-new-script.sh
```

2. Install it:
```bash
   ./install-script.sh scripts/my-new-script.sh
```

3. Use it:
```bash
   my-new-script
```

## Examples

### Install Obsidian Fullscreen Script
```bash
./install-script.sh scripts/open-obsidian-fullscreen.sh obsidian-fullscreen
```

Then use:
```bash
obsidian-fullscreen
```

### Install Textbook Opener
```bash
./install-script.sh ../Obsidian/textbook-opener/search_textbooks_by_name.sh textbook
```

## Notes

- Scripts are copied to `~/bin`
- Made executable automatically
- Original files remain in `scripts/` folder
- Ensure `~/bin` is in your PATH
