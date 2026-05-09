from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from contextlib import contextmanager
from cli_config import (
    APP_NAME, APP_TAGLINE,
    APP_NAME_COLOR, APP_TAGLINE_COLOR,
    HEADER_BORDER, DIVIDER_COLOR, HEADER_WIDTH,
    SPINNER_STYLE, SPINNER_COLOR, SPINNER_FETCH,
    SPINNER_ANALYZE, SPINNER_VISUAL,
    TABLE_BORDER, TABLE_HEADER_COLOR, TABLE_TITLE,
    COL_LINE_COLOR, COL_SECTION_COLOR, COL_SCORE_WIDTH,
    POSITIVE_COLOR, NEGATIVE_COLOR, NEUTRAL_COLOR,
    PANEL_BORDER, PANEL_TITLE, PANEL_TITLE_COLOR,
    PANEL_LABEL_COLOR, PANEL_VALUE_COLOR,
    PANEL_SCORE_POS, PANEL_SCORE_NEG, PANEL_QUOTE_COLOR
)

console = Console()


def print_header():
    title = Text()
    title.append("★  ", style=f"bold {APP_NAME_COLOR}")
    title.append(APP_NAME, style=f"bold {APP_NAME_COLOR}")
    title.append("  ★", style=f"bold {APP_NAME_COLOR}")

    tagline = Text(APP_TAGLINE, style=f"italic {APP_TAGLINE_COLOR}", justify="center")

    content = Text()
    content.append_text(title)
    content.append("\n")
    content.append_text(tagline)

    console.print(Panel(
        content,
        border_style=HEADER_BORDER,
        padding=(1, 4),
        width = HEADER_WIDTH,
    ))


def print_divider():
    console.print(Rule(style=DIVIDER_COLOR))

@contextmanager
def fetch_spinner():
    with console.status(
        f"[{SPINNER_COLOR}]{SPINNER_FETCH}[/]",
        spinner=SPINNER_STYLE,
        spinner_style=SPINNER_COLOR
    ):
        yield


@contextmanager
def analyze_spinner():
    with console.status(
        f"[{SPINNER_COLOR}]{SPINNER_ANALYZE}[/]",
        spinner=SPINNER_STYLE,
        spinner_style=SPINNER_COLOR
    ):
        yield


@contextmanager
def visual_spinner():
    with console.status(
        f"[{SPINNER_COLOR}]{SPINNER_VISUAL}[/]",
        spinner=SPINNER_STYLE,
        spinner_style=SPINNER_COLOR
    ):
        yield

def print_table(song):
    table = Table(
        title=TABLE_TITLE,
        border_style=TABLE_BORDER,
        header_style=f"bold {TABLE_HEADER_COLOR}",
        show_lines=False,
        padding=(0, 1),
    )

    table.add_column("Line", style=COL_LINE_COLOR,
                     no_wrap=False, ratio=6)
    table.add_column("Section", style=COL_SECTION_COLOR,
                     no_wrap=True, ratio=2)
    table.add_column("Score", no_wrap=True,
                     width=COL_SCORE_WIDTH, justify="right")

    for lyric_line in song.lines:
        score = lyric_line.compound

        if score > 0:
            score_str = f"[{POSITIVE_COLOR}]+{score:.3f}[/]"
        elif score < 0:
            score_str = f"[{NEGATIVE_COLOR}]{score:.3f}[/]"
        else:
            score_str = f"[{NEUTRAL_COLOR}]{score:.3f}[/]"

        table.add_row(
            lyric_line.text[:60],
            lyric_line.section,
            score_str,
        )

    console.print(table)

def print_summary(song):
    total_score = sum(l.compound for l in song.lines) / len(song.lines)
    score_color = PANEL_SCORE_POS if total_score >= 0 else PANEL_SCORE_NEG

    if total_score >= 0:
        highlight = max(song.lines, key=lambda l: l.compound)
    else:
        highlight = min(song.lines, key=lambda l: l.compound)

    content = Text()

    content.append("  Song      ", style=f"bold {PANEL_LABEL_COLOR}")
    content.append(f"{song.title}\n", style=f"bold {PANEL_VALUE_COLOR}")

    content.append("  Artist    ", style=f"bold {PANEL_LABEL_COLOR}")
    content.append(f"{song.artist}\n", style=PANEL_VALUE_COLOR)

    content.append("  Lines     ", style=f"bold {PANEL_LABEL_COLOR}")
    content.append(f"{len(song.lines)} analyzed\n", style=PANEL_VALUE_COLOR)

    content.append("  Score     ", style=f"bold {PANEL_LABEL_COLOR}")
    content.append(f"{total_score:+.3f}\n", style=f"bold {score_color}")

    content.append("\n")

    content.append("  ★  ", style=f"bold {PANEL_QUOTE_COLOR}")
    content.append(f'"{highlight.text[:70]}"',
                   style=f"italic {PANEL_QUOTE_COLOR}")

    console.print(Panel(
        content,
        title=f"[bold {PANEL_TITLE_COLOR}]{PANEL_TITLE}[/]",
        border_style=PANEL_BORDER,
        padding=(1, 2),
    ))