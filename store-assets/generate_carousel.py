from PIL import Image, ImageDraw, ImageFont
import os, math

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1080, 1350

# ── Fonts ──
def font(size, bold=False):
    names = ['segoeuib.ttf', 'arialbd.ttf'] if bold else ['segoeui.ttf', 'arial.ttf']
    for n in names:
        try: return ImageFont.truetype(n, size)
        except: pass
    return ImageFont.load_default()

# ── Colors ──
BG_DARK    = (10, 10, 20)
BG_CARD    = (18, 18, 35)
PURPLE     = (124, 58, 237)
PURPLE_L   = (167, 139, 250)
PURPLE_D   = (88, 28, 195)
BLUE       = (59, 130, 246)
CYAN       = (6, 182, 212)
GREEN      = (34, 197, 94)
YELLOW     = (250, 204, 21)
ORANGE     = (249, 115, 22)
RED        = (239, 68, 68)
WHITE      = (255, 255, 255)
GRAY       = (148, 163, 184)
LIGHT      = (226, 232, 240)
DARK_GRAY  = (51, 65, 85)
SURFACE    = (30, 30, 55)

def new_slide():
    img = Image.new('RGB', (W, H), BG_DARK)
    return img, ImageDraw.Draw(img)

def draw_rr(d, xy, fill, r=16, outline=None, width=0):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def gradient_rect(img, d, box, c1, c2, vertical=True):
    x1, y1, x2, y2 = box
    for i in range(y2 - y1 if vertical else x2 - x1):
        t = i / max((y2 - y1 if vertical else x2 - x1) - 1, 1)
        c = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        if vertical:
            d.line([(x1, y1 + i), (x2, y1 + i)], fill=c)
        else:
            d.line([(x1 + i, y1), (x1 + i, y2)], fill=c)

def draw_glow(d, cx, cy, radius, color, alpha_max=40):
    for r in range(radius, 0, -2):
        a = int(alpha_max * (1 - r / radius))
        c = tuple(min(255, color[j] + a) for j in range(3))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=None, outline=c, width=1)

def slide_number(d, num, total):
    d.text((W - 60, H - 50), f'{num}/{total}', font=font(18), fill=DARK_GRAY, anchor='mm')

def brand_footer(d):
    draw_rr(d, [0, H - 80, W, H], (8, 8, 18), r=0)
    d.text((W // 2, H - 40), 'github.com/saiteja181/hintcode', font=font(20, bold=True), fill=PURPLE_L, anchor='mm')

TOTAL = 10

# ══════════════════════════════════════════════════
# SLIDE 1: HOOK
# ══════════════════════════════════════════════════
img, d = new_slide()

# Dramatic gradient background
gradient_rect(img, d, [0, 0, W, H], (15, 5, 30), (5, 5, 15))

# Glowing orb behind text
for r in range(300, 0, -3):
    a = int(25 * (1 - r / 300))
    c = (PURPLE[0] // 6 + a, PURPLE[1] // 6 + a, PURPLE[2] // 6 + a)
    d.ellipse([W//2 - r, 350 - r, W//2 + r, 350 + r], fill=c)

# Top label
draw_rr(d, [W//2 - 140, 100, W//2 + 140, 145], PURPLE_D, r=25)
d.text((W//2, 122), 'STOP DOING THIS', font=font(22, bold=True), fill=WHITE, anchor='mm')

# Main hook text
d.text((W//2, 280), 'You Google', font=font(72, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 370), 'the answer.', font=font(72, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 460), 'Copy-paste.', font=font(72, bold=True), fill=RED, anchor='mm')
d.text((W//2, 550), 'Submit.', font=font(72, bold=True), fill=RED, anchor='mm')

# Separator line
d.line([(200, 640), (880, 640)], fill=PURPLE, width=3)

# Bottom text
d.text((W//2, 720), 'You learned', font=font(64, bold=True), fill=GRAY, anchor='mm')
d.text((W//2, 810), 'NOTHING.', font=font(80, bold=True), fill=WHITE, anchor='mm')

# Swipe hint
d.text((W//2, 1000), 'There is a better way.', font=font(32), fill=PURPLE_L, anchor='mm')

# Arrow
for i in range(3):
    ax = W//2 + i * 30
    d.text((ax + 780 - W//2, 1080), '>', font=font(36, bold=True), fill=PURPLE_L if i == 2 else DARK_GRAY, anchor='mm')

d.text((W//2, 1080), 'Swipe  >>>', font=font(24, bold=True), fill=PURPLE_L, anchor='mm')

brand_footer(d)
slide_number(d, 1, TOTAL)
img.save('carousel-01-hook.png')
print('Slide 1 done')


# ══════════════════════════════════════════════════
# SLIDE 2: THE PROBLEM
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (15, 5, 25), (5, 5, 15))

d.text((W//2, 80), 'The Student Cycle', font=font(42, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 135), 'Every CS student knows this loop', font=font(22), fill=GRAY, anchor='mt')

# Circular flow diagram
steps = [
    ('Stuck on\nproblem', RED, 170),
    ('Google the\nsolution', ORANGE, 170),
    ('Copy-paste\ncode', YELLOW, 170),
    ('Submit.\n"Accepted"', GREEN, 170),
    ('Next problem.\nSame struggle.', RED, 170),
]

# Draw as vertical flow with arrows
sy = 220
for i, (text, color, _) in enumerate(steps):
    cy = sy + i * 170
    # Card
    draw_rr(d, [140, cy, 940, cy + 120], SURFACE, r=16, outline=color, width=3)
    # Number circle
    d.ellipse([170, cy + 30, 230, cy + 90], fill=color)
    d.text((200, cy + 60), str(i + 1), font=font(28, bold=True), fill=WHITE, anchor='mm')
    # Text
    lines = text.split('\n')
    d.text((280, cy + (60 if len(lines) == 1 else 42)), lines[0], font=font(30, bold=True), fill=WHITE, anchor='lm')
    if len(lines) > 1:
        d.text((280, cy + 78), lines[1], font=font(24), fill=LIGHT, anchor='lm')
    # Arrow down
    if i < len(steps) - 1:
        ax = W // 2
        d.polygon([(ax - 10, cy + 130), (ax + 10, cy + 130), (ax, cy + 155)], fill=DARK_GRAY)

# Loop arrow hint
d.text((W//2, sy + 5 * 170 + 20), 'Repeat forever...', font=font(28, bold=True), fill=RED, anchor='mt')
draw_rr(d, [W//2 - 12, sy + 5 * 170 + 55, W//2 + 12, sy + 5 * 170 + 62], RED, r=2)

# Curved arrow from bottom back to top (simplified)
d.text((W//2, sy + 5 * 170 + 80), 'You never actually LEARN.', font=font(26), fill=GRAY, anchor='mt')

brand_footer(d)
slide_number(d, 2, TOTAL)
img.save('carousel-02-problem.png')
print('Slide 2 done')


# ══════════════════════════════════════════════════
# SLIDE 3: INTRODUCING HINTCODE
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (20, 8, 40), (5, 5, 15))

# Glow
for r in range(250, 0, -3):
    a = int(20 * (1 - r / 250))
    c = (PURPLE[0] // 8 + a, PURPLE[1] // 8 + a, PURPLE[2] // 8 + a)
    d.ellipse([W//2 - r, 320 - r, W//2 + r, 320 + r], fill=c)

# Badge
draw_rr(d, [W//2 - 80, 80, W//2 + 80, 120], GREEN, r=20)
d.text((W//2, 100), 'FREE TOOL', font=font(20, bold=True), fill=WHITE, anchor='mm')

# Logo area
d.ellipse([W//2 - 70, 170, W//2 + 70, 310], fill=PURPLE)
d.text((W//2, 220), 'HC', font=font(56, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 275), '</>', font=font(24, bold=True), fill=PURPLE_L, anchor='mm')

# Name
d.text((W//2, 360), 'HintCode', font=font(72, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 440), 'Smart Coding Hints for Students', font=font(28), fill=PURPLE_L, anchor='mm')

# Separator
d.line([(250, 500), (830, 500)], fill=PURPLE, width=2)

# What it does
desc_lines = [
    'A Chrome extension that reads your code,',
    'finds the exact bug, and nudges you to',
    'fix it yourself.',
    '',
    'Progressive hints - not solutions.',
]
ly = 540
for line in desc_lines:
    if line:
        d.text((W//2, ly), line, font=font(26), fill=LIGHT, anchor='mm')
    ly += 40

# Key stats
stats = [
    ('5', 'Platforms'),
    ('3', 'Hint Levels'),
    ('0', 'Data Collected'),
]
sx = 180
for val, label in stats:
    draw_rr(d, [sx - 100, 800, sx + 100, 920], SURFACE, r=14, outline=PURPLE_D, width=2)
    d.text((sx, 840), val, font=font(48, bold=True), fill=PURPLE_L, anchor='mm')
    d.text((sx, 890), label, font=font(18), fill=GRAY, anchor='mm')
    sx += 260

# Bottom tagline
d.text((W//2, 1000), 'No servers. No tracking. No subscriptions.', font=font(22), fill=GRAY, anchor='mm')
d.text((W//2, 1040), 'Just you, your code, and better hints.', font=font(24, bold=True), fill=GREEN, anchor='mm')

brand_footer(d)
slide_number(d, 3, TOTAL)
img.save('carousel-03-intro.png')
print('Slide 3 done')


# ══════════════════════════════════════════════════
# SLIDE 4: HOW IT WORKS - OVERVIEW
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (12, 5, 25), (5, 5, 12))

d.text((W//2, 70), 'How It Works', font=font(48, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 130), 'From stuck to solved in 4 steps', font=font(22), fill=GRAY, anchor='mt')

flow_steps = [
    (BLUE, 'DETECT', 'HintCode reads your code\n+ problem from the page', '{}'),
    (PURPLE, 'HINT 1', 'Gentle nudge about your\nspecific bug', '?'),
    (CYAN, 'HINT 2', 'Names the technique.\nPoints at buggy lines.', '!'),
    (GREEN, 'HINT 3', 'Step-by-step guide.\nEdge cases. No code given.', '*'),
]

sy = 210
for i, (color, title, desc, icon) in enumerate(flow_steps):
    cy = sy + i * 230

    # Connection line
    if i > 0:
        d.line([(160, cy - 110), (160, cy + 10)], fill=DARK_GRAY, width=3)

    # Icon circle
    d.ellipse([110, cy + 10, 210, cy + 110], fill=color)
    d.text((160, cy + 60), icon, font=font(40, bold=True), fill=WHITE, anchor='mm')

    # Card
    draw_rr(d, [250, cy, 950, cy + 120], SURFACE, r=14, outline=color, width=2)

    # Step label
    draw_rr(d, [270, cy + 10, 270 + len(title) * 16, cy + 42], color, r=8)
    d.text((275, cy + 26), title, font=font(18, bold=True), fill=WHITE, anchor='lm')

    # Description
    lines = desc.split('\n')
    d.text((275, cy + 62), lines[0], font=font(22), fill=LIGHT, anchor='lm')
    if len(lines) > 1:
        d.text((275, cy + 92), lines[1], font=font(22), fill=GRAY, anchor='lm')

# Bottom note
draw_rr(d, [100, 1140, 980, 1200], (40, 20, 20), r=12, outline=RED, width=2)
d.text((W//2, 1170), 'Last resort: Full solution (only if you ask twice)', font=font(20, bold=True), fill=(255, 180, 180), anchor='mm')

brand_footer(d)
slide_number(d, 4, TOTAL)
img.save('carousel-04-how.png')
print('Slide 4 done')


# ══════════════════════════════════════════════════
# SLIDE 5: CODE-AWARE DEMO - HINT 1
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (12, 5, 25), (5, 5, 12))

d.text((W//2, 60), 'Code-Aware Hints', font=font(42, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 115), 'Not generic advice. YOUR code. YOUR bug.', font=font(22), fill=GRAY, anchor='mt')

# Code editor mock — compact
draw_rr(d, [60, 170, 1020, 500], (13, 17, 23), r=14)
draw_rr(d, [60, 170, 1020, 208], (30, 30, 50), r=14)
d.rectangle([60, 195, 1020, 208], fill=(30, 30, 50))
d.ellipse([80, 180, 94, 194], fill=(255, 95, 87))
d.ellipse([104, 180, 118, 194], fill=(255, 189, 46))
d.ellipse([128, 180, 142, 194], fill=(39, 201, 63))
d.text((540, 189), 'max_subarray.py  |  LeetCode #53', font=font(13), fill=GRAY, anchor='mm')

code = [
    ('1', 'def', ' maxSubArray(self, nums):'),
    ('2', '    m', ' = 0'),
    ('3', '    cur', ' = 0'),
    ('4', '    for', ' n in nums:'),
    ('5', '        cur', ' += n'),
    ('6', '        if', ' cur > m:'),
    ('7', '            m', ' = cur'),
    ('8', '        if', ' cur < 0:'),
    ('9', '            cur', ' = 0'),
    ('10', '    return', ' m'),
]

cy = 220
f_code = font(16)
f_code_b = font(16, bold=True)
for num, kw, rest in code:
    if num == '2':
        d.rectangle([60, cy - 2, 1020, cy + 22], fill=(60, 20, 20))
        draw_rr(d, [920, cy, 1005, cy + 20], RED, r=6)
        d.text((962, cy + 10), 'BUG', font=font(11, bold=True), fill=WHITE, anchor='mm')
    d.text((85, cy), num, font=f_code, fill=(80, 80, 100))
    d.text((120, cy), kw, font=f_code_b, fill=PURPLE_L)
    d.text((120 + len(kw) * 9, cy), rest, font=f_code, fill=LIGHT)
    cy += 27

# Arrow
d.text((W//2, 530), 'HintCode detects the bug and says...', font=font(18), fill=PURPLE_L, anchor='mm')
d.polygon([(W//2 - 10, 555), (W//2 + 10, 555), (W//2, 572)], fill=PURPLE)

# Hint card — fits all text
draw_rr(d, [60, 590, 1020, 850], (45, 35, 8), r=14, outline=(200, 150, 30), width=2)
draw_rr(d, [80, 605, 240, 636], (200, 150, 30), r=8)
d.text((85, 620), 'HINT 1 - NUDGE', font=font(16, bold=True), fill=BG_DARK, anchor='lm')

hint_text = [
    ('Your line 2 sets m = 0.', False),
    ('', False),
    ('What happens when ALL numbers in', False),
    ('the array are negative?', False),
    ('', False),
    ('Try: nums = [-3, -1, -5]', True),
    ('What would your function return?', False),
]
hy = 655
for line, is_try in hint_text:
    if line:
        d.text((95, hy), line, font=font(20, bold=is_try), fill=YELLOW if is_try else (254, 243, 199))
    hy += 28

# Bottom note
d.text((W//2, 890), 'No algorithm names. No solution.', font=font(24, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 925), 'Just enough to make you THINK.', font=font(22), fill=PURPLE_L, anchor='mm')

# Before/After comparison
draw_rr(d, [60, 990, 510, 1190], (40, 15, 15), r=12, outline=RED, width=2)
d.text((285, 1020), 'ChatGPT / Google', font=font(20, bold=True), fill=RED, anchor='mm')
d.text((285, 1060), '"Use Kadane\'s algorithm.', font=font(18), fill=LIGHT, anchor='mm')
d.text((285, 1090), 'Here is the code..."', font=font(18), fill=LIGHT, anchor='mm')
d.line([(120, 1120), (450, 1120)], fill=RED, width=2)
d.text((285, 1150), 'You learned nothing.', font=font(18, bold=True), fill=RED, anchor='mm')

draw_rr(d, [570, 990, 1020, 1190], (15, 40, 15), r=12, outline=GREEN, width=2)
d.text((795, 1020), 'HintCode', font=font(20, bold=True), fill=GREEN, anchor='mm')
d.text((795, 1060), '"Your line 2 fails when', font=font(18), fill=LIGHT, anchor='mm')
d.text((795, 1090), 'nums = [-3, -1, -5]"', font=font(18), fill=LIGHT, anchor='mm')
d.line([(630, 1120), (960, 1120)], fill=GREEN, width=2)
d.text((795, 1150), 'You fix it yourself.', font=font(18, bold=True), fill=GREEN, anchor='mm')

brand_footer(d)
slide_number(d, 5, TOTAL)
img.save('carousel-05-demo.png')
print('Slide 5 done')


# ══════════════════════════════════════════════════
# SLIDE 6: PROGRESSIVE HINTS DEMO
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (12, 5, 25), (5, 5, 12))

d.text((W//2, 60), '3 Levels of Help', font=font(48, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 120), 'Escalate only when you need to', font=font(22), fill=GRAY, anchor='mt')

# Hint Level 1
draw_rr(d, [60, 190, 1020, 470], (45, 35, 8), r=16, outline=(200, 150, 30), width=2)
draw_rr(d, [80, 205, 340, 240], (200, 150, 30), r=10)
d.text((210, 222), 'LEVEL 1: NUDGE', font=font(18, bold=True), fill=BG_DARK, anchor='mm')
hint1 = [
    'Your line 2 sets m = 0. What happens when',
    'all numbers in the array are negative?',
    '',
    'Try nums = [-3, -1, -5]. What does your',
    'function return vs what it should return?',
]
hy = 260
for line in hint1:
    if line:
        d.text((95, hy), line, font=font(20), fill=(254, 243, 199))
    hy += 30

# Arrow
d.text((W//2, 490), 'Still stuck? Escalate.', font=font(18), fill=GRAY, anchor='mm')
d.polygon([(W//2 - 8, 510), (W//2 + 8, 510), (W//2, 525)], fill=BLUE)

# Hint Level 2
draw_rr(d, [60, 540, 1020, 810], (15, 30, 60), r=16, outline=BLUE, width=2)
draw_rr(d, [80, 555, 380, 590], BLUE, r=10)
d.text((230, 572), 'LEVEL 2: APPROACH', font=font(18, bold=True), fill=WHITE, anchor='mm')
hint2 = [
    'This is Kadane\'s Algorithm. Your m = 0 reset',
    'loses the "least negative" answer.',
    '',
    'Instead of 0, what should m start as to handle',
    'the all-negative case correctly?',
]
hy = 610
for line in hint2:
    if line:
        d.text((95, hy), line, font=font(20), fill=(200, 220, 255))
    hy += 30

# Arrow
d.text((W//2, 830), 'Need more detail?', font=font(18), fill=GRAY, anchor='mm')
d.polygon([(W//2 - 8, 850), (W//2 + 8, 850), (W//2, 865)], fill=PURPLE)

# Hint Level 3
draw_rr(d, [60, 880, 1020, 1180], (35, 20, 55), r=16, outline=PURPLE, width=2)
draw_rr(d, [80, 895, 430, 930], PURPLE, r=10)
d.text((255, 912), 'LEVEL 3: DETAILED GUIDE', font=font(18, bold=True), fill=WHITE, anchor='mm')
hint3 = [
    'Line 2: Initialize m = float(\'-inf\') not 0.',
    'Line 3: cur stays correct.',
    'Line 6-7: Your comparison logic is fine.',
    'Line 8-9: When cur < 0 you reset. Good.',
    '',
    'Edge case: [-1] should return -1, not 0.',
    'Fix line 2, keep everything else.',
]
hy = 950
for line in hint3:
    if line:
        is_line_ref = line.startswith('Line')
        d.text((95, hy), line, font=font(19, bold=is_line_ref), fill=(220, 200, 255) if is_line_ref else (200, 180, 240))
    hy += 28

brand_footer(d)
slide_number(d, 6, TOTAL)
img.save('carousel-06-levels.png')
print('Slide 6 done')


# ══════════════════════════════════════════════════
# SLIDE 7: 5 PLATFORMS
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (12, 5, 25), (5, 5, 12))

d.text((W//2, 70), 'Works Everywhere', font=font(48, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 130), '5 platforms. Auto-detection. Zero config.', font=font(22), fill=GRAY, anchor='mt')

platforms = [
    ('LeetCode', (255, 161, 22), 'LC', 'Most popular for interviews'),
    ('HackerRank', (0, 234, 100), 'HR', 'Used by companies for hiring'),
    ('CodeForces', (24, 144, 255), 'CF', 'Competitive programming'),
    ('CodeChef', (91, 70, 56), 'CC', 'Indian CP community'),
    ('GeeksforGeeks', (47, 141, 70), 'GFG', 'Practice + theory'),
]

sy = 210
for i, (name, color, initials, desc) in enumerate(platforms):
    cy = sy + i * 170
    # Card
    draw_rr(d, [80, cy, 1000, cy + 140], SURFACE, r=16, outline=color, width=2)

    # Icon circle
    d.ellipse([110, cy + 20, 210, cy + 120], fill=color)
    d.text((160, cy + 70), initials, font=font(34, bold=True), fill=WHITE, anchor='mm')

    # Platform name
    d.text((240, cy + 45), name, font=font(30, bold=True), fill=WHITE, anchor='lm')
    d.text((240, cy + 90), desc, font=font(20), fill=GRAY, anchor='lm')

    # Checkmark
    d.text((950, cy + 70), 'Auto', font=font(16, bold=True), fill=GREEN, anchor='rm')

# Bottom note
d.text((W//2, 1090), 'Auto-detects problem, code, and language', font=font(22), fill=LIGHT, anchor='mm')
d.text((W//2, 1130), 'Works with Monaco, CodeMirror, ACE editors', font=font(20), fill=GRAY, anchor='mm')

# Manual mode note
draw_rr(d, [200, 1170, 880, 1210], SURFACE, r=10, outline=PURPLE_D, width=1)
d.text((W//2, 1190), 'Manual mode available for any other site', font=font(18), fill=PURPLE_L, anchor='mm')

brand_footer(d)
slide_number(d, 7, TOTAL)
img.save('carousel-07-platforms.png')
print('Slide 7 done')


# ══════════════════════════════════════════════════
# SLIDE 8: PRIVACY & TRUST
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (5, 12, 20), (5, 5, 12))

d.text((W//2, 70), 'Privacy First', font=font(48, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 130), 'Your code stays YOUR code', font=font(24), fill=GRAY, anchor='mt')

# Architecture diagram
draw_rr(d, [100, 210, 500, 350], SURFACE, r=14, outline=BLUE, width=2)
d.text((300, 255), 'Your Browser', font=font(26, bold=True), fill=WHITE, anchor='mm')
d.text((300, 295), 'HintCode Extension', font=font(18), fill=BLUE, anchor='mm')

# Arrow
d.line([(500, 280), (580, 280)], fill=GREEN, width=3)
d.polygon([(575, 268), (595, 280), (575, 292)], fill=GREEN)
d.text((540, 260), 'Direct', font=font(14, bold=True), fill=GREEN, anchor='mm')

draw_rr(d, [580, 210, 980, 350], SURFACE, r=14, outline=GREEN, width=2)
d.text((780, 255), 'Groq / Grok API', font=font(26, bold=True), fill=WHITE, anchor='mm')
d.text((780, 295), 'Your own API key', font=font(18), fill=GREEN, anchor='mm')

# NO server
d.text((W//2, 400), 'NO middleman server', font=font(28, bold=True), fill=RED, anchor='mm')

# Privacy points
points = [
    ('No backend server', 'API calls go directly from your browser to AI', GREEN),
    ('No data collection', 'Zero analytics. Zero telemetry. Zero tracking.', GREEN),
    ('BYOK model', 'You provide your own free API key', GREEN),
    ('Fully open source', 'Audit every single line of code on GitHub', GREEN),
    ('Encrypted storage', 'API key in Chrome\'s encrypted sync storage', GREEN),
]
sy = 480
for title, desc, color in points:
    # Check icon — draw a tick mark
    d.ellipse([110, sy + 5, 150, sy + 45], fill=GREEN)
    # Draw tick as two lines
    cx_chk, cy_chk = 130, sy + 25
    d.line([(cx_chk - 8, cy_chk), (cx_chk - 2, cy_chk + 7)], fill=WHITE, width=3)
    d.line([(cx_chk - 2, cy_chk + 7), (cx_chk + 9, cy_chk - 6)], fill=WHITE, width=3)
    d.text((170, sy + 15), title, font=font(24, bold=True), fill=WHITE, anchor='lm')
    d.text((170, sy + 48), desc, font=font(18), fill=GRAY, anchor='lm')
    sy += 80

# Comparison
sy += 20
draw_rr(d, [100, sy, 500, sy + 120], (40, 15, 15), r=12, outline=RED, width=2)
d.text((300, sy + 25), 'Other AI tools', font=font(20, bold=True), fill=RED, anchor='mm')
d.text((300, sy + 55), 'Send your code to their servers', font=font(16), fill=LIGHT, anchor='mm')
d.text((300, sy + 80), 'Track usage. Sell data.', font=font(16), fill=GRAY, anchor='mm')

draw_rr(d, [580, sy, 980, sy + 120], (15, 40, 15), r=12, outline=GREEN, width=2)
d.text((780, sy + 25), 'HintCode', font=font(20, bold=True), fill=GREEN, anchor='mm')
d.text((780, sy + 55), 'YOUR key. YOUR browser.', font=font(16), fill=LIGHT, anchor='mm')
d.text((780, sy + 80), 'Nothing leaves your machine.', font=font(16), fill=GREEN, anchor='mm')

brand_footer(d)
slide_number(d, 8, TOTAL)
img.save('carousel-08-privacy.png')
print('Slide 8 done')


# ══════════════════════════════════════════════════
# SLIDE 9: SETUP IN 2 MINUTES
# ══════════════════════════════════════════════════
img, d = new_slide()
gradient_rect(img, d, [0, 0, W, H], (12, 5, 25), (5, 5, 12))

d.text((W//2, 60), 'Setup in 2 Minutes', font=font(48, bold=True), fill=WHITE, anchor='mt')
d.text((W//2, 120), 'Free. No credit card. No signup.', font=font(24), fill=GREEN, anchor='mt')

steps = [
    (BLUE, '1', 'Download from GitHub', 'Clone repo or download ZIP\ngithub.com/saiteja181/hintcode'),
    (PURPLE, '2', 'Load in Chrome', 'chrome://extensions\nEnable Developer Mode\nClick "Load unpacked"'),
    (CYAN, '3', 'Get free Groq API key', 'console.groq.com/keys\nNo credit card needed\nCopy the key'),
    (GREEN, '4', 'Paste key & start!', 'Click extension > Settings\nPaste key > Save > Test\nGo to LeetCode > Get hints!'),
]

sy = 200
for color, num, title, desc in steps:
    cy = sy
    # Main card
    draw_rr(d, [80, cy, 1000, cy + 230], SURFACE, r=16, outline=color, width=2)

    # Step number
    d.ellipse([110, cy + 15, 180, cy + 85], fill=color)
    d.text((145, cy + 50), num, font=font(36, bold=True), fill=WHITE, anchor='mm')

    # Title
    d.text((210, cy + 50), title, font=font(28, bold=True), fill=WHITE, anchor='lm')

    # Separator
    d.line([(110, cy + 95), (970, cy + 95)], fill=DARK_GRAY, width=1)

    # Description lines
    lines = desc.split('\n')
    ly = cy + 115
    for line in lines:
        is_url = '.' in line and ' ' not in line.strip()
        d.text((130, ly), line, font=font(20, bold=is_url), fill=PURPLE_L if is_url else LIGHT)
        ly += 30

    sy += 250

# Time badge
draw_rr(d, [W//2 - 150, 1210, W//2 + 150, 1250], GREEN, r=20)
d.text((W//2, 1230), 'Total time: ~2 minutes', font=font(20, bold=True), fill=WHITE, anchor='mm')

brand_footer(d)
slide_number(d, 9, TOTAL)
img.save('carousel-09-setup.png')
print('Slide 9 done')


# ══════════════════════════════════════════════════
# SLIDE 10: CTA
# ══════════════════════════════════════════════════
img, d = new_slide()

# Rich gradient
gradient_rect(img, d, [0, 0, W, H], (25, 10, 50), (5, 5, 15))

# Big glow
for r in range(400, 0, -3):
    a = int(18 * (1 - r / 400))
    c = (PURPLE[0] // 8 + a, PURPLE[1] // 8 + a, PURPLE[2] // 8 + a)
    d.ellipse([W//2 - r, 500 - r, W//2 + r, 500 + r], fill=c)

# Top quote
d.text((W//2, 100), '"The struggle is where', font=font(36, bold=True), fill=PURPLE_L, anchor='mm')
d.text((W//2, 150), 'learning happens."', font=font(36, bold=True), fill=PURPLE_L, anchor='mm')

# Separator
d.line([(350, 210), (730, 210)], fill=PURPLE, width=2)

# Main CTA
d.text((W//2, 300), 'Stop copying.', font=font(60, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 380), 'Start learning.', font=font(60, bold=True), fill=GREEN, anchor='mm')

# Logo
d.ellipse([W//2 - 50, 450, W//2 + 50, 550], fill=PURPLE)
d.text((W//2, 485), 'HC', font=font(40, bold=True), fill=WHITE, anchor='mm')
d.text((W//2, 530), '</>', font=font(18, bold=True), fill=PURPLE_L, anchor='mm')

d.text((W//2, 590), 'HintCode', font=font(48, bold=True), fill=WHITE, anchor='mm')

# Action items
actions = [
    'Star on GitHub',
    'github.com/saiteja181/hintcode',
    '',
    'Share with a friend who',
    'Googles every LeetCode answer',
    '',
    'Try it on your next problem',
]
ay = 700
for line in actions:
    if line:
        is_url = 'github.com' in line
        is_bold = 'Star' in line or 'Share' in line or 'Try' in line
        color = PURPLE_L if is_url else (GREEN if is_bold else LIGHT)
        d.text((W//2, ay), line, font=font(24, bold=is_bold), fill=color, anchor='mm')
    ay += 38

# Social proof line
draw_rr(d, [150, 990, 930, 1060], SURFACE, r=12, outline=PURPLE_D, width=1)
d.text((W//2, 1010), 'Open source  |  MIT License  |  Free forever', font=font(20, bold=True), fill=PURPLE_L, anchor='mm')
d.text((W//2, 1040), 'Built by @saiteja181', font=font(18), fill=GRAY, anchor='mm')

# Final CTA buttons
draw_rr(d, [200, 1100, 530, 1165], PURPLE, r=14)
d.text((365, 1132), 'Get HintCode Free', font=font(26, bold=True), fill=WHITE, anchor='mm')

draw_rr(d, [570, 1100, 880, 1165], BG_DARK, r=14, outline=PURPLE, width=2)
d.text((725, 1132), 'Star on GitHub', font=font(24, bold=True), fill=PURPLE_L, anchor='mm')

# Hashtags
d.text((W//2, 1210), '#coding #leetcode #opensource #students #ai #chrome', font=font(16), fill=DARK_GRAY, anchor='mm')

brand_footer(d)
slide_number(d, 10, TOTAL)
img.save('carousel-10-cta.png')
print('Slide 10 done')

print('\nAll 10 carousel slides generated!')
