import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.gridspec import GridSpec
import numpy as np
import os
from config import (
    BG_COLOR, STAR_COLOR, STAR_MIN_SIZE, STAR_MAX_SIZE,
    BG_STAR_COUNT, BG_STAR_MAX_SIZE,
    LINE_COLOR, LINE_WIDTH, LINE_ALPHA,
    TICK_HEIGHT, TICK_WIDTH, TICK_ALPHA,
    SCORE_COLOR_POS, SCORE_COLOR_NEG,
    TITLE_SIZE, ARTIST_SIZE, SCORE_SIZE, QUOTE_SIZE,
    FIGURE_WIDTH, FIGURE_HEIGHT, OUTPUT_DPI,
    LABEL_COLOR, AXIS_COLOR
)

BG       = BG_COLOR
GOLD     = STAR_COLOR
MOONLINE = LINE_COLOR


def plot_mood_arc(song, art_path=None):
    compounds = [line.compound for line in song.lines]
    texts     = [line.text     for line in song.lines]
    x         = np.array(range(len(compounds)))
    y         = np.array(compounds)

    intensity  = np.abs(y)
    star_sizes = STAR_MIN_SIZE + (intensity ** 1.5) * (STAR_MAX_SIZE - STAR_MIN_SIZE)

    total_score = float(np.mean(y))

    if total_score >= 0:
        hi_idx = int(np.argmax(y))
    else:
        hi_idx = int(np.argmin(y))
    highlight = texts[hi_idx]
    if len(highlight) > 80:
        highlight = highlight[:77] + "..."

    # ── canvas ──
    fig = plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    fig.patch.set_facecolor(BG)

    gs = GridSpec(
        3, 1, figure=fig,
        height_ratios=[2.8, 6, 2.2],
        hspace=0.45,
        left=0.06, right=0.97,
        top=0.97,  bottom=0.04,
    )

    ax_header = fig.add_subplot(gs[0])
    ax_main   = fig.add_subplot(gs[1])
    ax_footer = fig.add_subplot(gs[2])

    for ax in [ax_header, ax_footer]:
        ax.set_facecolor(BG)
        ax.axis("off")
    ax_main.set_facecolor(BG)

    # ════════════════════════════════
    # HEADER
    # ════════════════════════════════

    # big album art — left anchored
    if art_path and os.path.exists(art_path):
        from PIL import Image
        art = Image.open(art_path).convert("RGBA").resize((200, 200))

        frame_path = "assets/frame.png"
        if os.path.exists(frame_path):
            frame    = Image.open(frame_path).convert("RGBA").resize((240, 240))
            combined = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
            combined.paste(art,   (20, 20))
            combined.paste(frame, (0,  0), frame)
            display_img = combined
        else:
            display_img = art

        imagebox = OffsetImage(np.array(display_img), zoom=0.95)
        ab = AnnotationBbox(
            imagebox, (0.0, 0.5),
            xycoords='axes fraction',
            box_alignment=(0, 0.5),
            frameon=False,
        )
        ax_header.add_artist(ab)

    # title and artist sitting to the right of the big art
    ax_header.text(
        0.22, 0.72, song.title,
        transform=ax_header.transAxes,
        color='white', fontsize=TITLE_SIZE,
        fontweight='bold', va='center',
        path_effects=[pe.withStroke(linewidth=4, foreground=BG)]
    )
    ax_header.text(
        0.22, 0.38, song.artist,
        transform=ax_header.transAxes,
        color='#888888', fontsize=ARTIST_SIZE,
        style='italic', va='center'
    )

    # emotional score — right side
    score_color = SCORE_COLOR_POS if total_score >= 0 else SCORE_COLOR_NEG

    ax_header.text(
        0.98, 0.82, "Emotional Score",
        transform=ax_header.transAxes,
        color='#888888', fontsize=11,
        ha='right', va='center'
    )
    ax_header.text(
        0.98, 0.40, f"{total_score:+.3f}",
        transform=ax_header.transAxes,
        color=score_color, fontsize=SCORE_SIZE,
        fontweight='bold', ha='right', va='center',
        path_effects=[pe.withStroke(linewidth=6, foreground=BG)]
    )

    # emotional scale bar
    scale_ax = fig.add_axes([0.22, 0.845, 0.52, 0.018])
    scale_ax.set_facecolor(BG)
    for spine in scale_ax.spines.values():
        spine.set_edgecolor("#2A2A2A")
    scale_ax.tick_params(
        left=False, labelleft=False,
        colors="#AAAAAA", labelsize=8.5, length=4
    )

    grad = np.linspace(0, 1, 300).reshape(1, -1)
    scale_ax.imshow(grad, aspect='auto',
                    extent=[-1, 1, 0, 1],
                    cmap='YlOrBr', alpha=0.7)
    scale_ax.set_xlim(-1, 1)
    scale_ax.set_ylim(0,  1)
    scale_ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    scale_ax.set_xticklabels(
        ["-1.0", "-0.5", "0", "+0.5", "+1.0"],
        color="#DDDDDD", fontsize=8.5
    )
    scale_ax.plot(
        total_score, 0.5, '*',
        color=score_color, markersize=16, zorder=5,
        path_effects=[pe.withStroke(linewidth=2, foreground='white')]
    )

    # ════════════════════════════════
    # MAIN — constellation
    # ════════════════════════════════

    rng = np.random.default_rng(7)
    n   = BG_STAR_COUNT
    bsx = rng.uniform(0, 1, n)
    bsy = rng.uniform(0, 1, n)
    bss = rng.uniform(0.3, BG_STAR_MAX_SIZE, n)
    bsa = rng.uniform(0.08, 0.5, n)
    for bx, by, bs, ba in zip(bsx, bsy, bss, bsa):
        ax_main.plot(bx, by, '*', color='white',
                     markersize=bs, alpha=ba,
                     transform=ax_main.transAxes, zorder=1)

    # connecting line
    ax_main.plot(x, y,
                 color=MOONLINE, linewidth=LINE_WIDTH,
                 alpha=LINE_ALPHA, zorder=3,
                 solid_capstyle='round')

    # tick bars
    for i in range(len(x)):
        ax_main.plot(
            [x[i], x[i]],
            [y[i] - TICK_HEIGHT, y[i] + TICK_HEIGHT],
            color=MOONLINE, linewidth=TICK_WIDTH,
            alpha=TICK_ALPHA, zorder=3
        )

    # stars
    for i in range(len(x)):
        s = star_sizes[i]
        ax_main.scatter(x[i], y[i], s=s * 6,
                        color=GOLD, alpha=0.03,
                        marker='*', linewidths=0, zorder=4)
        ax_main.scatter(x[i], y[i], s=s * 3,
                        color=GOLD, alpha=0.07,
                        marker='*', linewidths=0, zorder=5)
        ax_main.scatter(x[i], y[i], s=s * 1.5,
                        color=GOLD, alpha=0.15,
                        marker='*', linewidths=0, zorder=6)
        ax_main.scatter(x[i], y[i], s=s,
                        color=GOLD, alpha=0.92,
                        marker='*', linewidths=0, zorder=7)
        ax_main.scatter(x[i], y[i], s=max(s * 0.08, 6),
                        color='white', alpha=0.85,
                        marker='*', linewidths=0, zorder=8)

    # zero baseline
    ax_main.axhline(y=0, color='white', linewidth=0.5,
                    alpha=0.12, linestyle='--', zorder=2)

    ax_main.set_xlim(-1, len(x) + 1)
    ax_main.set_ylim(-1.3, 1.3)
    ax_main.set_xlabel(
        "Lyric Lines  →",
        color=LABEL_COLOR, fontsize=10, labelpad=10
    )
    ax_main.set_ylabel(
        "← negative  |  positive →",
        color=LABEL_COLOR, fontsize=9, labelpad=10
    )
    ax_main.tick_params(colors=AXIS_COLOR, labelsize=7)
    ax_main.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax_main.set_yticklabels(
        ["-1.0", "-0.5", "0", "+0.5", "+1.0"],
        color=AXIS_COLOR, fontsize=7
    )
    ax_main.yaxis.grid(True, color="#0F0F0F", linewidth=0.6, zorder=0)
    ax_main.xaxis.grid(True, color="#0F0F0F", linewidth=0.4, zorder=0)
    ax_main.set_axisbelow(True)
    for spine in ax_main.spines.values():
        spine.set_edgecolor("#1A1A1A")

    # ════════════════════════════════
    # FOOTER — highlighted lyric
    # ════════════════════════════════

    ax_footer.text(
        0.5, 0.75,
        "most emotional line",
        ha='center', va='center',
        transform=ax_footer.transAxes,
        color=LABEL_COLOR, fontsize=9, style='italic'
    )
    ax_footer.text(
        0.5, 0.28,
        f'★   "{highlight}"',
        ha='center', va='center',
        transform=ax_footer.transAxes,
        color=score_color, fontsize=QUOTE_SIZE,
        style='italic', alpha=0.85,
        path_effects=[pe.withStroke(linewidth=3, foreground=BG)]
    )

    # ── save ──
    os.makedirs("output", exist_ok=True)
    filename = (
        f"output/{song.title}_{song.artist}_constellation.png"
        .replace(" ", "_")
    )
    plt.savefig(filename, dpi=OUTPUT_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close()

    print(f"\nConstellation saved to {filename}")
    return filename