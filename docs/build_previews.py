#!/usr/bin/env python3
"""Render palette and terminal preview SVGs into docs/img.

Everything is drawn from the palette in .config/palette/PALETTE.md.
The bat preview is real `bat` output (needs bat and its gruvbox-material-alabaster theme).

    python3 docs/build_previews.py
"""
import html
import os
import re
import subprocess
import tempfile

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

C = {
    "bg0": "#32302f", "bg1": "#3c3836", "bg3": "#504945",
    "grey0": "#7c6f64", "grey1": "#928374", "grey2": "#a89984",
    "fg0": "#d4be98", "fg1": "#ddc7a1", "white": "#f9f5d7",
    "red": "#ea6962", "orange": "#e78a4e", "yellow": "#d5a034", "green": "#98971a",
    "sage": "#89b482", "blue": "#7daea3", "purple": "#d3869b", "beige": "#bdae93",
    "orange_light": "#f0a878", "magenta": "#b27085", "ansi_red": "#cc241d",
    "diff_add": "#3a4a30", "diff_add_word": "#4f6640", "diff_del": "#4d2e2c", "diff_del_word": "#6b3a36",
}
FONT = "'DepartureMono Nerd Font','SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
FS, CW, LH, PAD = 14, 8.4, 20, 18


def esc(text):
    return html.escape(text, quote=False)


class Term:
    def __init__(self, cols, rows, title, bg="bg1"):
        self.cols, self.rows, self.title, self.bg = cols, rows, title, C[bg]
        self.items = []

    def _xy(self, row, col):
        return PAD + col * CW, 38 + PAD + row * LH

    def fill(self, row, col, width, color, height=1):
        x, y = self._xy(row, col)
        self.items.append(
            f'<rect x="{x:.1f}" y="{y - 15}" width="{width * CW:.1f}" height="{LH * height}" fill="{C.get(color, color)}"/>'
        )

    def put(self, row, col, text, fg="fg0", bg=None, bold=False, italic=False, underline=False):
        if not text:
            return
        if bg:
            self.fill(row, col, len(text), C.get(bg, bg))
        x, y = self._xy(row, col)
        style = ""
        if bold:
            style += ' font-weight="bold"'
        if italic:
            style += ' font-style="italic"'
        if underline:
            style += ' text-decoration="underline"'
        color = C.get(fg, fg)
        self.items.append(
            f'<text x="{x:.1f}" y="{y}" fill="{color}" textLength="{len(text) * CW:.1f}" '
            f'lengthAdjust="spacing" xml:space="preserve"{style}>{esc(text)}</text>'
        )

    def line(self, row, col, markup, base="fg0", bg=None, punct=True):
        """Markup: ⟦color|text⟧ spans; color may end with ! (bold) ~ (italic) _ (underline)."""
        pos = col
        tokens = re.split(r"(⟦[\w!~_]+\|.*?⟧)", markup)
        for token in tokens:
            if not token:
                continue
            m = re.fullmatch(r"⟦([\w!~_]+)\|(.*?)⟧", token)
            if m:
                name, text = m.groups()
                flags = {
                    "bold": name.endswith("!") or "!" in name,
                    "italic": "~" in name,
                    "underline": name.endswith("_"),
                }
                name = name.rstrip("!~_")
                self.put(row, pos, text, name, bg, **flags)
                pos += len(text)
            else:
                for chunk in re.split(r"(::|[.,;:])", token) if punct else [token]:
                    if not chunk:
                        continue
                    color = "grey2" if chunk in ("::", ".", ",", ";", ":") else base
                    self.put(row, pos, chunk, color, bg)
                    pos += len(chunk)
        return pos

    def svg(self):
        width = PAD * 2 + self.cols * CW
        height = 38 + PAD * 2 + self.rows * LH
        dots = "".join(
            f'<circle cx="{22 + i * 18}" cy="19" r="5.5" fill="{c}" opacity="0.85"/>'
            for i, c in enumerate((C["red"], C["yellow"], C["green"]))
        )
        title = (
            f'<text x="{width / 2:.1f}" y="24" fill="{C["grey1"]}" text-anchor="middle" '
            f'font-size="12">{esc(self.title)}</text>'
        )
        body = "\n".join(self.items)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
            f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="{FONT}" font-size="{FS}">'
            f'<rect x="0.5" y="0.5" width="{width - 1:.0f}" height="{height - 1:.0f}" rx="12" '
            f'fill="{self.bg}" stroke="{C["bg3"]}"/>{dots}{title}\n{body}</svg>'
        )

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, name), "w") as handle:
            handle.write(self.svg())


def box(term, row, col, width, height, color="grey0", title=""):
    if title:
        label = f" {title} "
        term.put(row, col, "╭─", color)
        term.put(row, col + 2, label, "grey1")
        term.put(row, col + 2 + len(label), "─" * (width - 4 - len(label)) + "╮", color)
    else:
        term.put(row, col, "╭" + "─" * (width - 2) + "╮", color)
    for r in range(1, height - 1):
        term.put(row + r, col, "│", color)
        term.put(row + r, col + width - 1, "│", color)
    term.put(row + height - 1, col, "╰" + "─" * (width - 2) + "╯", color)


# ---------------------------------------------------------------- palette
def build_palette():
    base16 = [
        ("base00", "bg0", "32302f", "editor background"),
        ("base01", "bg1", "3c3836", "terminal background"),
        ("base02", "bg3", "504945", "selection, active line"),
        ("base03", "grey0", "7c6f64", "comments, inactive"),
        ("base04", "grey1", "928374", "metadata, dates"),
        ("base05", "fg0", "d4be98", "base text"),
        ("base06", "fg1", "ddc7a1", "emphasis, active"),
        ("base07", "white", "f9f5d7", "rare flashes"),
        ("base08", "red", "ea6962", "types, errors"),
        ("base09", "orange", "e78a4e", "functions, focus"),
        ("base0A", "yellow", "d5a034", "docstrings, warnings"),
        ("base0B", "green", "98971a", "strings, success"),
        ("base0C", "sage", "89b482", "annotations"),
        ("base0D", "blue", "7daea3", "links only"),
        ("base0E", "purple", "d3869b", "constants, numbers"),
        ("base0F", "beige", "bdae93", "parameters"),
    ]
    extras = [
        ("extra", "orange_light", "f0a878", "macros (orange_light)"),
        ("extra", "grey2", "a89984", "punctuation"),
        ("extra", "magenta", "b27085", "ANSI magenta, merged"),
    ]
    ansi = [
        ("32302f", "black"), ("cc241d", "red"), ("98971a", "green"), ("d5a034", "yellow"),
        ("a89984", "blue → grey"), ("b27085", "magenta"), ("a89984", "cyan → grey"), ("d4be98", "white"),
        ("7c6f64", "bright black"), ("cc241d", "bright red"), ("98971a", "bright green"), ("d5a034", "bright yellow"),
        ("bdae93", "bright blue"), ("b27085", "bright magenta"), ("bdae93", "bright cyan"), ("ddc7a1", "bright white"),
    ]
    tw, th, gap, left = 178, 92, 12, 28
    width = left * 2 + 8 * tw + 7 * gap
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="620" viewBox="0 0 {width} 620" '
        f'font-family="{FONT}" font-size="13">',
        f'<rect width="{width}" height="620" rx="14" fill="{C["bg0"]}"/>',
    ]

    def tile(x, y, slot, name, hex_, role):
        light = sum(int(hex_[i:i + 2], 16) for i in (0, 2, 4)) > 380
        ink = C["bg0"] if light else C["fg0"]
        out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="10" fill="#{hex_}"/>')
        if hex_ in ("32302f", "3c3836"):
            out.append(f'<rect x="{x + .5}" y="{y + .5}" width="{tw - 1}" height="{th - 1}" rx="10" fill="none" stroke="{C["bg3"]}"/>')
        out.append(f'<text x="{x + 12}" y="{y + 24}" fill="{ink}" font-weight="bold">{slot} · {name}</text>')
        out.append(f'<text x="{x + 12}" y="{y + 46}" fill="{ink}">#{hex_}</text>')
        out.append(f'<text x="{x + 12}" y="{y + 72}" fill="{ink}" font-size="11" opacity="0.85">{esc(role)}</text>')

    def heading(y, text):
        out.append(f'<text x="{left}" y="{y}" fill="{C["fg1"]}" font-size="15" font-weight="bold">{text}</text>')

    heading(34, "Base16 slots")
    for i, (slot, name, hex_, role) in enumerate(base16):
        tile(left + (i % 8) * (tw + gap), 48 + (i // 8) * (th + gap), slot, name, hex_, role)
    heading(300, "Extra shades")
    for i, (slot, name, hex_, role) in enumerate(extras):
        tile(left + i * (tw + gap), 314, slot, name, hex_, role)
    heading(444, "Terminal ANSI 0–15")
    sw = 62
    for i, (hex_, role) in enumerate(ansi):
        x = left + (i % 8) * (tw + gap)
        y = 458 + (i // 8) * 70
        out.append(f'<rect x="{x}" y="{y}" width="{sw}" height="56" rx="8" fill="#{hex_}" stroke="{C["bg3"]}"/>')
        out.append(f'<text x="{x + sw + 10}" y="{y + 22}" fill="{C["fg0"]}" font-weight="bold">{i}</text>')
        out.append(f'<text x="{x + sw + 10}" y="{y + 42}" fill="{C["grey1"]}" font-size="11">{esc(role)}</text>')
    out.append("</svg>")
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "palette.svg"), "w") as handle:
        handle.write("\n".join(out))


# ---------------------------------------------------------------- roles
def build_roles():
    t = Term(72, 14, "syntax roles", "bg0")
    rows = [
        ("fg0", "variables, operators, keywords", "base text, no colour on purpose"),
        ("orange", "function_name()", "functions, methods"),
        ("orange_light", "println!()", "macros"),
        ("red", "ClassName", "types, classes"),
        ("green", '"string literal"', "strings"),
        ("yellow", '"""docstring"""', "docstrings, block comments"),
        ("grey0~", "# comment", "comments, hints"),
        ("purple", "42  3.14  CONSTANT", "constants, numbers"),
        ("beige", "parameter", "function parameters"),
        ("sage", "@decorator", "annotations"),
        ("grey2", "( ) , ; ::", "punctuation"),
        ("blue_", "https://example.com", "links - the only blue"),
    ]
    for i, (color, sample, role) in enumerate(rows):
        t.put(i + 1, 2, sample, color.rstrip("~_"), italic="~" in color, underline=color.endswith("_"))
        t.put(i + 1, 36, role, "grey1")
    t.save("roles.svg")


# ---------------------------------------------------------------- helix
def build_helix():
    t = Term(80, 27, "hx counter.rs", "bg0")
    rust = [
        "use std::collections::⟦red|HashMap⟧;",
        "",
        "⟦yellow|/// Counts how many times each word was seen.⟧",
        "pub struct ⟦red|Counter⟧ {",
        "    words: ⟦red|HashMap⟧<⟦red|String⟧, ⟦red|usize⟧>,",
        "}",
        "",
        "impl ⟦red|Counter⟧ {",
        "    pub fn ⟦orange|add⟧(&mut self, ⟦beige|word⟧: &⟦red|str⟧) {",
        "        ⟦grey0~|// ignore empty tokens⟧",
        "        if ⟦beige|word⟧.⟦orange|is_empty⟧() {",
        "            return;",
        "        }",
        "        *self.words.⟦orange|entry⟧(⟦beige|word⟧.⟦orange|to_string⟧()).⟦orange|or_insert⟧(⟦purple|0⟧) += ⟦purple|1⟧;",
        "        ⟦orange_light|println!⟧(⟦green|\"added {}\"⟧, ⟦beige|word⟧);",
        "    }",
        "}",
    ]
    python = [
        "⟦sage|@lru_cache⟧(maxsize=⟦purple|128⟧)",
        "def ⟦orange|load⟧(⟦beige|path⟧):",
        "    ⟦yellow|\"\"\"Read a file once and keep it in memory.\"\"\"⟧",
        "    with ⟦orange|open⟧(⟦beige|path⟧) as f:",
        "        return f.⟦orange|read⟧()",
    ]
    for i, text in enumerate(rust):
        number = str(i + 1).rjust(3)
        if i == 13:
            t.fill(i + 1, 0, 80, "bg3")
            t.put(i + 1, 0, number, "fg1", bold=True)
        else:
            t.put(i + 1, 0, number, "grey2")
        t.line(i + 1, 5, text, bg="bg3" if i == 13 else None)
    t.put(14, 66, " ", bg="fg0")
    base = len(rust) + 2
    t.put(base - 1, 5, "─" * 70, "bg3")
    for i, text in enumerate(python):
        t.put(base + i, 0, str(i + 1).rjust(3), "grey2")
        t.line(base + i, 5, text)
    sr = 25
    t.fill(sr, 0, 80, "bg1")
    t.put(sr, 1, " NOR ", "fg1", "bg3", bold=True)
    t.put(sr, 7, "counter.rs", "fg0", "bg1")
    t.put(sr, 18, "[+]", "yellow", "bg1")
    t.put(sr, 50, "1 W", "yellow", "bg1")
    t.put(sr, 55, "74%", "fg0", "bg1")
    t.put(sr, 60, "14:9", "fg0", "bg1")
    t.put(sr, 66, "utf-8", "grey1", "bg1")
    t.put(sr, 73, "main", "fg0", "bg1")
    t.save("helix.svg")


# ---------------------------------------------------------------- ansi -> term (bat)
def parse_ansi(text):
    text = re.sub(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)", "", text)
    text = re.sub(r"\x1b\[[0-9;?]*[A-Za-ln-z]", "", text)
    lines, state = [], {"fg": None, "bg": None, "bold": False, "italic": False, "underline": False}
    for raw in text.splitlines():
        spans, pos = [], 0
        for m in re.finditer(r"\x1b\[([0-9;]*)m", raw):
            if m.start() > pos:
                spans.append((raw[pos:m.start()], dict(state)))
            codes = [int(c) if c else 0 for c in m.group(1).split(";")]
            i = 0
            while i < len(codes):
                code = codes[i]
                if code == 0:
                    state.update(fg=None, bg=None, bold=False, italic=False, underline=False)
                elif code == 1:
                    state["bold"] = True
                elif code == 3:
                    state["italic"] = True
                elif code == 4:
                    state["underline"] = True
                elif code in (22, 23, 24):
                    state[{22: "bold", 23: "italic", 24: "underline"}[code]] = False
                elif code in (38, 48) and codes[i + 1:i + 2] == [2]:
                    rgb = "#%02x%02x%02x" % tuple(codes[i + 2:i + 5])
                    state["fg" if code == 38 else "bg"] = rgb
                    i += 4
                elif code == 39:
                    state["fg"] = None
                elif code == 49:
                    state["bg"] = None
                i += 1
            pos = m.end()
        if pos < len(raw):
            spans.append((raw[pos:], dict(state)))
        lines.append(spans)
    return lines


def put_ansi(term, row, col, spans):
    pos = col
    for text, st in spans:
        term.put(row, pos, text, st["fg"] or "fg0", st["bg"], st["bold"], st["italic"], st["underline"])
        pos += len(text)


SAMPLE_PY = '''from functools import lru_cache


class Config:
    """Runtime settings loaded once."""

    retries = 3

    @lru_cache(maxsize=None)
    def load(self, path):
        # read the file only on the first call
        with open(path) as handle:
            return handle.read()
'''


def build_bat():
    with tempfile.TemporaryDirectory() as workdir:
        with open(os.path.join(workdir, "config.py"), "w") as handle:
            handle.write(SAMPLE_PY)
        env = dict(os.environ, COLORTERM="truecolor")
        out = subprocess.run(
            ["bat", "--color=always", "--paging=never", "--decorations=always", "--style=numbers,header",
             "--theme=gruvbox-material-alabaster", "config.py"],
            capture_output=True, text=True, env=env, check=True, cwd=workdir,
        ).stdout
    lines = parse_ansi(out)
    t = Term(64, len(lines) + 2, "bat config.py", "bg1")
    for i, spans in enumerate(lines):
        put_ansi(t, i + 1, 1, spans)
    t.save("bat.svg")


# ---------------------------------------------------------------- fzf-tab
def build_fzf():
    t = Term(86, 19, "zsh - fzf-tab", "bg1")
    t.line(1, 1, "⟦green!|.dotfiles⟧ ⟦grey1|~/.dotfiles⟧ ⟦yellow|git:(⟧⟦red|main⟧⟦yellow|)⟧ ⟦fg0!|×⟧", punct=False)
    t.line(2, 1, "⟦green!|>⟧ bat .config/⟦grey1|he⟧", punct=False)
    box(t, 4, 3, 34, 13, "grey0")
    items = ["helix/config.toml", "helix/languages.toml", "herdr/config.toml", "hunk/config.toml",
             "ghostty/config", "kanata/config.kbd", "atuin/config.toml", "bat/config", "yazi/yazi.toml"]
    t.put(5, 5, "> he", "green")
    t.put(5, 28, "9/42", "green")
    for i, item in enumerate(items[:4]):
        r = 7 + i
        selected = i == 0
        head, tail = item[:2], item[2:]
        if selected:
            t.fill(r, 4, 32, "bg3")
            t.put(r, 5, ">", "ansi_red", "bg3", bold=True)
            t.put(r, 7, head, "green", "bg3", bold=True)
            t.put(r, 9, tail, "fg1", "bg3", bold=True)
        else:
            t.put(r, 7, head, "green")
            t.put(r, 9, tail, "fg0")
    box(t, 4, 40, 44, 13, "grey0")
    t.put(5, 42, "config.toml", "grey1")
    preview = [
        'theme = ⟦green|"alabaster_gruvbox_material"⟧',
        "",
        "⟦fg0!|[editor]⟧",
        'line-number = ⟦green|"relative"⟧',
        "scrolloff = ⟦purple|10⟧",
        "mouse = ⟦purple|true⟧",
        "",
        "⟦fg0!|[editor.cursor-shape]⟧",
        'insert = ⟦green|"bar"⟧',
        'normal = ⟦green|"block"⟧',
    ]
    for i, text in enumerate(preview):
        t.put(6 + i, 42, str(i + 1).rjust(2), "grey2")
        t.line(6 + i, 46, text)
    t.save("fzf-tab.svg")


# ---------------------------------------------------------------- atuin
def build_atuin():
    t = Term(86, 16, "zsh - atuin (Ctrl-R)", "bg1")
    rows = [
        ("2d ago", "0.4s", "uv run pytest -x"),
        ("1d ago", "1.2s", "git rebase origin/main"),
        ("5h ago", "0.1s", "rg \"def load\" backend/"),
        ("2h ago", "12s", "docker compose up -d db"),
        ("41m ago", "0.2s", "hx .config/kanata/config.kbd"),
        ("12m ago", "3.1s", "uv run ruff check ."),
        ("3m ago", "0.7s", "uv run pytest -k reviews"),
    ]
    for i, (when, dur, cmd) in enumerate(rows):
        r = 1 + i
        selected = i == len(rows) - 1
        if selected:
            t.fill(r, 1, 82, "bg3")
            t.put(r, 2, ">", "green", "bg3", bold=True)
        t.put(r, 4, when.rjust(8), "grey1", "bg3" if selected else None)
        t.put(r, 14, dur.rjust(5), "yellow", "bg3" if selected else None)
        t.put(r, 22, cmd, "green" if selected else "fg0", "bg3" if selected else None, bold=selected)
    t.put(9, 1, "─" * 82, "grey0")
    t.line(10, 2, "⟦grey1|directory⟧  ⟦fg0|~/Rocketdata/backend⟧", punct=False)
    t.line(11, 2, "⟦grey1|exit code⟧  ⟦green|0⟧   ⟦grey1|host⟧  ⟦fg0|mac⟧", punct=False)
    t.line(13, 2, "⟦green|>⟧ ⟦fg1|pytest⟧", punct=False)
    t.put(14, 2, "enter run - tab edit - ctrl-r filter: host", "grey0")
    t.put(13, 76, "7/1840", "grey0")
    t.save("atuin.svg")


# ---------------------------------------------------------------- herdr
def build_herdr():
    t = Term(92, 24, "herdr", "bg1")
    # left pane: active
    box(t, 1, 1, 46, 22, "fg0", "claude")
    t.line(3, 3, "⟦fg1!|Refactor review fetcher⟧", punct=False)
    t.line(5, 3, "⟦green|+⟧ ⟦fg0|read services.py⟧", punct=False)
    t.line(6, 3, "⟦green|+⟧ ⟦fg0|add regression test⟧", punct=False)
    t.line(7, 3, "⟦yellow|~⟧ ⟦fg0|running pytest...⟧", punct=False)
    t.line(9, 3, "⟦grey0|focus: working⟧", punct=False)
    t.put(21, 3, "> ", "green")
    t.put(21, 5, " ", bg="fg0")
    # right top: inactive
    box(t, 1, 48, 43, 11, "grey0", "shell")
    t.line(3, 50, "⟦grey1|~/Rocketdata⟧ ⟦yellow|git:(⟧⟦red|TS-6135⟧⟦yellow|)⟧", punct=False)
    t.line(4, 50, "⟦green|>⟧ ⟦fg0|git status -sb⟧", punct=False)
    t.line(5, 50, "⟦grey0|## TS-6135...origin/TS-6135⟧", punct=False)
    t.line(6, 50, "⟦yellow| M⟧ ⟦fg0|backend/app/flamp/models.py⟧", punct=False)
    t.line(7, 50, "⟦green|A ⟧ ⟦fg0|backend/tests/test_flamp.py⟧", punct=False)
    # right bottom: inactive
    box(t, 12, 48, 43, 11, "grey0", "logs")
    t.line(14, 50, "⟦grey1|12:04:11⟧ ⟦green|INFO ⟧ ⟦fg0|collector started⟧", punct=False)
    t.line(15, 50, "⟦grey1|12:04:13⟧ ⟦yellow|WARN ⟧ ⟦fg0|retry yandex page 3⟧", punct=False)
    t.line(16, 50, "⟦grey1|12:04:19⟧ ⟦ansi_red|ERROR⟧ ⟦fg0|timeout after 10s⟧", punct=False)
    t.save("herdr.svg")


# ---------------------------------------------------------------- diff (hunk)
def build_diff():
    t = Term(84, 15, "hunk - services.py", "bg0")
    t.put(1, 1, "backend/app/reviews/services.py", "fg1", bold=True)
    head = "        return Review.objects.filter(brand_id=brand_id, "
    rows = [
        ("ctx", 41, 41, [("    def find_existing(self, brand_id, origin_id):", False)]),
        ("del", 42, None, [(head, False), ("company_id=None", True), (")", False)]),
        ("add", None, 42, [(head, False), ("origin_id=origin_id", True), (")", False)]),
        ("ctx", 43, 43, []),
        ("ctx", 44, 44, [("    def save(self, payload):", False)]),
        ("del", 45, None, [("        review = self.find_existing(payload.brand_id)", False)]),
        ("add", None, 45, [("        review = self.find_existing(payload.brand_id", False),
                           (", payload.origin_id", True), (")", False)]),
        ("ctx", 46, 46, [("        if review is None:", False)]),
        ("ctx", 47, 47, [("            review = Review(**payload.fields)", False)]),
    ]
    for i, (kind, old, new, segments) in enumerate(rows):
        r = 3 + i
        bg = {"add": "diff_add", "del": "diff_del", "ctx": None}[kind]
        word_bg = {"add": "diff_add_word", "del": "diff_del_word", "ctx": None}[kind]
        if bg:
            t.fill(r, 0, 84, bg)
        t.put(r, 1, (str(old) if old else "").rjust(3), "grey1", bg)
        t.put(r, 5, (str(new) if new else "").rjust(3), "grey1", bg)
        sign = {"add": "+", "del": "-", "ctx": " "}[kind]
        t.put(r, 9, sign, {"add": "green", "del": "red", "ctx": "fg0"}[kind], bg, bold=True)
        pos = 11
        for text, changed in segments:
            t.put(r, pos, text, "fg0", word_bg if changed else bg)
            pos += len(text)
    t.save("diff.svg")


if __name__ == "__main__":
    build_palette()
    build_roles()
    build_helix()
    build_bat()
    build_fzf()
    build_atuin()
    build_herdr()
    build_diff()
    print("ok:", sorted(os.listdir(OUT)))
