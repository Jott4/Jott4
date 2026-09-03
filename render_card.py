"""Gera dark_mode.svg e light_mode.svg a partir de ascii_art.txt e do painel abaixo.

Rode `python render_card.py` sempre que mudar o texto do painel ou a arte ASCII.
Os valores dinamicos (Uptime, repos, stars, commits, seguidores, linhas de codigo)
sao preenchidos depois pelo today.py, que roda no GitHub Actions.
"""

from html import escape

ASCII_FILE = "ascii_art.txt"

TITLE = "joao@arvore"
VALUE_COL = 24
LINE_WIDTH = 54

PANEL = [
    ("section", "Sistema"),
    ("static", "SO", "macOS, iOS, Linux"),
    ("dynamic", "Uptime", "age_data", "24 anos, 0 meses, 0 dias"),
    ("static", "Host", "Árvore Educação"),
    ("static", "Kernel", "Engenheiro de Software"),
    ("static", "IDE", "Claude Code, VSCode"),
    ("section", "Linguagens"),
    ("static", "Programação", "TypeScript, Python, JavaScript"),
    ("static", "Computador", "HTML, CSS, SQL, JSON, YAML"),
    ("static", "Reais", "Português, Inglês"),
    ("section", "Interesses"),
    ("static", "Software", "Agentes de IA, automação, LLMs"),
    ("section", "Contato"),
    ("static", "Email.Pessoal", "jvgcunha2002@gmail.com"),
    ("static", "LinkedIn", "Jott4"),
    ("static", "X", "jvgcunha"),
    ("static", "Local", "Londrina, Brasil"),
    ("section", "Estatísticas do GitHub"),
    ("stats_repos", None),
    ("stats_commits", None),
    ("stats_loc", None),
]

THEMES = {
    "dark_mode.svg": {
        "bg": "#161b22",
        "fg": "#c9d1d9",
        "key": "#ffa657",
        "value": "#a5d6ff",
        "add": "#3fb950",
        "delete": "#f85149",
        "dots": "#616e7f",
    },
    "light_mode.svg": {
        "bg": "#ffffff",
        "fg": "#24292f",
        "key": "#953800",
        "value": "#0a3069",
        "add": "#1a7f37",
        "delete": "#cf222e",
        "dots": "#57606a",
    },
}

ASCII_X, ASCII_Y0, ASCII_SIZE, ASCII_STEP = 16, 44, 13, 16
PANEL_X, PANEL_Y0, PANEL_SIZE, PANEL_STEP = 474, 36, 16, 20
WIDTH, HEIGHT = 1060, 500


def dots(label):
    filler = VALUE_COL - 3 - len(label)
    return " " + "." * max(1, filler) + " "


def rule(prefix_len):
    return "-" * max(1, LINE_WIDTH - prefix_len)


def key(text):
    return f'<tspan class="key">{escape(text)}</tspan>'


def value(text, element_id=None):
    ident = f' id="{element_id}"' if element_id else ""
    return f'<tspan class="value"{ident}>{escape(text)}</tspan>'


def filler(text, element_id=None):
    ident = f' id="{element_id}"' if element_id else ""
    return f'<tspan class="cc"{ident}>{escape(text)}</tspan>'


def panel_lines():
    lines = [
        f'<tspan x="{PANEL_X}" y="{PANEL_Y0}">{escape(TITLE)}</tspan> {rule(len(TITLE) + 1)}'
    ]
    y = PANEL_Y0
    for row in PANEL:
        y += PANEL_STEP
        head = f'<tspan x="{PANEL_X}" y="{y}"'
        kind = row[0]
        if kind == "section":
            label = f"- {row[1]}"
            lines.append(f"{head}>{escape(label)}</tspan> {rule(len(label) + 1)}")
        elif kind == "static":
            _, label, val = row
            lines.append(
                f'{head} class="cc">. </tspan>{key(label)}:'
                f"{filler(dots(label))}{value(val)}"
            )
        elif kind == "dynamic":
            _, label, element_id, placeholder = row
            lines.append(
                f'{head} class="cc">. </tspan>{key(label)}:'
                f"{filler(dots(label), element_id + '_dots')}"
                f"{value(placeholder, element_id)}"
            )
        elif kind == "stats_repos":
            lines.append(
                f'{head} class="cc">. </tspan>{key("Repos")}:'
                f'{filler(" .... ", "repo_data_dots")}{value("0", "repo_data")}'
                f' {{{key("Contribuições")}: {value("0", "contrib_data")}}} | '
                f'{key("Estrelas")}:{filler(" ........ ", "star_data_dots")}'
                f'{value("0", "star_data")}'
            )
        elif kind == "stats_commits":
            lines.append(
                f'{head} class="cc">. </tspan>{key("Commits")}:'
                f'{filler(" ................ ", "commit_data_dots")}'
                f'{value("0", "commit_data")} | {key("Seguidores")}:'
                f'{filler(" ....... ", "follower_data_dots")}'
                f'{value("0", "follower_data")}'
            )
        elif kind == "stats_loc":
            label = "Linhas de código"
            lines.append(
                f'{head} class="cc">. </tspan>{key(label)}:'
                f'{filler(". ", "loc_data_dots")}{value("0", "loc_data")}'
                f' ( <tspan class="addColor" id="loc_add">0</tspan>'
                f'<tspan class="addColor">++</tspan>, '
                f'<tspan id="loc_del_dots"> </tspan>'
                f'<tspan class="delColor" id="loc_del">0</tspan>'
                f'<tspan class="delColor">--</tspan> )'
            )
    return lines


def ascii_lines():
    with open(ASCII_FILE, encoding="utf-8") as handle:
        art = handle.read().rstrip("\n").split("\n")
    return [
        f'<tspan x="{ASCII_X}" y="{ASCII_Y0 + index * ASCII_STEP}">'
        f"{escape(line)}</tspan>"
        for index, line in enumerate(art)
    ]


def build(theme):
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{WIDTH}px" height="{HEIGHT}px" font-size="{PANEL_SIZE}px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
size-adjust: 109%;
}}
.key {{fill: {theme['key']};}}
.value {{fill: {theme['value']};}}
.addColor {{fill: {theme['add']};}}
.delColor {{fill: {theme['delete']};}}
.cc {{fill: {theme['dots']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{WIDTH}px" height="{HEIGHT}px" fill="{theme['bg']}" rx="15"/>
<text x="{ASCII_X}" y="{ASCII_Y0}" fill="{theme['fg']}" font-size="{ASCII_SIZE}px">
{chr(10).join(ascii_lines())}
</text>
<text x="{PANEL_X}" y="{PANEL_Y0}" fill="{theme['fg']}">
{chr(10).join(panel_lines())}
</text>
</svg>
"""


if __name__ == "__main__":
    for filename, theme in THEMES.items():
        with open(filename, "w", encoding="utf-8") as handle:
            handle.write(build(theme))
        print("gerado:", filename)
