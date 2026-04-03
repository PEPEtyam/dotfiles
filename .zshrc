# ============================================================
# Environment variables
# ============================================================
export ZSH="$HOME/.oh-my-zsh"
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib/"
export EDITOR=hx

# ============================================================
# Oh My Posh (skip in Apple Terminal)
# ============================================================
if [ "$TERM_PROGRAM" != "Apple_Terminal" ]; then
  eval "$(oh-my-posh init zsh --config $HOME/.config/ohmyposh/robbyrussell_v1.omp.toml)"
fi

# ============================================================
# Direnv
# ============================================================
eval "$(direnv hook zsh)"

# ============================================================
# Shell options
# ============================================================
CASE_SENSITIVE="false"
HYPHEN_INSENSITIVE="true"
ENABLE_CORRECTION="true"

setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_SAVE_NO_DUPS
setopt globdots
setopt AUTO_MENU
setopt COMPLETE_IN_WORD

# ============================================================
# Oh My Zsh plugins
# ============================================================
plugins=(
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

# ============================================================
# Key bindings
# ============================================================
bindkey '^ ' autosuggest-accept
bindkey '^[[27;2;13~' autosuggest-execute
bindkey '^[[27;5;13~' autosuggest-execute
bindkey '^[[91;5u' up-line-or-history       # Ctrl+[
bindkey '^]' down-line-or-history            # Ctrl+]

# ============================================================
# Load Oh My Zsh
# ============================================================
source $ZSH/oh-my-zsh.sh

# ============================================================
# Completions
# ============================================================
# Speed up compinit – recheck once a day
autoload -Uz compinit
if [[ -n ~/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi

# Docker CLI completions
fpath=(/Users/a1/.docker/completions $fpath)

# fzf-tab (if installed)
if [[ -f ~/.oh-my-zsh/custom/plugins/fzf-tab/fzf-tab.plugin.zsh ]]; then
  source ~/.oh-my-zsh/custom/plugins/fzf-tab/fzf-tab.plugin.zsh

  zstyle ':fzf-tab:*' fzf-command ftb-tmux-popup
  zstyle ':fzf-tab:*' popup-min-size 80 10
  zstyle ':fzf-tab:*' popup-pad 10
  zstyle ':fzf-tab:*' popup-smart-size on
  zstyle ':completion:*' menu no
  zstyle ':fzf-tab:*' switch-group '[' ']'
  zstyle ':fzf-tab:*' fzf-flags '--layout=reverse-list'
  zstyle ':fzf-tab:*' use-fzf-default-opts yes

  # File preview
  zstyle ':fzf-tab:complete:(ls|cat|bat|less|nano|vim|code):*' \
    fzf-preview '[[ -f $realpath ]] && bat --color=always --style=plain --line-range=:50 $realpath || [[ -d $realpath ]] && ls -la $realpath'

  # Git log preview
  zstyle ':fzf-tab:complete:git-(log|diff|show):*' \
    fzf-preview 'git log --oneline --color=always $word | head -50'

  # Process preview
  zstyle ':fzf-tab:complete:(kill|killall):*' \
    fzf-preview 'ps aux | grep $word | head -10'

  # Man page preview
  zstyle ':fzf-tab:complete:man:*' \
    fzf-preview 'man $word | head -50'

  # Docker preview
  zstyle ':fzf-tab:complete:docker-(run|exec|stop|rm):*' \
    fzf-preview 'docker ps -a | grep $word || docker images | grep $word'
fi

# ============================================================
# Aliases
# ============================================================
alias y="yazi"

# ============================================================
# Theme / UI (bat, fzf)
# ============================================================
export BAT_THEME="gruvbox-dark"

export FZF_DEFAULT_OPTS=$FZF_DEFAULT_OPTS'
  --color=fg:-1,bg:-1,hl:
  --color=fg+:#f9f5d7,bg+:#282828,hl+:#f9f5d7
  --color=info:#98971a,prompt:#b8bb26,pointer:#c34043
  --color=marker:#d79921,spinner:#458588,header:#cc241d'

# ============================================================
# PATH construction (avoid overwriting)
# ============================================================
export PATH="/opt/homebrew/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/bin:$PATH"
export PATH="/bin:$PATH"
export PATH="/usr/sbin:$PATH"
export PATH="/sbin:$PATH"
export PATH="/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:$PATH"
export PATH="/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:$PATH"
export PATH="/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:$PATH"

# Source local env (if exists)
[ -f "$HOME/.local/bin/env" ] && . "$HOME/.local/bin/env"
