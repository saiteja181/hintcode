from PIL import Image, ImageDraw, ImageFont
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_font(size):
    for name in ['segoeuib.ttf', 'segoeui.ttf', 'arialbd.ttf', 'arial.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

def get_light_font(size):
    for name in ['segoeui.ttf', 'segoeuil.ttf', 'arial.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

BG = (10, 10, 25)
PURPLE = (124, 58, 237)
PURPLE_LIGHT = (167, 139, 250)
PURPLE_GLOW = (90, 40, 180)
DARK_CARD = (18, 24, 48)
SURFACE = (15, 52, 96)
BORDER = (42, 42, 74)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
LIGHT_GRAY = (226, 232, 240)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
YELLOW = (250, 204, 21)
ORANGE = (255, 161, 22)
BLUE = (59, 130, 246)

def rr(d, xy, fill, radius=12, outline=None):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)

def draw_lightbulb(d, cx, cy, size):
    import math
    r = size // 2
    d.ellipse([cx-r, cy-r-4, cx+r, cy+r-4], fill=WHITE)
    bw = size // 3
    d.rectangle([cx-bw//2, cy+r-6, cx+bw//2, cy+r+size//5], fill=WHITE)
    for angle in [-40, 0, 40]:
        rad = math.radians(angle)
        x1 = cx + int(math.sin(rad) * (r + 4))
        y1 = cy - 4 - int(math.cos(rad) * (r + 4))
        x2 = cx + int(math.sin(rad) * (r + 12))
        y2 = cy - 4 - int(math.cos(rad) * (r + 12))
        d.line([x1, y1, x2, y2], fill=WHITE, width=max(2, size//10))


# ===== IMAGE 1: Hero / Hook Image (1200x1200 square for LinkedIn) =====
img = Image.new('RGB', (1200, 1200), BG)
d = ImageDraw.Draw(img)

# Subtle gradient glow at center
for i in range(200, 0, -1):
    alpha = int(12 * (1 - i/200))
    color = (PURPLE[0]//8 + alpha, PURPLE[1]//8, PURPLE[2]//4 + alpha)
    d.ellipse([600-i*2, 400-i*2, 600+i*2, 400+i*2], fill=color)

# Icon
d.ellipse([540, 80, 660, 200], fill=PURPLE)
draw_lightbulb(d, 600, 140, 40)

# Title
d.text((600, 240), 'HintCode', font=get_font(72), fill=WHITE, anchor='mt')
d.text((600, 320), 'Smart Coding Hints for Students', font=get_light_font(28), fill=PURPLE_LIGHT, anchor='mt')

# The hook — big text
lines = [
    ('Stop copying solutions.', WHITE),
    ('Start understanding them.', YELLOW),
]
y = 420
for text, color in lines:
    d.text((600, y), text, font=get_font(48), fill=color, anchor='mt')
    y += 65

# Feature cards in 2x2 grid
features = [
    ('Reads Your Code', 'Finds the exact buggy line'),
    ('3-Level Hints', 'Nudge > Approach > Guide'),
    ('5 Platforms', 'LC / HR / CF / CC / GFG'),
    ('100% Free', 'No card, no servers, open source'),
]
card_w, card_h = 480, 100
start_x, start_y = 120, 620
gap_x, gap_y = 520, 120
for i, (title, sub) in enumerate(features):
    col = i % 2
    row = i // 2
    x = start_x + col * gap_x
    y = start_y + row * gap_y
    rr(d, [x, y, x+card_w, y+card_h], DARK_CARD, 14, outline=BORDER)
    # Purple dot
    d.ellipse([x+18, y+28, x+38, y+48], fill=PURPLE)
    d.text((x+28, y+38), str(i+1), font=get_font(14), fill=WHITE, anchor='mm')
    d.text((x+54, y+26), title, font=get_font(22), fill=WHITE)
    d.text((x+54, y+56), sub, font=get_light_font(16), fill=GRAY)

# Bottom CTA
rr(d, [350, 1050, 850, 1110], PURPLE, 30)
d.text((600, 1080), 'github.com/saiteja181/hintcode', font=get_font(20), fill=WHITE, anchor='mm')

# Bottom tagline
d.text((600, 1150), 'Learn by thinking, not copying.', font=get_light_font(18), fill=GRAY, anchor='mt')

img.save('linkedin-1-hero.png')
print('Created linkedin-1-hero.png')


# ===== IMAGE 2: The Problem vs Solution (1200x1200) =====
img = Image.new('RGB', (1200, 1200), BG)
d = ImageDraw.Draw(img)

# Header
d.text((600, 50), 'How students practice DSA', font=get_font(36), fill=GRAY, anchor='mt')

# LEFT: The wrong way (red)
rr(d, [50, 120, 575, 700], (30, 15, 15), 16, outline=(100, 30, 30))
d.text((312, 150), 'Without HintCode', font=get_font(26), fill=RED, anchor='mt')

wrong_steps = [
    'Stuck on Two Sum',
    'Google "two sum solution"',
    'Copy-paste from GeeksforGeeks',
    'Submit. AC. Move on.',
    'See same pattern next week...',
    'Stuck again.',
    'Repeat forever.',
]
y = 210
for step in wrong_steps:
    d.ellipse([90, y+4, 106, y+20], fill=RED)
    d.text((120, y), step, font=get_light_font(20), fill=(255, 180, 180))
    y += 50

# RIGHT: The right way (green)
rr(d, [625, 120, 1150, 700], (15, 30, 15), 16, outline=(30, 100, 30))
d.text((887, 150), 'With HintCode', font=get_font(26), fill=GREEN, anchor='mt')

right_steps = [
    'Stuck on Two Sum',
    'Click "Get a Hint"',
    '"What if you remembered',
    '  what you already saw?"',
    'Think... hash map!',
    'Write the solution yourself.',
    'Actually understand it.',
]
y = 210
for step in right_steps:
    d.ellipse([665, y+4, 681, y+20], fill=GREEN)
    d.text((695, y), step, font=get_light_font(20), fill=(180, 255, 180))
    y += 50

# VS circle in the middle
d.ellipse([560, 380, 640, 460], fill=BG, outline=BORDER)
d.text((600, 420), 'vs', font=get_font(28), fill=GRAY, anchor='mm')

# Bottom section: the 3 hint levels
d.text((600, 740), '3 Levels of Progressive Hints', font=get_font(32), fill=WHITE, anchor='mt')

hint_data = [
    ('1', 'Gentle Nudge', '"Your line 4 resets to 0.', 'What happens with [-3,-1,-2]?"', (133, 77, 14), (254, 243, 199)),
    ('2', 'Approach', '"This is a Kadane\'s problem.', 'Your reset logic drops the answer."', (30, 64, 175), (219, 234, 254)),
    ('3', 'Detailed Guide', '"Step 1: Track current sum.', 'Step 2: Update max at each index..."', (107, 33, 168), (237, 233, 254)),
]
y = 810
for num, title, line1, line2, bg_color, text_color in hint_data:
    rr(d, [80, y, 1120, y+110], bg_color, 12)
    d.text((120, y+18), f'Hint {num}', font=get_font(20), fill=text_color)
    d.text((120, y+46), title, font=get_light_font(16), fill=text_color)
    d.text((380, y+22), line1, font=get_light_font(18), fill=text_color)
    d.text((380, y+50), line2, font=get_light_font(18), fill=text_color)
    y += 125

img.save('linkedin-2-comparison.png')
print('Created linkedin-2-comparison.png')


# ===== IMAGE 3: Code-Aware Demo (1200x1200) =====
img = Image.new('RGB', (1200, 1200), BG)
d = ImageDraw.Draw(img)

d.text((600, 40), 'It reads your actual code', font=get_font(38), fill=WHITE, anchor='mt')
d.text((600, 90), 'and pinpoints exactly where you went wrong', font=get_light_font(22), fill=GRAY, anchor='mt')

# Code editor mock
rr(d, [50, 140, 750, 620], (13, 17, 23), 14)
# Editor header bar
rr(d, [50, 140, 750, 185], (30, 30, 50), 14)
d.rectangle([50, 170, 750, 185], fill=(30, 30, 50))
d.ellipse([70, 152, 86, 168], fill=(255, 95, 87))
d.ellipse([96, 152, 112, 168], fill=(255, 189, 46))
d.ellipse([122, 152, 138, 168], fill=(39, 201, 63))
d.text((400, 162), 'max_subarray.cpp', font=get_light_font(14), fill=GRAY, anchor='mm')

# Code with line numbers - highlight the buggy line
code_lines = [
    ('1', 'class Solution {', False),
    ('2', 'public:', False),
    ('3', '    int maxSubArray(vector<int>& nums) {', False),
    ('4', '        int m = 0, ans = 0;', True),   # BUG LINE
    ('5', '        for (auto i : nums) {', False),
    ('6', '            m += i;', False),
    ('7', '            if (m < 0) m = 0;', True),  # BUG LINE
    ('8', '            ans = max(ans, m);', False),
    ('9', '        }', False),
    ('10', '        return ans;', False),
    ('11', '    }', False),
    ('12', '};', False),
]
y = 205
code_font = get_light_font(17)
for num, line, is_bug in code_lines:
    if is_bug:
        d.rectangle([50, y-2, 750, y+28], fill=(60, 20, 20))
        # Red arrow
        d.text((730, y+10), '<', font=get_font(22), fill=RED, anchor='mm')
    num_color = (100, 100, 120)
    d.text((75, y), num, font=code_font, fill=num_color, anchor='rt')
    line_color = (255, 200, 200) if is_bug else LIGHT_GRAY
    d.text((90, y), line, font=code_font, fill=line_color)
    y += 32

# Hint panel on the right
rr(d, [790, 140, 1150, 620], DARK_CARD, 14)
rr(d, [790, 140, 1150, 188], PURPLE, 14)
d.rectangle([790, 170, 1150, 188], fill=PURPLE)
d.text((970, 164), 'HintCode', font=get_font(18), fill=WHITE, anchor='mm')

# Hint 1 card
rr(d, [810, 205, 1130, 380], (40, 30, 5), 10, outline=(161, 98, 7))
d.text((825, 218), 'HINT 1 - NUDGE', font=get_font(13), fill=(254, 243, 199))

hint1_lines = [
    'Your line 4 initializes',
    'both m and ans to 0.',
    '',
    'What happens when the',
    'input is [-3, -1, -2]?',
    '',
    'Can the maximum subarray',
    'sum ever be negative?',
]
hy = 248
for line in hint1_lines:
    d.text((825, hy), line, font=get_light_font(15), fill=(254, 243, 199))
    hy += 22

# Arrow from buggy line to hint
d.line([750, 232, 790, 290], fill=RED, width=2)

# Hint 2 card (locked look)
rr(d, [810, 400, 1130, 450], (30, 64, 175), 10)
d.text((970, 425), 'Hint 2: Approach', font=get_font(16), fill=(219, 234, 254), anchor='mm')

# Hint 3 card (locked look)
rr(d, [810, 465, 1130, 515], (107, 33, 168), 10)
d.text((970, 490), 'Hint 3: Detailed Guide', font=get_font(16), fill=(237, 233, 254), anchor='mm')

# Solution button
rr(d, [810, 540, 1130, 590], DARK_CARD, 10, outline=BORDER)
d.text((970, 565), 'Reveal Solution', font=get_light_font(15), fill=GRAY, anchor='mm')

# Bottom section: key stats
d.text((600, 660), 'Why HintCode?', font=get_font(34), fill=WHITE, anchor='mt')

stats = [
    ('5', 'Platforms\nSupported', ORANGE),
    ('3', 'Hint Levels\nProgressive', PURPLE_LIGHT),
    ('0', 'Data\nCollected', GREEN),
    ('$0', 'Cost\nFree Forever', YELLOW),
]
sx = 150
for val, label, color in stats:
    d.text((sx, 740), val, font=get_font(52), fill=color, anchor='mt')
    lines = label.split('\n')
    d.text((sx, 800), lines[0], font=get_light_font(16), fill=LIGHT_GRAY, anchor='mt')
    d.text((sx, 822), lines[1], font=get_light_font(14), fill=GRAY, anchor='mt')
    sx += 260

# Platforms bar
platforms = [
    ('LeetCode', ORANGE),
    ('HackerRank', (0, 234, 100)),
    ('CodeForces', BLUE),
    ('CodeChef', (91, 70, 56)),
    ('GFG', (47, 141, 70)),
]
px = 110
py = 900
for name, color in platforms:
    w = len(name) * 12 + 40
    rr(d, [px, py, px+w, py+40], color, 8)
    d.text((px + w//2, py+20), name, font=get_font(15), fill=WHITE, anchor='mm')
    px += w + 16

# CTA
rr(d, [300, 1000, 900, 1070], PURPLE, 16)
d.text((600, 1020), 'github.com/saiteja181/hintcode', font=get_font(24), fill=WHITE, anchor='mt')
d.text((600, 1050), 'Star it. Share it. Help students learn.', font=get_light_font(15), fill=(200, 200, 255), anchor='mt')

# Footer
d.text((600, 1130), 'Open Source  |  MIT License  |  No Backend  |  No Tracking', font=get_light_font(14), fill=GRAY, anchor='mt')
d.text((600, 1160), 'Learn by thinking, not copying.', font=get_light_font(16), fill=PURPLE_LIGHT, anchor='mt')

img.save('linkedin-3-demo.png')
print('Created linkedin-3-demo.png')


# ===== IMAGE 4: Social proof / CTA carousel (1200x1200) =====
img = Image.new('RGB', (1200, 1200), BG)
d = ImageDraw.Draw(img)

# Big headline
d.text((600, 60), 'Every student deserves', font=get_font(42), fill=WHITE, anchor='mt')
d.text((600, 115), 'a mentor that doesn\'t', font=get_font(42), fill=WHITE, anchor='mt')
d.text((600, 170), 'spoil the answer.', font=get_font(42), fill=YELLOW, anchor='mt')

# Testimonial-style cards (fictional use cases)
cases = [
    ('"I was stuck on DP problems for weeks.\nHintCode taught me to think in subproblems\ninstead of memorizing solutions."', 'CSE Student, 3rd Year'),
    ('"The hint said: your line 7 resets to 0.\nWhat about all-negative arrays?\nThat one question unlocked Kadane\'s for me."', 'Competitive Programmer'),
    ('"I stopped using editorial sections.\nHintCode gives me just enough to\nfigure it out myself."', 'Self-taught Developer'),
]
y = 270
colors = [(40, 30, 5), (15, 25, 55), (35, 15, 45)]
borders = [(161, 98, 7), (59, 130, 246), (124, 58, 237)]
for i, (quote, role) in enumerate(cases):
    rr(d, [80, y, 1120, y+175], colors[i], 14, outline=borders[i])
    # Quote mark
    d.text((110, y+10), '"', font=get_font(48), fill=borders[i])
    # Quote text
    qlines = quote.replace('"', '').split('\n')
    qy = y + 25
    for ql in qlines:
        d.text((150, qy), ql, font=get_light_font(19), fill=LIGHT_GRAY)
        qy += 28
    # Role
    d.text((1090, y+145), '- ' + role, font=get_light_font(15), fill=GRAY, anchor='rt')
    y += 200

# How to get started
d.text((600, 890), 'Get started in 2 minutes', font=get_font(32), fill=WHITE, anchor='mt')

steps = [
    ('1', 'Clone the repo', 'or download ZIP'),
    ('2', 'Load in Chrome', 'chrome://extensions'),
    ('3', 'Add free API key', 'console.groq.com'),
    ('4', 'Get your first hint', 'on any LeetCode problem'),
]
sx = 150
for num, title, sub in steps:
    d.ellipse([sx-22, 955, sx+22, 999], fill=PURPLE)
    d.text((sx, 977), num, font=get_font(22), fill=WHITE, anchor='mm')
    d.text((sx, 1015), title, font=get_font(16), fill=WHITE, anchor='mt')
    d.text((sx, 1040), sub, font=get_light_font(13), fill=GRAY, anchor='mt')
    if num != '4':
        d.line([sx+30, 977, sx+180, 977], fill=BORDER, width=2)
    sx += 250

# CTA
rr(d, [250, 1095, 950, 1165], PURPLE, 30)
d.text((600, 1118), 'github.com/saiteja181/hintcode', font=get_font(26), fill=WHITE, anchor='mt')
d.text((600, 1148), 'Star it if you think students deserve better tools', font=get_light_font(14), fill=(200, 200, 255), anchor='mt')

img.save('linkedin-4-cta.png')
print('Created linkedin-4-cta.png')

print('\nAll 4 LinkedIn images done!')
