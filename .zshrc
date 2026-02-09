# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export PATH="$HOME/.local/bin:$PATH"
export ZSH="$HOME/.oh-my-zsh"
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
# eval "$(starship init zsh)"
alias git='grc git'

PROMPT="%F{cyan}%n %1~ %# %f"
export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"

export LDFLAGS="-L/opt/homebrew/opt/sqlite/lib"
export CPPFLAGS="-I/opt/homebrew/opt/sqlite/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/sqlite/lib/pkgconfig"
export LDFLAGS="-L/opt/homebrew/opt/tcl-tk@8/lib"
export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk@8/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk@8/lib/pkgconfig"
export LDFLAGS="-L/opt/homebrew/opt/zlib/lib"
export CPPFLAGS="-I/opt/homebrew/opt/zlib/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/zlib/lib/pkgconfig"

eval "$(pyenv virtualenv-init -)"
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

eval "$(oh-my-posh init zsh --config $(brew --prefix oh-my-posh)/themes/atomic.omp.json)"
export PATH="$HOME/gitCode:$PATH"
alias obsidian_vault="open \"$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian\""
export OBSIDIAN_VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian"


alias obsidian='open -a Obsidian'
alias obsidian_vault_open='cd "$OBSIDIAN_VAULT"'

# Add ~/bin to PATH
export PATH="$HOME/bin:$PATH"

# Textbook shortcuts
export TEXTBOOKS_DIR="$HOME/Documents/Textbooks"
alias tb='textbook'
alias tbl='find "$TEXTBOOKS_DIR" -type f -name "*.pdf" -exec basename {} \;'

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Brew maintenance
alias brewup='brew update && brew upgrade && brew cleanup && brew doctor'
alias ls='eza --icons'
alias ll='eza -l --icons --git'
alias la='eza -la --icons --git'
alias cat='bat'
alias rg='rg --smart-case'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
alias gd='git diff'
alias reload='source ~/.zshrc'
alias note='cd "$OBSIDIAN_VAULT" && touch "$(date +%Y-%m-%d)-note.md" && obsidian'
alias py='python3'
alias search='rg --hidden --follow --ignore-file ~/.gitignore'
alias textbook_open='open "$TEXTBOOKS_DIR/$(find "$TEXTBOOKS_DIR" -name "*.pdf" | fzf)"'
alias textbook_note='cd "$OBSIDIAN_VAULT" && nano "$(basename $(find "$TEXTBOOKS_DIR" -name "*.pdf" | fzf) .pdf)-notes.md"'
alias clip='pbpaste >> "$OBSIDIAN_VAULT/inbox.md" && echo "\n---\n" >> "$OBSIDIAN_VAULT/inbox.md"'

# Fixed daily note alias - opens specific file
alias daily='cd "$OBSIDIAN_VAULT" && touch "$(date +%Y-%m-%d).md" && open "obsidian://open?vault=Obsidian&file=$(date +%Y-%m-%d).md"'

# Fixed note alias - opens specific file
alias note='cd "$OBSIDIAN_VAULT" && NOTE_NAME="$(date +%Y-%m-%d)-note.md" && touch "$NOTE_NAME" && open "obsidian://open?vault=Obsidian&file=${NOTE_NAME}"'
# Obsidian Planner shortcuts
alias todo='open "obsidian://open?vault=Obsidian&file=___Planner/To%20Do"'
alias year_important='open "obsidian://open?vault=Obsidian&file=___Planner/Year%20Important"'
alias del_to_do='open "obsidian://open?vault=Obsidian&file=___Planner/Del%20ToDo"'
alias kanban='open "obsidian://open?vault=Obsidian&file=___Planner/Kanban%20Board"'
# Obsidian Intw shortcuts
alias concepts='open "obsidian://open?vault=Obsidian&file=Intw/Concepts"'
alias DSA_revision='open "obsidian://open?vault=Obsidian&file=Intw/DSA%20Revision"'
alias project_ideas='open "obsidian://open?vault=Obsidian&file=___Planner/Project%20Ideas"'
alias leetcode_saved_questions='open "obsidian://open?vault=Obsidian&file=Intw/Leetcode%20Questions"'
# Obsidian Networking shortcuts
alias CRM_log='open "obsidian://open?vault=Obsidian&file=Networking/CRM%20Log"'
alias my_website='open "obsidian://open?vault=Obsidian&file=Networking/My%20Website"'
alias invites='open "obsidian://open?vault=Obsidian&file=Networking/Invites"'
alias CFPs='open "obsidian://open?vault=Obsidian&file=Networking/CFPs/CFP%20Tracker%20Log"'
export RESUME_DIR="$HOME/Documents/Resume/Search"
export CDPATH=".:$HOME/gitCode:$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents:$HOME"
alias configs='open "obsidian://open?vault=Obsidian&file=Admin/Configs"'

# Open 2 cute pages in Obsidian
alias diary='open "obsidian://open?vault=Obsidian&file=__Journal/2%20cute%20pages"'

# ===== TIMER START =====
# Timer with LARGE GREEN alert that FORCES itself to front
timer() {
    if [ -z "$1" ]; then
        echo "Usage: timer <minutes> [seconds] <task> <alarm_type>"
        echo "Alarm types: short, musical, loud, desk, digital, funny, old_desk"
        echo ""
        echo "Examples:"
        echo "  timer 25 study loud"
        echo "  timer 0 3 yo funny"
        return 1
    fi
    
    minutes=$1
    shift
    
    # Default values
    seconds=0
    task="timer"
    alarm_type="${TIMER_ALARM:-loud}"
    custom_sound=""
    
    # Get all remaining args
    remaining_args=("$@")
    
    # Check if first remaining arg is a number (seconds)
    if [[ "${remaining_args[1]}" =~ ^[0-9]+$ ]]; then
        seconds="${remaining_args[1]}"
        task="${remaining_args[2]}"
        if [ -n "${remaining_args[3]}" ]; then
            if [[ "${remaining_args[3]}" == /* ]] || [[ "${remaining_args[3]}" == ~* ]] || [[ "${remaining_args[3]}" =~ \.(mp3|wav|m4a)$ ]]; then
                custom_sound="${remaining_args[3]}"
            else
                alarm_type="${remaining_args[3]}"
            fi
        fi
    else
        task="${remaining_args[1]}"
        if [ -n "${remaining_args[2]}" ]; then
            if [[ "${remaining_args[2]}" == /* ]] || [[ "${remaining_args[2]}" == ~* ]] || [[ "${remaining_args[2]}" =~ \.(mp3|wav|m4a)$ ]]; then
                custom_sound="${remaining_args[2]}"
            else
                alarm_type="${remaining_args[2]}"
            fi
        fi
    fi
    
    total_seconds=$((minutes * 60 + seconds))
    
    # Display timer info
    if [ $seconds -eq 0 ]; then
        echo "⏱️  Timer: $minutes min for '$task'"
    else
        echo "⏱️  Timer: ${minutes}m ${seconds}s for '$task'"
    fi
    
    # Select alarm sound file
    if [ -n "$custom_sound" ]; then
        alarm_file="${custom_sound/#\~/$HOME}"
        if [ ! -f "$alarm_file" ]; then
            alarm_file="$HOME/.timer_sounds/loud_alarm.mp3"
        fi
    else
        case $alarm_type in
            short) alarm_file="$HOME/.timer_sounds/short_alarm.mp3" ;;
            musical) alarm_file="$HOME/.timer_sounds/musical_alarm.mp3" ;;
            loud) alarm_file="$HOME/.timer_sounds/loud_alarm.mp3" ;;
            desk) alarm_file="$HOME/.timer_sounds/desk_alarm.mp3" ;;
            digital) alarm_file="$HOME/.timer_sounds/digital_alarm.mp3" ;;
            funny) alarm_file="$HOME/.timer_sounds/funny_alarm.mp3" ;;
            old_desk) alarm_file="$HOME/.timer_sounds/old_desk_alarm.mp3" ;;
            *) alarm_file="$HOME/.timer_sounds/loud_alarm.mp3" ;;
        esac
    fi
    
    # Create Swift app for alarm - FORCES TO FRONT
    cat > /tmp/timer_alarm.swift <<SWIFT
import Cocoa

class AlarmWindow: NSWindow {
    init(task: String) {
        let screenSize = NSScreen.main?.frame.size ?? NSSize(width: 1200, height: 800)
        let width: CGFloat = screenSize.width * 0.75
        let height: CGFloat = screenSize.height * 0.75
        let x = (screenSize.width - width) / 2
        let y = (screenSize.height - height) / 2
        
        super.init(
            contentRect: NSRect(x: x, y: y, width: width, height: height),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        
        self.title = "ALARM"
        self.isReleasedWhenClosed = false
        
        // FORCE window to stay on top of EVERYTHING
        self.level = .screenSaver
        self.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        
        let greenColor = NSColor(red: 0.18, green: 0.8, blue: 0.44, alpha: 1.0)
        self.backgroundColor = greenColor
        
        let contentView = NSView(frame: self.contentView!.bounds)
        contentView.wantsLayer = true
        contentView.layer?.backgroundColor = greenColor.cgColor
        
        let message = NSTextField(labelWithString: "Time Up for '\\(task)'")
        message.font = NSFont.systemFont(ofSize: 72, weight: .bold)
        message.textColor = .white
        message.alignment = .center
        message.frame = NSRect(x: 50, y: height/2, width: width-100, height: 200)
        contentView.addSubview(message)
        
        let button = NSButton(frame: NSRect(x: width/2 - 200, y: 150, width: 400, height: 100))
        button.title = "STOP ALARM"
        button.bezelStyle = .rounded
        button.font = NSFont.systemFont(ofSize: 36, weight: .bold)
        button.target = self
        button.action = #selector(stopAlarm)
        contentView.addSubview(button)
        
        self.contentView = contentView
    }
    
    @objc func stopAlarm() {
        NSApplication.shared.terminate(nil)
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: AlarmWindow!
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        let task = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "timer"
        window = AlarmWindow(task: task)
        window.makeKeyAndOrderFront(nil)
        
        // FORCE to front and activate
        NSApp.activate(ignoringOtherApps: true)
        window.orderFrontRegardless()
        window.makeKey()
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
SWIFT
    
    # Start timer
    (
        sleep $total_seconds
        
        say -v Samantha "Time up for $task" &
        say_pid=$!
        
        (while true; do afplay "$alarm_file"; sleep 0.3; done) &
        alarm_loop_pid=$!
        
        # Compile and run Swift app
        swiftc /tmp/timer_alarm.swift -o /tmp/timer_alarm 2>/dev/null
        /tmp/timer_alarm "$task"
        
        # Kill alarm when window closes
        kill $alarm_loop_pid $say_pid 2>/dev/null
        killall -9 afplay 2>/dev/null
        killall -9 say 2>/dev/null
        rm -f /tmp/timer_alarm.swift /tmp/timer_alarm
    ) &
    
    timer_pid=$!
    echo "Timer running (PID: $timer_pid)"
    echo "To stop: timer_stop"
}

timer_stop() {
    echo "🛑 Stopping..."
    pkill -f "sleep" 2>/dev/null
    pkill -f "timer_alarm" 2>/dev/null
    killall -9 afplay 2>/dev/null
    killall -9 say 2>/dev/null
    rm -f /tmp/timer_alarm.swift /tmp/timer_alarm
    echo "✅ Stopped"
}

alias timer5='timer 5 break short'
alias timer25='timer 25 pomodoro loud'
export TIMER_ALARM=loud
# ===== TIMER END =====
