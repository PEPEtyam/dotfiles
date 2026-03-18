export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib/"
export PATH="/opt/homebrew/bin:$PATH"
export EDITOR=hx

if [ "$TERM_PROGRAM" != "Apple_Terminal" ]; then
  eval "$(oh-my-posh init zsh --config $HOME/.config/ohmyposh/robbyrussell_v1.omp.toml)"
fi

eval "$(direnv hook zsh)"

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time Oh My Zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
# ZSH_THEME="robbyrussell"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
CASE_SENSITIVE="false"
HYPHEN_INSENSITIVE="true"

ENABLE_CORRECTION="true"

# Remove duplicates from history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_SAVE_NO_DUPS

# Enable hidden files in completion
setopt globdots
# Enable menu completion
setopt AUTO_MENU
# Enable completion caching
setopt COMPLETE_IN_WORD

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
plugins=(
  # dirhistory
  brew
  git
  gitfast
  docker
  macos
  httpie
  eza
  docker-compose
  npm
  pre-commit
  kubectl
  python
  rust
  zsh-autosuggestions
  fast-syntax-highlighting
  zoxide
  fzf-tab
  
  colored-man-pages
  command-not-found
  extract
  web-search
  copyfile
  copypath
)

# zsh-autosuggestions
bindkey '^ ' autosuggest-accept
bindkey '^[[27;2;13~' autosuggest-execute
bindkey '^[[27;5;13~' autosuggest-execute

# dirhistory
# bindkey "˙" dirhistory_zle_dirhistory_back      # Option+h = ←
# bindkey "¬" dirhistory_zle_dirhistory_future    # Option+l = →
# bindkey "˚" dirhistory_zle_dirhistory_up        # Option+k = ↑
# bindkey "∆" dirhistory_zle_dirhistory_down      # Option+j = ↓

# history
bindkey '^[[91;5u' up-line-or-history       # Control+[ = предыдущая команда (↑)
bindkey '^]' down-line-or-history     # Control+] = следующая команда (↓)


source $ZSH/oh-my-zsh.sh

# === COMPLETION CONFIGURATION ===
# Load completions
autoload -Uz compinit
# Speed up compinit by checking once a day
if [[ -n ~/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi

# === FZF-TAB CONFIGURATION (если установлен) ===
if [[ -f ~/.oh-my-zsh/custom/plugins/fzf-tab/fzf-tab.plugin.zsh ]]; then
  # Load fzf-tab after compinit but before plugins which will wrap widgets
  source ~/.oh-my-zsh/custom/plugins/fzf-tab/fzf-tab.plugin.zsh

  zstyle ':fzf-tab:*' fzf-command ftb-tmux-popup
  zstyle ':fzf-tab:*' popup-min-size 80 10
  zstyle ':fzf-tab:*' popup-pad 10
  zstyle ':fzf-tab:*' popup-smart-size on
  
  # fzf-tab configuration
  zstyle ':completion:*' menu no
  zstyle ':fzf-tab:*' switch-group '[' ']'
  zstyle ':fzf-tab:*' fzf-flags '--layout=reverse-list'
  zstyle ':fzf-tab:*' use-fzf-default-opts yes
  
  # File preview for common commands
  zstyle ':fzf-tab:complete:(ls|cat|bat|less|nano|vim|code):*' \
    fzf-preview '[[ -f $realpath ]] && bat --color=always --style=plain --line-range=:50 $realpath || [[ -d $realpath ]] && ls -la $realpath'
  
  # Git log preview
  zstyle ':fzf-tab:complete:git-(log|diff|show):*' \
    fzf-preview 'git log --oneline --color=always $word | head -50'
  
  # Process preview for kill commands
  zstyle ':fzf-tab:complete:(kill|killall):*' \
    fzf-preview 'ps aux | grep $word | head -10'
  
  # Man page preview
  zstyle ':fzf-tab:complete:man:*' \
    fzf-preview 'man $word | head -50'
  
  # Docker container/image preview
  zstyle ':fzf-tab:complete:docker-(run|exec|stop|rm):*' \
    fzf-preview 'docker ps -a | grep $word || docker images | grep $word'
fi

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

# My aliases
alias y="yazi"

export BAT_THEME="gruvbox-dark"

export FZF_DEFAULT_OPTS=$FZF_DEFAULT_OPTS'
  --color=fg:-1,bg:-1,hl:
  --color=fg+:#f9f5d7,bg+:#282828,hl+:#f9f5d7
  --color=info:#98971a,prompt:#b8bb26,pointer:#c34043
  --color=marker:#d79921,spinner:#458588,header:#cc241d'

# Kanagawa-paper
# export FZF_DEFAULT_OPTS="
#   --color=fg:#54546D,fg+:#dcd7ba,bg:-1,bg+:#1F1F28
#   --color=hl:#54546D,hl+:#c8c093,info:#8a9a7b,marker:#FF5D62
#   --color=prompt:#87a987,spinner:#938aa9,pointer:#c4746e,header:#7aa89f
#   --color=border:#54546D,scrollbar:#363646,preview-fg:#DCD7BA,label:#aeaeae
#   --color=query:#c5c9c5
#   --preview-window=border-rounded"

export PATH=/opt/homebrew/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin
eval 

. "$HOME/.local/bin/env"
export PATH="$HOME/.cargo/bin:$PATH"
# The following lines have been added by Docker Desktop to enable Docker CLI completions.
fpath=(/Users/a1/.docker/completions $fpath)
autoload -Uz compinit
compinit
# End of Docker CLI completions
