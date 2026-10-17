#!/bin/sh
# Redraw docs/img/kanata.svg with keymap-drawer (https://github.com/caksoylar/keymap-drawer).
# docs/kanata/keymap.json describes the layers of .config/kanata/config.kbd;
# docs/kanata/layout.json places every key of the MacBook keyboard.
set -eu
cd "$(dirname "$0")"
uvx --from keymap-drawer keymap -c kanata/draw.json draw -j kanata/layout.json kanata/keymap.json \
  | sed '1s|>|><rect width="100%" height="100%" fill="#32302f" rx="10"/>|' > img/kanata.svg
