from PIL import Image, ImageDraw, ImageFont
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_font(size):
    for name in ['segoeui.ttf', 'segoeuib.ttf', 'arial.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

def get_bold_font(size):
    for name in ['segoeuib.ttf', 'arialbd.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return get_font(size)

BG = (26, 26, 46)
PURPLE = (124, 58, 237)
PURPLE_LIGHT = (167, 139, 250)
DARK_CARD = (22, 33, 62)
SURFACE = (15, 52, 96)
BORDER = (42, 42, 74)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
LIGHT_GRAY = (226, 232, 240)

def draw_rr(d, xy, fill, radius=12, outline=None):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


# ===== Screenshot 1: Progressive Hints =====
img = Image.new('RGB', (1280, 800), BG)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, 1280, 70], fill=(15, 15, 30))
d.text((640, 35), 'Get Progressive Hints When You Are Stuck',
       font=get_bold_font(28), fill=WHITE, anchor='mm')

# Left: mock code editor
draw_rr(d, [40, 100, 780, 740], (13, 17, 23), 14)
draw_rr(d, [40, 100, 780, 145], (30, 30, 50), 14)
d.rectangle([40, 130, 780, 145], fill=(30, 30, 50))
d.ellipse([60, 112, 76, 128], fill=(255, 95, 87))
d.ellipse([86, 112, 102, 128], fill=(255, 189, 46))
d.ellipse([112, 112, 128, 128], fill=(39, 201, 63))
d.text((420, 122), 'two_sum.py', font=get_font(14), fill=GRAY, anchor='mm')

code_lines = [
    ('  1', 'def two_sum(nums, target):'),
    ('  2', '    for i in range(len(nums)):'),
    ('  3', '        for j in range(i+1, len(nums)):'),
    ('  4', '            if nums[i] + nums[j] == target:'),
    ('  5', '                return [i, j]'),
    ('  6', '    return []'),
    ('  7', ''),
    ('  8', '# This works but is O(n^2)...'),
    ('  9', '# How can I make it faster?'),
]
y = 165
f_code = get_font(16)
for num, line in code_lines:
    d.text((60, y), num, font=f_code, fill=(100, 100, 120))
    color = (92, 99, 112) if line.startswith('#') else LIGHT_GRAY
    d.text((105, y), line, font=f_code, fill=color)
    y += 28

# Right: hint panel
px, py = 820, 100
pw, ph = 420, 640
draw_rr(d, [px, py, px+pw, py+ph], DARK_CARD, 14)
draw_rr(d, [px, py, px+pw, py+48], PURPLE, 14)
d.rectangle([px, py+30, px+pw, py+48], fill=PURPLE)
d.text((px+pw//2, py+24), 'HintCode', font=get_bold_font(18), fill=WHITE, anchor='mm')

hint_data = [
    ((133, 77, 14), 'Hint 1: Gentle Nudge', 'Think differently'),
    ((30, 64, 175), 'Hint 2: Approach', 'Name the technique'),
    ((107, 33, 168), 'Hint 3: Detailed Guide', 'Step-by-step'),
]
by = py + 65
for color, label, sub in hint_data:
    draw_rr(d, [px+16, by, px+pw-16, by+50], color, 10)
    d.text((px+30, by+15), label, font=get_bold_font(16), fill=WHITE)
    d.text((px+pw-30, by+18), sub, font=get_font(12), fill=WHITE, anchor='rt')
    by += 62

by += 10
draw_rr(d, [px+16, by, px+pw-16, by+180], (40, 30, 5), 10, outline=(161, 98, 7))
d.text((px+30, by+14), 'HINT 1 - GENTLE NUDGE', font=get_bold_font(12), fill=(254, 243, 199))
hint_lines = [
    'Think about what you are really',
    'searching for with each element.',
    '',
    'If you know the target and one',
    'number, do you already know what',
    'the other number must be?',
    '',
    'Is there a way to remember what',
    "you have already seen?",
]
hy = by + 38
for line in hint_lines:
    d.text((px+30, hy), line, font=get_font(14), fill=(254, 243, 199))
    hy += 20

d.rectangle([0, 770, 1280, 800], fill=(15, 15, 30))
d.text((640, 785), 'HintCode - Learn by thinking, not copying',
       font=get_font(13), fill=GRAY, anchor='mm')

img.save('screenshot-1-1280x800.png')
print('Created screenshot-1')


# ===== Screenshot 2: Supported Platforms =====
img = Image.new('RGB', (1280, 800), BG)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, 1280, 70], fill=(15, 15, 30))
d.text((640, 35), 'Works on 5 Major Coding Platforms',
       font=get_bold_font(28), fill=WHITE, anchor='mm')

platforms = [
    ('LC', (255, 161, 22), 'LeetCode'),
    ('HR', (0, 234, 100), 'HackerRank'),
    ('CF', (24, 144, 255), 'CodeForces'),
    ('CC', (91, 70, 56), 'CodeChef'),
    ('GFG', (47, 141, 70), 'GeeksforGeeks'),
]
start_x = 140
gap = 240
cy = 340
for i, (initials, color, name) in enumerate(platforms):
    cx = start_x + i * gap
    r = 70
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    d.text((cx, cy), initials, font=get_bold_font(36), fill=WHITE, anchor='mm')
    d.text((cx, cy+r+25), name, font=get_bold_font(18), fill=LIGHT_GRAY, anchor='mt')
    d.text((cx, cy+r+55), 'Supported', font=get_font(14), fill=(34, 197, 94), anchor='mt')

d.text((640, 550), 'Auto-detects problems, code, and language from each platform',
       font=get_font(18), fill=GRAY, anchor='mt')

cards = ['Auto-Detection', 'Side Panel UI', 'Hint Caching', 'Manual Mode']
for i, label in enumerate(cards):
    cx = 200 + i * 230
    draw_rr(d, [cx-90, 620, cx+90, 680], DARK_CARD, 10, outline=BORDER)
    d.text((cx, 650), label, font=get_bold_font(15), fill=PURPLE_LIGHT, anchor='mm')

d.rectangle([0, 770, 1280, 800], fill=(15, 15, 30))
d.text((640, 785), 'HintCode - Learn by thinking, not copying',
       font=get_font(13), fill=GRAY, anchor='mm')

img.save('screenshot-2-1280x800.png')
print('Created screenshot-2')


# ===== Screenshot 3: Easy Setup =====
img = Image.new('RGB', (1280, 800), BG)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, 1280, 70], fill=(15, 15, 30))
d.text((640, 35), 'Easy Setup - Just Add Your Free API Key',
       font=get_bold_font(28), fill=WHITE, anchor='mm')

# Settings card
cx, cy = 500, 420
cw, ch = 520, 480
draw_rr(d, [cx-cw//2, cy-ch//2, cx+cw//2, cy+ch//2], DARK_CARD, 16, outline=BORDER)

d.text((cx, cy-ch//2+40), 'HintCode Settings',
       font=get_bold_font(24), fill=WHITE, anchor='mm')

ly = cy - ch//2 + 80
d.text((cx-cw//2+30, ly), 'GROK API KEY', font=get_bold_font(12), fill=GRAY)
ly += 28
draw_rr(d, [cx-cw//2+30, ly, cx+cw//2-100, ly+42], SURFACE, 8)
d.text((cx-cw//2+45, ly+12), 'xai-xxxxxxxxxxxxxxxxxxxxxxxx', font=get_font(15), fill=GRAY)
draw_rr(d, [cx+cw//2-90, ly, cx+cw//2-30, ly+42], SURFACE, 8)
d.text((cx+cw//2-60, ly+12), 'Show', font=get_font(14), fill=GRAY, anchor='mt')

ly += 55
d.text((cx-cw//2+30, ly), 'Get your free API key at console.x.ai',
       font=get_font(14), fill=PURPLE_LIGHT)

ly += 40
draw_rr(d, [cx-cw//2+30, ly, cx-cw//2+170, ly+42], PURPLE, 8)
d.text((cx-cw//2+100, ly+12), 'Save Key', font=get_bold_font(15), fill=WHITE, anchor='mt')
draw_rr(d, [cx-cw//2+185, ly, cx-cw//2+360, ly+42], BG, 8, outline=PURPLE)
d.text((cx-cw//2+272, ly+12), 'Test Connection',
       font=get_bold_font(14), fill=PURPLE_LIGHT, anchor='mt')

ly += 55
draw_rr(d, [cx-cw//2+30, ly, cx+cw//2-30, ly+36], (15, 60, 30), 6)
d.text((cx, ly+10), 'Connection successful! Grok is ready.',
       font=get_font(14), fill=(34, 197, 94), anchor='mt')

ly += 55
d.text((cx-cw//2+30, ly), 'AI MODEL', font=get_bold_font(12), fill=GRAY)
ly += 28
draw_rr(d, [cx-cw//2+30, ly, cx+cw//2-30, ly+42], SURFACE, 8)
d.text((cx-cw//2+45, ly+12), 'grok-3-mini (recommended)',
       font=get_font(15), fill=LIGHT_GRAY)

# Steps on right
steps = [
    ('1', 'Install extension'),
    ('2', 'Get free API key'),
    ('3', 'Paste & save'),
    ('4', 'Start learning!'),
]
sx = 960
sy = 220
for num, label in steps:
    d.ellipse([sx-18, sy-18, sx+18, sy+18], fill=PURPLE)
    d.text((sx, sy), num, font=get_bold_font(18), fill=WHITE, anchor='mm')
    d.text((sx+35, sy), label, font=get_font(17), fill=LIGHT_GRAY, anchor='lm')
    if num != '4':
        d.line([sx, sy+22, sx, sy+52], fill=BORDER, width=2)
    sy += 70

d.text((960, sy+20), 'Free tier available',
       font=get_bold_font(16), fill=(34, 197, 94), anchor='mt')
d.text((960, sy+45), 'No credit card needed',
       font=get_font(14), fill=GRAY, anchor='mt')

d.rectangle([0, 770, 1280, 800], fill=(15, 15, 30))
d.text((640, 785), 'HintCode - Learn by thinking, not copying',
       font=get_font(13), fill=GRAY, anchor='mm')

img.save('screenshot-3-1280x800.png')
print('Created screenshot-3')
print('All screenshots done!')
