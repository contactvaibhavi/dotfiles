#!/bin/bash
# Open Multiple Apps in Full Screen
# Manages opening and fullscreening macOS applications

# Special case mappings for apps where display name != process name
declare -a special_mappings=(
    "iTerm|iTerm2|$HOME/Applications/iTerm.app"
    "iTerm2|iTerm2|$HOME/Applications/iTerm.app"
    "Google Chrome|Google Chrome|Google Chrome"
)

# Default config file location - use absolute path
config_file="$HOME/bin/apps_config.txt"

# Configuration
app_delay=3

# Colors
green='\033[0;32m'
blue='\033[0;34m'
yellow='\033[1;33m'
red='\033[0;31m'
nc='\033[0m'

get_process_and_path() {
    local app_name="$1"
    
    for mapping in "${special_mappings[@]}"; do
        IFS='|' read -r name process path <<< "$mapping"
        if [ "$name" = "$app_name" ]; then
            echo "$process|$path"
            return 0
        fi
    done
    
    echo "$app_name|$app_name"
}

check_and_fullscreen() {
    local app_name="$1"
    
    local process_name app_path
    IFS='|' read -r process_name app_path <<< "$(get_process_and_path "$app_name")"
    
    echo -e "${blue}Processing:${nc} $app_name"
    
    if ! pgrep -x "$process_name" > /dev/null 2>&1; then
        echo -e "  Not running - opening..."
        if [ -e "$app_path" ]; then
            open "$app_path"
        else
            open -a "$app_path"
        fi
        sleep "$app_delay"
    else
        echo -e "  Already running"
    fi
    
    echo -n "  Fullscreen status: "
    
    local result
    result=$(osascript - "$app_path" "$process_name" 2>&1 <<'ASCRIPT'
on run argv
    set appPath to item 1 of argv
    set processName to item 2 of argv
    
    try
        tell application appPath to activate
        delay 1
        
        tell application "System Events"
            tell process processName
                if (count windows) = 0 then
                    return "no_window"
                end if
                
                set hasFS to false
                set nonFSWindow to missing value
                
                repeat with w in windows
                    try
                        if (value of attribute "AXFullScreen" of w) is true then
                            set hasFS to true
                        else
                            set nonFSWindow to w
                        end if
                    end try
                end repeat
                
                if hasFS then
                    return "already_fullscreen"
                else if nonFSWindow is not missing value then
                    keystroke "f" using {control down, command down}
                    delay 1
                    return "toggled"
                else
                    return "no_support"
                end if
            end tell
        end tell
    on error e
        return "error: " & e
    end try
end run
ASCRIPT
)
    
    case "$result" in
        "already_fullscreen")
            echo -e "${green}Already fullscreen${nc}"
            ;;
        "toggled")
            echo -e "${green}✓ Made fullscreen${nc}"
            ;;
        "no_window")
            echo -e "${yellow}No window found${nc}"
            ;;
        "no_support")
            echo -e "${yellow}No fullscreen support${nc}"
            ;;
        error*)
            echo -e "${red}Error: ${result#error: }${nc}"
            ;;
        *)
            echo -e "${yellow}Unknown: $result${nc}"
            ;;
    esac
}

load_apps_from_config() {
    if [ ! -f "$config_file" ]; then
        echo -e "${red}Error: Config file not found: $config_file${nc}" >&2
        exit 1
    fi
    
    while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
        echo "$line" | xargs
    done < "$config_file"
}

main() {
    echo "================================================"
    echo "  Managing Apps in Full Screen"
    echo "================================================"
    echo ""
    
    local apps_to_process=()
    if [ $# -eq 0 ]; then
        while IFS= read -r app; do
            apps_to_process+=("$app")
        done < <(load_apps_from_config)
    else
        apps_to_process=("$@")
    fi
    
    for app in "${apps_to_process[@]}"; do
        check_and_fullscreen "$app"
        echo ""
    done
    
    echo "================================================"
    echo -e "${green}Done!${nc}"
    echo "================================================"
    echo ""
}

main "$@"