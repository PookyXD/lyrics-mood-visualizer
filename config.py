# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   LYRICS MOOD VISUALIZER CONFIG
#   Change anything here — it updates the whole visual
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Background ──
BG_COLOR        = "#050505"   # main background color

# ── Stars ──
STAR_COLOR      = "#FFD700"   # color of constellation stars
STAR_MIN_SIZE   = 30          # smallest star (neutral lines)
STAR_MAX_SIZE   = 400         # biggest star (most emotional lines)
BG_STAR_COUNT   = 1000         # how many background stars (keep under 200)
BG_STAR_MAX_SIZE = 1.8        # max size of background stars

# ── Connecting Line ──
LINE_COLOR      = "#AAAACC"   # moon colored line between stars
LINE_WIDTH      = 1.1         # thickness of the line
LINE_ALPHA      = 0.45        # transparency (0.0 invisible → 1.0 solid)

# ── Tick Bars ──
TICK_HEIGHT     = 0.1       # how tall the little bars between stars are
TICK_WIDTH      = 1.0         # thickness of tick bars
TICK_ALPHA      = 0.3         # transparency of tick bars

# ── Score Display ──
SCORE_COLOR_POS = "#FFD700"   # color when song is positive
SCORE_COLOR_NEG = "#FFD700"   # color when song is negative

# ── Typography ──
TITLE_SIZE      = 22          # song title font size
ARTIST_SIZE     = 20          # artist name font size
SCORE_SIZE      = 30          # big score number font size
QUOTE_SIZE      = 30          # quoted lyric font size

# ── Labels ──
LABEL_COLOR     = "#DEDEDE"   # color for small labels like "Lyric Lines" and "most emotional line"
AXIS_COLOR      = "#CFCFCF"   # color for axis tick numbers
LABEL_SIZE = 19   # size of small labels like "most emotional line"

# ── Canvas ──
FIGURE_WIDTH    = 24          # width of the output image
FIGURE_HEIGHT   = 14          # height of the output image
OUTPUT_DPI      = 180         # quality of saved PNG (150 normal, 300 print)