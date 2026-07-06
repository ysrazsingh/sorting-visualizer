WIDTH, HEIGHT = 1000, 560
NUM_BARS      = 80
MAX_VAL       = 280

# menu height scales with number of algorithms (set by engine at runtime)
# these are the defaults for the full 10-algo layout (2 rows × 45 px)
MENU_H = 90
VIZ_H  = HEIGHT - MENU_H   # 470

BG            = (10,  12,  16)
BAR_COLOR     = (239, 71,  111)
COMPARE_CLR   = (255, 209, 102)   # yellow  – comparing
SWAP_CLR      = (6,   214, 160)   # teal    – swapping
OVERWRITE_CLR = (17,  138, 178)   # blue    – single-cell write
DONE_CLR      = (100, 200, 120)   # green   – finished
MENU_BG       = (16,  18,  24)
DIVIDER       = (38,  42,  54)
TEXT_DIM      = (110, 115, 135)
TEXT_BRIGHT   = (220, 225, 235)
ACTIVE_BG     = (45,  15,  25)
ACTIVE_BORDER = (239, 71,  111)

SPEED_LEVELS = [2, 4, 8, 16, 32, 64, 128]

# ── colour themes  (index 0 = default, 1 = B&W) ──────────────────────────────
THEMES = [
    {   # 0 – Color
        "bar":       (239, 71,  111),
        "compare":   (255, 209, 102),
        "swap":      (6,   214, 160),
        "overwrite": (17,  138, 178),
        "done":      (100, 200, 120),
    },
    {   # 1 – Black & White
        "bar":       (155, 155, 155),
        "compare":   (215, 215, 215),
        "swap":      (255, 255, 255),
        "overwrite": (190, 190, 190),
        "done":      (255, 255, 255),
    },
]
THEME_NAMES = ["Color", "B&W"]
