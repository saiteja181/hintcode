"""
Generate Chrome Web Store promotional images for HintCode extension.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Color palette ──────────────────────────────────────────────
BG = "#1a1a2e"
PURPLE = "#7b2ff7"
PURPLE_LIGHT = "#a855f7"
PURPLE_DARK = "#4c1d95"
WHITE = "#ffffff"
GRAY_LIGHT = "#b0b0c0"
GRAY_MID = "#6b7280"
CARD_BG = "#16213e"
CARD_BG2 = "#0f3460"
YELLOW_HINT = "#f59e0b"
BLUE_HINT = "#3b82f6"
PURPLE_HINT = "#8b5cf6"

# ── Font helpers ───────────────────────────────────────────────
def get_font(size, bold=False):
    """Try Windows system fonts, fall back to default."""
    candidates = []
    if bold:
        candidates = ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf", "calibri.ttf"]

    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            pass
    # fallback
    try:
        return ImageFont.truetype("arial.ttf", size)
    except (OSError, IOError):
        return ImageFont.load_default()


def text_bbox(draw, text, font):
    """Return (width, height) of rendered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    r = radius
    # corners
    draw.pieslice([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=fill, outline=outline, width=width)
    # fill rectangles
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x0 + r, y1 - r], fill=fill)
    draw.rectangle([x1 - r, y0 + r, x1, y1 - r], fill=fill)
    if outline:
        draw.line([x0 + r, y0, x1 - r, y0], fill=outline, width=width)
        draw.line([x0 + r, y1, x1 - r, y1], fill=outline, width=width)
        draw.line([x0, y0 + r, x0, y1 - r], fill=outline, width=width)
        draw.line([x1, y0 + r, x1, y1 - r], fill=outline, width=width)


def draw_icon(draw, cx, cy, radius):
    """Draw the HintCode icon: purple circle with white lightbulb."""
    # Purple circle
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=PURPLE)
    # Lighter ring
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=PURPLE_LIGHT, width=max(2, radius // 15))

    # Lightbulb - simplified
    bulb_r = int(radius * 0.38)
    bulb_cy = cy - int(radius * 0.12)

    # Bulb circle (top part)
    draw.ellipse([cx - bulb_r, bulb_cy - bulb_r, cx + bulb_r, bulb_cy + bulb_r], fill=WHITE)

    # Bulb body going down
    neck_w = int(bulb_r * 0.55)
    neck_top = bulb_cy + int(bulb_r * 0.6)
    neck_bottom = bulb_cy + int(bulb_r * 1.6)
    draw.rectangle([cx - neck_w, neck_top, cx + neck_w, neck_bottom], fill=WHITE)

    # Base lines (filament base)
    base_w = int(neck_w * 0.8)
    for i in range(3):
        ly = neck_bottom + int(bulb_r * 0.15) + i * max(2, int(bulb_r * 0.14))
        draw.line([cx - base_w, ly, cx + base_w, ly], fill=PURPLE_DARK, width=max(1, radius // 20))

    # Tip at bottom
    tip_y = neck_bottom + int(bulb_r * 0.65)
    draw.polygon([(cx - base_w, neck_bottom + int(bulb_r * 0.12)),
                   (cx + base_w, neck_bottom + int(bulb_r * 0.12)),
                   (cx, tip_y)], fill=WHITE)

    # Rays around bulb
    ray_len = int(radius * 0.18)
    ray_start = int(radius * 0.55)
    for angle_deg in [30, 70, 110, 150, 210, 250, 290, 330]:
        a = math.radians(angle_deg)
        x1 = cx + int(ray_start * math.cos(a))
        y1 = bulb_cy + int(ray_start * math.sin(a))
        x2 = cx + int((ray_start + ray_len) * math.cos(a))
        y2 = bulb_cy + int((ray_start + ray_len) * math.sin(a))
        draw.line([x1, y1, x2, y2], fill=YELLOW_HINT, width=max(1, radius // 18))


def draw_gradient_bar(img, x0, y0, x1, y1, color_start, color_end):
    """Draw a horizontal gradient bar."""
    draw = ImageDraw.Draw(img)
    w = x1 - x0
    rs, gs, bs = Image.new("RGB", (1,1), color_start).getpixel((0,0))
    re, ge, be = Image.new("RGB", (1,1), color_end).getpixel((0,0))
    for x in range(w):
        t = x / max(w - 1, 1)
        r = int(rs + (re - rs) * t)
        g = int(gs + (ge - gs) * t)
        b = int(bs + (be - bs) * t)
        draw.line([x0 + x, y0, x0 + x, y1], fill=(r, g, b))


def draw_gradient_bg(img, y_start, y_end, color_start, color_end):
    """Draw a vertical gradient background region."""
    draw = ImageDraw.Draw(img)
    h = y_end - y_start
    rs, gs, bs = Image.new("RGB", (1,1), color_start).getpixel((0,0))
    re, ge, be = Image.new("RGB", (1,1), color_end).getpixel((0,0))
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(rs + (re - rs) * t)
        g = int(gs + (ge - gs) * t)
        b = int(bs + (be - bs) * t)
        draw.line([0, y_start + y, img.width, y_start + y], fill=(r, g, b))


# ══════════════════════════════════════════════════════════════
# 1. Small Promo Tile  440x280
# ══════════════════════════════════════════════════════════════
def create_promo_small():
    W, H = 440, 280
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Purple gradient glow at bottom
    draw_gradient_bg(img, H - 50, H, "#1a1a2e", "#2d1066")

    # Purple accent line at bottom
    draw_gradient_bar(img, 40, H - 8, W - 40, H - 2, PURPLE_DARK, PURPLE_LIGHT)

    # Title
    font_title = get_font(36, bold=True)
    tw, th = text_bbox(draw, "HintCode", font_title)
    draw.text(((W - tw) // 2, 35), "HintCode", fill=WHITE, font=font_title)

    # Subtitle
    font_sub = get_font(16)
    st = "Progressive Hints for Coding Problems"
    sw, sh = text_bbox(draw, st, font_sub)
    draw.text(((W - sw) // 2, 80), st, fill=GRAY_LIGHT, font=font_sub)

    # Icon centered
    draw_icon(draw, W // 2, 175, 55)

    path = os.path.join(OUTPUT_DIR, "promo-small-440x280.png")
    img.save(path)
    print(f"Created: {path}")


# ══════════════════════════════════════════════════════════════
# 2. Large Promo Tile  920x680
# ══════════════════════════════════════════════════════════════
def create_promo_large():
    W, H = 920, 680
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Subtle gradient at bottom
    draw_gradient_bg(img, H - 80, H, "#1a1a2e", "#2d1066")

    # ── LEFT SIDE ──
    left_x = 60
    font_big = get_font(48, bold=True)
    draw.text((left_x, 50), "HintCode", fill=WHITE, font=font_big)

    font_sub = get_font(20)
    draw.text((left_x, 115), "Learn by thinking, not copying", fill=GRAY_LIGHT, font=font_sub)

    # Purple divider
    draw.rectangle([left_x, 155, left_x + 80, 158], fill=PURPLE_LIGHT)

    # Bullet points
    font_bullet = get_font(19)
    bullets = [
        ("3-Level Progressive Hints", YELLOW_HINT),
        ("5 Coding Platforms", BLUE_HINT),
        ("Powered by Grok AI", PURPLE_LIGHT),
        ("100% Private - BYOK", "#10b981"),
    ]
    by = 180
    for text, color in bullets:
        # Bullet dot
        draw.ellipse([left_x + 4, by + 6, left_x + 16, by + 18], fill=color)
        draw.text((left_x + 28, by), text, fill=WHITE, font=font_bullet)
        by += 40

    # Icon below bullets
    draw_icon(draw, left_x + 100, by + 80, 60)

    # ── RIGHT SIDE: Mock hint panel ──
    panel_x = 480
    panel_y = 50
    panel_w = 390
    panel_h = 580

    # Panel background
    draw_rounded_rect(draw, [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], 16, fill=CARD_BG)
    # Panel border
    draw_rounded_rect(draw, [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], 16, outline="#2a2a4a", width=2)

    # Panel title
    font_panel_title = get_font(22, bold=True)
    draw.text((panel_x + 30, panel_y + 25), "HintCode Hints", fill=WHITE, font=font_panel_title)

    # Problem name
    font_sm = get_font(14)
    draw.text((panel_x + 30, panel_y + 60), "Problem: Two Sum", fill=GRAY_LIGHT, font=font_sm)

    # Hint cards
    card_data = [
        ("Hint 1: Gentle Nudge", YELLOW_HINT, "#78350f",
         "Think about using a data structure\nthat allows O(1) lookups..."),
        ("Hint 2: Approach", BLUE_HINT, "#1e3a5f",
         "Use a hash map to store each\nnumber's complement as you iterate..."),
        ("Hint 3: Detailed Guide", PURPLE_HINT, PURPLE_DARK,
         "Create a dict. For each num, check\nif target-num exists in dict. If yes,\nreturn indices. Else store num:idx."),
    ]

    cy = panel_y + 95
    for title, accent, card_bg, body in card_data:
        card_h = 140
        # Card background
        draw_rounded_rect(draw, [panel_x + 20, cy, panel_x + panel_w - 20, cy + card_h], 10, fill=card_bg)
        # Accent bar on left
        draw.rectangle([panel_x + 20, cy + 12, panel_x + 26, cy + card_h - 12], fill=accent)
        # Title
        font_card_title = get_font(17, bold=True)
        draw.text((panel_x + 38, cy + 14), title, fill=accent, font=font_card_title)
        # Body
        font_card = get_font(13)
        draw.text((panel_x + 38, cy + 42), body, fill="#d1d5db", font=font_card)
        cy += card_h + 16

    # "Powered by Grok AI" at bottom of panel
    font_tiny = get_font(12)
    pw_text = "Powered by Grok AI"
    pw_w, _ = text_bbox(draw, pw_text, font_tiny)
    draw.text((panel_x + (panel_w - pw_w) // 2, panel_y + panel_h - 35), pw_text, fill=GRAY_MID, font=font_tiny)

    path = os.path.join(OUTPUT_DIR, "promo-large-920x680.png")
    img.save(path)
    print(f"Created: {path}")


# ══════════════════════════════════════════════════════════════
# 3. Screenshot 1  1280x800 - Progressive Hints
# ══════════════════════════════════════════════════════════════
def create_screenshot_1():
    W, H = 1280, 800
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title bar area
    font_title = get_font(32, bold=True)
    title = "Get Progressive Hints When You're Stuck"
    tw, th = text_bbox(draw, title, font_title)
    draw.text(((W - tw) // 2, 30), title, fill=WHITE, font=font_title)

    # Purple underline
    draw_gradient_bar(img, (W - 300) // 2, 75, (W + 300) // 2, 79, PURPLE_DARK, PURPLE_LIGHT)

    # ── LEFT: Code editor mockup ──
    editor_x, editor_y = 50, 110
    editor_w, editor_h = 620, 640

    # Editor background
    draw_rounded_rect(draw, [editor_x, editor_y, editor_x + editor_w, editor_y + editor_h], 12, fill="#0d1117")
    # Title bar
    draw_rounded_rect(draw, [editor_x, editor_y, editor_x + editor_w, editor_y + 40], 12, fill="#161b22")
    draw.rectangle([editor_x, editor_y + 28, editor_x + editor_w, editor_y + 40], fill="#161b22")
    # Traffic lights
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        draw.ellipse([editor_x + 16 + i * 22, editor_y + 12, editor_x + 28 + i * 22, editor_y + 24], fill=c)
    # Tab
    font_tab = get_font(12)
    draw.text((editor_x + 90, editor_y + 13), "solution.py", fill=GRAY_LIGHT, font=font_tab)

    # Code lines (simulated)
    code_lines = [
        ("#c678dd", "class"),  (" ", WHITE, " "),  ("#e5c07b", "Solution"),  ("#abb2bf", ":"),
        None,
        ("    ", "#abb2bf", ""),  ("#c678dd", "def"),  (" ", WHITE, " "),  ("#61afef", "twoSum"),  ("#abb2bf", "(self, nums, target):"),
        None,
        ("        ", "#7f848e", "# How to solve this efficiently?"),
        ("        ", "#7f848e", "# Brute force is O(n^2)..."),
        None,
        ("        ", "#c678dd", "for"),  (" ", "#e06c75", "i"),  (" ", "#c678dd", "in"),  (" ", "#61afef", "range"),  ("#abb2bf", "(len(nums)):"),
        ("            ", "#c678dd", "for"),  (" ", "#e06c75", "j"),  (" ", "#c678dd", "in"),  (" ", "#61afef", "range"),  ("#abb2bf", "(i+1, len(nums)):"),
        ("                ", "#c678dd", "if"),  (" ", "#abb2bf", "nums[i] + nums[j] == target:"),
        ("                    ", "#c678dd", "return"),  (" ", "#abb2bf", "[i, j]"),
        None,
        ("        ", "#7f848e", "# There must be a better way..."),
        ("        ", "#7f848e", "# Let me check HintCode hints!"),
    ]

    font_code = get_font(14)
    ly = editor_y + 55
    line_h = 24
    for line in code_lines:
        if line is None:
            ly += line_h
            continue
        if isinstance(line, tuple) and len(line) == 2:
            color, text = line
            draw.text((editor_x + 20, ly), text, fill=color, font=font_code)
            lx = editor_x + 20 + text_bbox(draw, text, font_code)[0]
        elif isinstance(line, tuple) and len(line) == 3:
            indent, color, text = line
            full = indent + text
            draw.text((editor_x + 20, ly), full, fill=color, font=font_code)
            ly += line_h
            continue
        else:
            ly += line_h
            continue
        # For multi-segment lines, just continue on same line
        ly += line_h

    # Line numbers
    font_ln = get_font(12)
    for i in range(1, 22):
        draw.text((editor_x + 6, editor_y + 55 + (i-1) * line_h - 1), str(i), fill="#4b5263", font=font_ln)

    # ── RIGHT: Hint side panel ──
    panel_x = 710
    panel_y = 110
    panel_w = 520
    panel_h = 640

    draw_rounded_rect(draw, [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], 12, fill=CARD_BG)

    # Panel header
    font_ph = get_font(24, bold=True)
    draw_icon(draw, panel_x + 30, panel_y + 30, 18)
    draw.text((panel_x + 56, panel_y + 18), "HintCode", fill=WHITE, font=font_ph)

    font_prob = get_font(14)
    draw.text((panel_x + 30, panel_y + 55), "Problem detected: Two Sum", fill=GRAY_LIGHT, font=font_prob)

    # Hint buttons/cards
    hints = [
        ("Hint 1: Gentle Nudge", YELLOW_HINT, "#78350f",
         "Think about what data structure gives you\nO(1) lookup time. You've probably used it\nbefore in other problems..."),
        ("Hint 2: Approach", BLUE_HINT, "#1e3a5f",
         "Use a hash map (dictionary). As you iterate\nthrough the array, for each element, check if\nits complement (target - current) exists in the map."),
        ("Hint 3: Detailed Guide", PURPLE_HINT, PURPLE_DARK,
         "1. Create an empty dictionary\n2. For each number at index i:\n   - Calculate complement = target - nums[i]\n   - If complement in dict, return [dict[complement], i]\n   - Otherwise, store nums[i]: i in dict\nTime: O(n), Space: O(n)"),
    ]

    cy = panel_y + 85
    for title, accent, card_bg, body in hints:
        # Determine card height based on body lines
        lines = body.count("\n") + 1
        card_h = 55 + lines * 20

        # Card
        draw_rounded_rect(draw, [panel_x + 18, cy, panel_x + panel_w - 18, cy + card_h], 10, fill=card_bg)

        # Left accent bar
        draw.rectangle([panel_x + 18, cy + 8, panel_x + 24, cy + card_h - 8], fill=accent)

        # Lock/unlock icon (small circle)
        draw.ellipse([panel_x + panel_w - 50, cy + 14, panel_x + panel_w - 34, cy + 30], fill=accent)

        # Title
        font_ht = get_font(17, bold=True)
        draw.text((panel_x + 36, cy + 12), title, fill=accent, font=font_ht)

        # Body
        font_hb = get_font(13)
        draw.text((panel_x + 36, cy + 38), body, fill="#d1d5db", font=font_hb)

        cy += card_h + 14

    # Footer
    font_footer = get_font(12)
    ft = "Powered by Grok AI  |  Your API key, your privacy"
    fw, _ = text_bbox(draw, ft, font_footer)
    draw.text((panel_x + (panel_w - fw) // 2, panel_y + panel_h - 30), ft, fill=GRAY_MID, font=font_footer)

    path = os.path.join(OUTPUT_DIR, "screenshot-1-1280x800.png")
    img.save(path)
    print(f"Created: {path}")


# ══════════════════════════════════════════════════════════════
# 4. Screenshot 2  1280x800 - 5 Platforms
# ══════════════════════════════════════════════════════════════
def create_screenshot_2():
    W, H = 1280, 800
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    font_title = get_font(36, bold=True)
    title = "Works on 5 Major Coding Platforms"
    tw, _ = text_bbox(draw, title, font_title)
    draw.text(((W - tw) // 2, 50), title, fill=WHITE, font=font_title)

    # Subtitle
    font_sub = get_font(18)
    sub = "Seamless integration with your favorite platforms"
    sw, _ = text_bbox(draw, sub, font_sub)
    draw.text(((W - sw) // 2, 100), sub, fill=GRAY_LIGHT, font=font_sub)

    # Purple underline
    draw_gradient_bar(img, (W - 250) // 2, 135, (W + 250) // 2, 139, PURPLE_DARK, PURPLE_LIGHT)

    # Platform data
    platforms = [
        ("LC", "#FFA116", "LeetCode"),
        ("HR", "#00EA64", "HackerRank"),
        ("CF", "#1890FF", "Codeforces"),
        ("CC", "#5B4638", "CodeChef"),
        ("GFG", "#2F8D46", "GeeksforGeeks"),
    ]

    # Layout: 5 circles evenly spaced
    circle_r = 70
    total_w = (len(platforms) - 1) * 220
    start_x = (W - total_w) // 2
    center_y = 320

    font_init = get_font(38, bold=True)
    font_name = get_font(18)
    font_desc = get_font(13)

    descriptions = [
        "Problems, Contests\n& Interview Prep",
        "Challenges, Certifications\n& Interview Prep",
        "Competitive Programming\n& Contests",
        "Practice, Compete\n& Learn",
        "Practice, Tutorials\n& Company Questions",
    ]

    for i, (initials, color, name) in enumerate(platforms):
        cx = start_x + i * 220
        cy = center_y

        # Outer glow ring
        for r_offset in range(8, 0, -1):
            alpha_hex = hex(20 + r_offset * 3)[2:].zfill(2)
            glow_color = color
            draw.ellipse([cx - circle_r - r_offset, cy - circle_r - r_offset,
                          cx + circle_r + r_offset, cy + circle_r + r_offset],
                         outline=glow_color, width=1)

        # Circle background
        draw.ellipse([cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r], fill=color)

        # Inner darker circle for depth
        inner_r = circle_r - 6
        # Slightly darker version
        draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=color)

        # Initials
        iw, ih = text_bbox(draw, initials, font_init)
        draw.text((cx - iw // 2, cy - ih // 2 - 2), initials, fill=WHITE, font=font_init)

        # Platform name
        nw, _ = text_bbox(draw, name, font_name)
        draw.text((cx - nw // 2, cy + circle_r + 20), name, fill=WHITE, font=font_name)

        # Description
        desc = descriptions[i]
        for j, line in enumerate(desc.split("\n")):
            lw, _ = text_bbox(draw, line, font_desc)
            draw.text((cx - lw // 2, cy + circle_r + 48 + j * 18), line, fill=GRAY_LIGHT, font=font_desc)

    # Bottom section: feature highlights
    features_y = 530
    draw.rectangle([0, features_y, W, features_y + 1], fill="#2a2a4a")

    font_feat_title = get_font(22, bold=True)
    ft = "One Extension, All Platforms"
    ftw, _ = text_bbox(draw, ft, font_feat_title)
    draw.text(((W - ftw) // 2, features_y + 25), ft, fill=WHITE, font=font_feat_title)

    # Feature boxes
    features = [
        ("Auto-Detect", "Automatically detects\nthe coding platform\nand problem"),
        ("Smart Parsing", "Extracts problem\nstatement, constraints\nand examples"),
        ("Instant Hints", "Get 3 levels of\nprogressive hints\nin seconds"),
    ]

    box_w = 300
    box_h = 150
    box_gap = 40
    total_boxes = len(features) * box_w + (len(features) - 1) * box_gap
    box_start_x = (W - total_boxes) // 2
    box_y = features_y + 65

    font_box_title = get_font(18, bold=True)
    font_box_desc = get_font(14)

    for i, (title, desc) in enumerate(features):
        bx = box_start_x + i * (box_w + box_gap)
        draw_rounded_rect(draw, [bx, box_y, bx + box_w, box_y + box_h], 10, fill=CARD_BG, outline="#2a2a4a", width=1)

        # Accent dot
        draw.ellipse([bx + 20, box_y + 18, bx + 32, box_y + 30], fill=PURPLE_LIGHT)

        tw2, _ = text_bbox(draw, title, font_box_title)
        draw.text((bx + 42, box_y + 15), title, fill=WHITE, font=font_box_title)
        draw.text((bx + 20, box_y + 48), desc, fill=GRAY_LIGHT, font=font_box_desc)

    path = os.path.join(OUTPUT_DIR, "screenshot-2-1280x800.png")
    img.save(path)
    print(f"Created: {path}")


# ══════════════════════════════════════════════════════════════
# 5. Screenshot 3  1280x800 - Easy Setup
# ══════════════════════════════════════════════════════════════
def create_screenshot_3():
    W, H = 1280, 800
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Title
    font_title = get_font(36, bold=True)
    title = "Easy Setup - Just Add Your Free API Key"
    tw, _ = text_bbox(draw, title, font_title)
    draw.text(((W - tw) // 2, 40), title, fill=WHITE, font=font_title)

    # Subtitle
    font_sub = get_font(18)
    sub = "Get started in under 60 seconds"
    sw, _ = text_bbox(draw, sub, font_sub)
    draw.text(((W - sw) // 2, 90), sub, fill=GRAY_LIGHT, font=font_sub)

    # Purple underline
    draw_gradient_bar(img, (W - 200) // 2, 125, (W + 200) // 2, 129, PURPLE_DARK, PURPLE_LIGHT)

    # ── Settings card (centered) ──
    card_w = 600
    card_h = 480
    card_x = (W - card_w) // 2
    card_y = 160

    # Card shadow
    draw_rounded_rect(draw, [card_x + 4, card_y + 4, card_x + card_w + 4, card_y + card_h + 4], 16, fill="#0a0a1a")
    # Card
    draw_rounded_rect(draw, [card_x, card_y, card_x + card_w, card_y + card_h], 16, fill=CARD_BG)
    draw_rounded_rect(draw, [card_x, card_y, card_x + card_w, card_y + card_h], 16, outline="#2a2a4a", width=2)

    # Card header
    draw_rounded_rect(draw, [card_x, card_y, card_x + card_w, card_y + 55], 16, fill=CARD_BG2)
    draw.rectangle([card_x, card_y + 40, card_x + card_w, card_y + 55], fill=CARD_BG2)

    # Icon in header
    draw_icon(draw, card_x + 35, card_y + 27, 16)
    font_header = get_font(20, bold=True)
    draw.text((card_x + 60, card_y + 16), "HintCode Settings", fill=WHITE, font=font_header)

    # ── Form content ──
    form_x = card_x + 40
    form_y = card_y + 80

    # API Provider label
    font_label = get_font(16, bold=True)
    font_input = get_font(15)
    font_hint = get_font(13)

    draw.text((form_x, form_y), "AI Provider", fill=GRAY_LIGHT, font=font_label)

    # Provider selector (mock dropdown)
    sel_y = form_y + 28
    draw_rounded_rect(draw, [form_x, sel_y, form_x + card_w - 80, sel_y + 42], 8, fill="#0d1117", outline="#374151", width=1)
    draw.text((form_x + 14, sel_y + 10), "Grok (xAI)                                                            v", fill=WHITE, font=font_input)

    # API Key label
    key_y = sel_y + 65
    draw.text((form_x, key_y), "API Key", fill=GRAY_LIGHT, font=font_label)

    # API Key input
    inp_y = key_y + 28
    draw_rounded_rect(draw, [form_x, inp_y, form_x + card_w - 80, inp_y + 42], 8, fill="#0d1117", outline="#374151", width=1)
    draw.text((form_x + 14, inp_y + 10), "xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxx", fill=GRAY_MID, font=font_input)

    # Lock icon hint
    draw.text((form_x, inp_y + 50), "Your key is stored locally and never sent to our servers", fill="#10b981", font=font_hint)

    # Buttons row
    btn_y = inp_y + 90
    # Save button
    btn_w = 160
    btn_h = 44
    draw_rounded_rect(draw, [form_x, btn_y, form_x + btn_w, btn_y + btn_h], 10, fill=PURPLE)
    font_btn = get_font(16, bold=True)
    btw, _ = text_bbox(draw, "Save Key", font_btn)
    draw.text((form_x + (btn_w - btw) // 2, btn_y + 11), "Save Key", fill=WHITE, font=font_btn)

    # Test Connection button
    btn2_x = form_x + btn_w + 20
    btn2_w = 200
    draw_rounded_rect(draw, [btn2_x, btn_y, btn2_x + btn2_w, btn_y + btn_h], 10, fill="#0d1117", outline=PURPLE_LIGHT, width=2)
    btw2, _ = text_bbox(draw, "Test Connection", font_btn)
    draw.text((btn2_x + (btn2_w - btw2) // 2, btn_y + 11), "Test Connection", fill=PURPLE_LIGHT, font=font_btn)

    # Success message area
    success_y = btn_y + 65
    draw_rounded_rect(draw, [form_x, success_y, form_x + card_w - 80, success_y + 40], 8, fill="#064e3b")
    font_success = get_font(14)
    draw.text((form_x + 14, success_y + 10), "Connection successful! You're all set.", fill="#34d399", font=font_success)
    # Checkmark
    draw.text((form_x + card_w - 110, success_y + 10), "OK", fill="#34d399", font=font_success)

    # Get free key info
    info_y = success_y + 60
    draw_rounded_rect(draw, [form_x, info_y, form_x + card_w - 80, info_y + 55], 8, fill="#1e1b4b", outline=PURPLE_DARK, width=1)
    font_info = get_font(14)
    draw.text((form_x + 14, info_y + 8), "Get your free API key at:", fill=GRAY_LIGHT, font=font_info)
    font_link = get_font(16, bold=True)
    draw.text((form_x + 14, info_y + 30), "console.x.ai", fill=PURPLE_LIGHT, font=font_link)
    # Underline the link
    lw_link, _ = text_bbox(draw, "console.x.ai", font_link)
    draw.line([form_x + 14, info_y + 49, form_x + 14 + lw_link, info_y + 49], fill=PURPLE_LIGHT, width=1)

    # ── Side steps (right side) ──
    steps_x = card_x + card_w + 50
    steps_y = 200
    font_step_title = get_font(18, bold=True)
    font_step_desc = get_font(14)

    steps = [
        ("Step 1", "Visit console.x.ai\nand create an account", YELLOW_HINT),
        ("Step 2", "Generate a free\nAPI key", BLUE_HINT),
        ("Step 3", "Paste key in the\nextension settings", PURPLE_LIGHT),
        ("Step 4", "Start solving with\nprogressive hints!", "#10b981"),
    ]

    for i, (step_title, step_desc, color) in enumerate(steps):
        sy = steps_y + i * 130

        # Step circle with number
        draw.ellipse([steps_x, sy, steps_x + 40, sy + 40], fill=color)
        num = str(i + 1)
        nw, nh = text_bbox(draw, num, font_step_title)
        draw.text((steps_x + (40 - nw) // 2, sy + (40 - nh) // 2 - 2), num, fill=WHITE, font=font_step_title)

        # Connecting line to next step
        if i < len(steps) - 1:
            draw.line([steps_x + 20, sy + 44, steps_x + 20, sy + 130], fill="#374151", width=2)

        # Text
        draw.text((steps_x + 52, sy + 2), step_title, fill=color, font=font_step_title)
        draw.text((steps_x + 52, sy + 26), step_desc, fill=GRAY_LIGHT, font=font_step_desc)

    path = os.path.join(OUTPUT_DIR, "screenshot-3-1280x800.png")
    img.save(path)
    print(f"Created: {path}")


# ══════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Chrome Web Store assets...")
    print()
    create_promo_small()
    create_promo_large()
    create_screenshot_1()
    create_screenshot_2()
    create_screenshot_3()
    print()
    print("All assets generated successfully!")
