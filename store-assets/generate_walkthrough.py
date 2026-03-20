from PIL import Image, ImageDraw, ImageFont
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_font(size):
    for name in ['segoeuib.ttf', 'arialbd.ttf', 'segoeui.ttf', 'arial.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

def get_light_font(size):
    for name in ['segoeui.ttf', 'arial.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

BG = (10, 10, 25)
PURPLE = (124, 58, 237)
PURPLE_LIGHT = (167, 139, 250)
DARK_CARD = (18, 24, 48)
SURFACE = (15, 52, 96)
BORDER = (42, 42, 74)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
LIGHT = (226, 232, 240)
RED = (239, 68, 68)
GREEN = (34, 197, 94)
YELLOW = (250, 204, 21)
ORANGE = (255, 161, 22)

def rr(d, xy, fill, radius=12, outline=None):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)

def draw_arrow(d, x1, y1, x2, y2, color=RED, width=3, head_size=12):
    """Draw arrow from (x1,y1) to (x2,y2)"""
    import math
    d.line([x1, y1, x2, y2], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    a1 = angle + math.pi * 0.8
    a2 = angle - math.pi * 0.8
    d.polygon([
        (x2, y2),
        (x2 + head_size * math.cos(a1), y2 + head_size * math.sin(a1)),
        (x2 + head_size * math.cos(a2), y2 + head_size * math.sin(a2)),
    ], fill=color)

def draw_circle_number(d, cx, cy, num, bg=PURPLE, r=24):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=bg)
    d.text((cx, cy), str(num), font=get_font(22), fill=WHITE, anchor='mm')

pages = []

# ===== PAGE 1: Title =====
img = Image.new('RGB', (1200, 1600), BG)
d = ImageDraw.Draw(img)

d.text((600, 200), 'HintCode', font=get_font(72), fill=WHITE, anchor='mt')
d.text((600, 290), 'Installation Guide', font=get_font(36), fill=PURPLE_LIGHT, anchor='mt')
d.text((600, 360), 'Get set up in under 2 minutes', font=get_light_font(22), fill=GRAY, anchor='mt')

# Steps overview
steps = [
    'Download the extension',
    'Open Chrome Extensions page',
    'Enable Developer Mode',
    'Load the extension',
    'Get your free API key',
    'Configure & test',
    'Start getting hints!',
]
y = 500
for i, step in enumerate(steps):
    draw_circle_number(d, 200, y, i+1)
    d.text((245, y), step, font=get_light_font(26), fill=LIGHT, anchor='lm')
    if i < len(steps) - 1:
        d.line([200, y+28, 200, y+62], fill=BORDER, width=2)
    y += 90

d.text((600, 1350), 'Next: Step-by-step with screenshots', font=get_light_font(18), fill=GRAY, anchor='mt')
draw_arrow(d, 600, 1390, 600, 1440, PURPLE_LIGHT, 2, 10)

rr(d, [200, 1480, 1000, 1540], DARK_CARD, 12, outline=BORDER)
d.text((600, 1510), 'github.com/saiteja181/hintcode', font=get_font(20), fill=PURPLE_LIGHT, anchor='mm')

pages.append(img)


# ===== PAGE 2: Download =====
img = Image.new('RGB', (1200, 1600), BG)
d = ImageDraw.Draw(img)

draw_circle_number(d, 80, 50, 1, r=28)
d.text((125, 50), 'Download the Extension', font=get_font(32), fill=WHITE, anchor='lm')

# Mock GitHub page
rr(d, [50, 110, 1150, 600], DARK_CARD, 14, outline=BORDER)

# GitHub header bar
rr(d, [50, 110, 1150, 165], (22, 27, 34), 14)
d.rectangle([50, 150, 1150, 165], fill=(22, 27, 34))
d.text((80, 138), 'github.com/saiteja181/hintcode', font=get_light_font(16), fill=GRAY, anchor='lm')

# Repo content mockup
d.text((100, 190), 'saiteja181 / hintcode', font=get_font(22), fill=WHITE)
rr(d, [100, 230, 300, 260], (21, 32, 43), 6, outline=(48, 54, 61))
d.text((200, 245), 'Public', font=get_light_font(12), fill=GRAY, anchor='mm')

# Star button
rr(d, [850, 230, 980, 265], (33, 38, 45), 6, outline=(48, 54, 61))
d.text((915, 248), 'Star', font=get_light_font(14), fill=LIGHT, anchor='mm')

# Green Code button
rr(d, [850, 300, 1050, 345], GREEN, 8)
d.text((950, 323), 'Code', font=get_font(18), fill=WHITE, anchor='mm')

# Dropdown
rr(d, [750, 355, 1100, 560], (22, 27, 34), 10, outline=(48, 54, 61))
d.text((770, 375), 'Clone', font=get_font(14), fill=LIGHT)
rr(d, [770, 400, 1080, 435], (13, 17, 23), 6, outline=(48, 54, 61))
d.text((785, 418), 'https://github.com/saiteja181/hintcode.git', font=get_light_font(11), fill=GRAY, anchor='lm')

# Download ZIP highlighted
rr(d, [770, 500, 960, 540], (40, 50, 30), 6, outline=GREEN)
d.text((865, 520), 'Download ZIP', font=get_font(16), fill=GREEN, anchor='mm')

# Arrow pointing to Download ZIP
draw_arrow(d, 650, 520, 760, 520, RED, 3)
d.text((520, 510), 'Click here!', font=get_font(20), fill=RED, anchor='rm')

# Instructions below
d.text((100, 640), 'Option A: Download ZIP', font=get_font(24), fill=YELLOW)
d.text((100, 680), '1. Click the green "Code" button on the repo page', font=get_light_font(18), fill=LIGHT)
d.text((100, 710), '2. Click "Download ZIP"', font=get_light_font(18), fill=LIGHT)
d.text((100, 740), '3. Extract the ZIP to any folder on your computer', font=get_light_font(18), fill=LIGHT)

d.text((100, 800), 'Option B: Git Clone', font=get_font(24), fill=YELLOW)
rr(d, [100, 840, 900, 880], (13, 17, 23), 8)
d.text((120, 852), 'git clone https://github.com/saiteja181/hintcode.git', font=get_light_font(16), fill=GREEN, anchor='lm')

pages.append(img)


# ===== PAGE 3: Chrome Extensions Page =====
img = Image.new('RGB', (1200, 1600), BG)
d = ImageDraw.Draw(img)

draw_circle_number(d, 80, 50, 2, r=28)
d.text((125, 50), 'Open Chrome Extensions', font=get_font(32), fill=WHITE, anchor='lm')

# Chrome address bar mock
rr(d, [50, 120, 1150, 250], (22, 27, 34), 14, outline=BORDER)
rr(d, [80, 150, 1120, 195], (13, 17, 23), 22)

# URL highlighted
rr(d, [90, 155, 520, 190], (40, 30, 10), 18, outline=ORANGE)
d.text((100, 172), 'chrome://extensions/', font=get_font(18), fill=ORANGE, anchor='lm')

draw_arrow(d, 520, 172, 600, 172, RED, 3)
d.text((620, 172), 'Type this in the address bar', font=get_font(18), fill=RED, anchor='lm')

# Extensions page mock
rr(d, [50, 290, 1150, 800], DARK_CARD, 14, outline=BORDER)
d.text((100, 320), 'Extensions', font=get_font(28), fill=WHITE)

# Developer mode toggle
rr(d, [850, 310, 1100, 350], (22, 27, 34), 8, outline=BORDER)
d.text((870, 330), 'Developer mode', font=get_light_font(15), fill=LIGHT, anchor='lm')

# Toggle switch (OFF)
rr(d, [1040, 318, 1090, 342], (80, 80, 80), 12)
d.ellipse([1042, 320, 1062, 340], fill=(200, 200, 200))

draw_circle_number(d, 50, 330, 3, GREEN, 20)
draw_arrow(d, 800, 330, 1030, 330, GREEN, 3)
d.text((770, 320), 'Turn ON', font=get_font(20), fill=GREEN, anchor='rm')

# After enabling - show the buttons
d.text((100, 400), 'After enabling Developer mode, 3 buttons appear:', font=get_light_font(18), fill=GRAY)

# Load unpacked button (highlighted)
rr(d, [100, 450, 310, 500], (40, 30, 60), 8, outline=PURPLE)
d.text((205, 475), 'Load unpacked', font=get_font(16), fill=PURPLE_LIGHT, anchor='mm')

rr(d, [340, 450, 520, 500], DARK_CARD, 8, outline=BORDER)
d.text((430, 475), 'Pack extension', font=get_light_font(15), fill=GRAY, anchor='mm')

rr(d, [550, 450, 700, 500], DARK_CARD, 8, outline=BORDER)
d.text((625, 475), 'Update', font=get_light_font(15), fill=GRAY, anchor='mm')

draw_circle_number(d, 50, 475, 4, PURPLE, 20)
draw_arrow(d, 80, 475, 95, 475, PURPLE, 3)

d.text((100, 540), 'Click "Load unpacked"', font=get_font(22), fill=PURPLE_LIGHT)
d.text((100, 575), 'Select the folder where you extracted/cloned HintCode', font=get_light_font(18), fill=LIGHT)

# Folder picker mock
rr(d, [100, 620, 800, 780], (13, 17, 23), 10, outline=BORDER)
d.text((120, 640), 'Select Folder', font=get_font(16), fill=LIGHT)
d.text((120, 675), 'C:\\Users\\you\\Downloads\\', font=get_light_font(14), fill=GRAY)

# Folder items
folders = ['Documents', 'Downloads', 'hintcode']
fy = 710
for folder in folders:
    icon_color = GRAY if folder != 'hintcode' else YELLOW
    text_color = GRAY if folder != 'hintcode' else YELLOW
    d.text((160, fy), folder, font=get_light_font(16), fill=text_color)
    if folder == 'hintcode':
        rr(d, [140, fy-4, 760, fy+24], (40, 40, 10), 4, outline=YELLOW)
        draw_arrow(d, 780, fy+10, 770, fy+10, RED, 2, 8)
        d.text((820, fy+5), 'Select this!', font=get_font(14), fill=RED, anchor='lm')
    fy += 34

pages.append(img)


# ===== PAGE 4: Get API Key =====
img = Image.new('RGB', (1200, 1600), BG)
d = ImageDraw.Draw(img)

draw_circle_number(d, 80, 50, 5, r=28)
d.text((125, 50), 'Get Your Free API Key', font=get_font(32), fill=WHITE, anchor='lm')

d.text((100, 110), 'HintCode uses Groq AI (completely free, no credit card needed)', font=get_light_font(18), fill=GRAY)

# Step A: Go to Groq
d.text((100, 170), 'A. Go to console.groq.com/keys', font=get_font(22), fill=YELLOW)

# Mock Groq page
rr(d, [50, 210, 1150, 550], DARK_CARD, 14, outline=BORDER)
rr(d, [50, 210, 1150, 260], (15, 15, 30), 14)
d.rectangle([50, 245, 1150, 260], fill=(15, 15, 30))
d.text((80, 235), 'console.groq.com/keys', font=get_light_font(14), fill=GRAY, anchor='lm')

d.text((100, 285), 'API Keys', font=get_font(24), fill=WHITE)
d.text((100, 320), 'Create and manage your API keys', font=get_light_font(16), fill=GRAY)

# Create API key button
rr(d, [100, 365, 340, 415], PURPLE, 10)
d.text((220, 390), 'Create API Key', font=get_font(18), fill=WHITE, anchor='mm')
draw_arrow(d, 360, 390, 400, 390, RED, 3)
d.text((420, 385), 'Click this!', font=get_font(18), fill=RED, anchor='lm')

# Generated key
rr(d, [100, 445, 900, 490], (13, 17, 23), 8, outline=BORDER)
d.text((120, 468), 'gsk_abc123xyz456...your_key_here', font=get_light_font(16), fill=GREEN, anchor='lm')

rr(d, [920, 450, 1020, 485], SURFACE, 8, outline=BORDER)
d.text((970, 468), 'Copy', font=get_light_font(14), fill=LIGHT, anchor='mm')
draw_arrow(d, 1040, 468, 1080, 468, RED, 3)
d.text((1090, 462), 'Copy it!', font=get_font(14), fill=RED, anchor='lm')

# Step B: Paste in HintCode settings
d.text((100, 580), 'B. Open HintCode Settings', font=get_font(22), fill=YELLOW)
d.text((100, 620), 'Click HintCode icon in Chrome toolbar > Settings', font=get_light_font(18), fill=LIGHT)

# Mock settings
rr(d, [50, 670, 1150, 1200], DARK_CARD, 14, outline=BORDER)
d.text((600, 700), 'HintCode Settings', font=get_font(24), fill=WHITE, anchor='mt')

d.text((100, 750), 'PROVIDER', font=get_font(12), fill=GRAY)
rr(d, [100, 775, 700, 815], SURFACE, 8, outline=BORDER)
d.text((120, 795), 'Groq (Free, no card needed)', font=get_light_font(16), fill=LIGHT, anchor='lm')

d.text((100, 845), 'API KEY', font=get_font(12), fill=GRAY)
rr(d, [100, 870, 700, 910], SURFACE, 8, outline=GREEN)
d.text((120, 890), 'gsk_abc123xyz456...', font=get_light_font(16), fill=GREEN, anchor='lm')
draw_arrow(d, 720, 890, 760, 890, RED, 3)
d.text((780, 885), 'Paste your key here', font=get_font(16), fill=RED, anchor='lm')

# Save + Test buttons
rr(d, [100, 940, 280, 985], PURPLE, 10)
d.text((190, 963), 'Save Key', font=get_font(18), fill=WHITE, anchor='mm')
draw_circle_number(d, 60, 963, 1, GREEN, 16)
draw_arrow(d, 78, 963, 95, 963, GREEN, 2, 8)

rr(d, [300, 940, 520, 985], BG, 10, outline=PURPLE)
d.text((410, 963), 'Test Connection', font=get_font(16), fill=PURPLE_LIGHT, anchor='mm')
draw_circle_number(d, 545, 963, 2, GREEN, 16)
draw_arrow(d, 530, 963, 525, 963, GREEN, 2, 8)

# Success message
rr(d, [100, 1010, 700, 1050], (15, 50, 25), 8)
d.text((400, 1030), 'Connection successful! AI is ready.', font=get_font(16), fill=GREEN, anchor='mm')

# Final instruction
rr(d, [50, 1280, 1150, 1400], (20, 35, 15), 14, outline=GREEN)
d.text((600, 1310), 'You are all set!', font=get_font(28), fill=GREEN, anchor='mt')
d.text((600, 1350), 'Go to any LeetCode problem and click "Stuck? Get a Hint"', font=get_light_font(18), fill=LIGHT, anchor='mt')

pages.append(img)


# ===== PAGE 5: Using HintCode =====
img = Image.new('RGB', (1200, 1600), BG)
d = ImageDraw.Draw(img)

draw_circle_number(d, 80, 50, 7, r=28)
d.text((125, 50), 'Start Getting Hints!', font=get_font(32), fill=WHITE, anchor='lm')

d.text((100, 110), 'Navigate to any coding problem on a supported platform', font=get_light_font(18), fill=GRAY)

# Mock LeetCode page with floating button
rr(d, [50, 160, 1150, 700], (13, 17, 23), 14, outline=BORDER)
# Header
rr(d, [50, 160, 1150, 210], (22, 22, 30), 14)
d.rectangle([50, 195, 1150, 210], fill=(22, 22, 30))
d.text((80, 185), 'leetcode.com/problems/maximum-subarray/', font=get_light_font(14), fill=GRAY, anchor='lm')

d.text((100, 230), '53. Maximum Subarray', font=get_font(22), fill=WHITE)
d.text((100, 265), 'Medium', font=get_font(14), fill=ORANGE)

d.text((100, 310), 'Given an integer array nums, find the subarray', font=get_light_font(16), fill=LIGHT)
d.text((100, 335), 'with the largest sum, and return its sum.', font=get_light_font(16), fill=LIGHT)

# Code area
rr(d, [100, 380, 750, 650], (8, 12, 18), 8, outline=BORDER)
code = [
    'class Solution {',
    'public:',
    '    int maxSubArray(vector<int>& nums) {',
    '        int m = 0, ans = 0;',
    '        for (auto i : nums) {',
    '            m += i;',
    '            if (m < 0) m = 0;',
    '            ans = max(ans, m);',
    '        }',
    '        return ans;',
    '    }',
    '};',
]
cy = 395
for line in code:
    d.text((120, cy), line, font=get_light_font(14), fill=LIGHT)
    cy += 22

# Floating button (highlighted)
rr(d, [850, 620, 1100, 670], PURPLE, 25, outline=YELLOW)
d.text((975, 645), 'Stuck? Get a Hint', font=get_font(16), fill=WHITE, anchor='mm')
draw_arrow(d, 820, 560, 870, 620, RED, 3)
d.text((700, 545), 'Click this button!', font=get_font(22), fill=RED, anchor='rm')
d.text((700, 575), '(appears automatically)', font=get_light_font(15), fill=GRAY, anchor='rm')

# Below: hint panel
d.text((100, 740), 'The side panel opens with your hints:', font=get_font(20), fill=LIGHT)

# Hint flow
hints = [
    ('Hint 1', 'Gentle Nudge', '"Your line 4 initializes ans to 0. What if all numbers are negative?"', (133, 77, 14), (254, 243, 199)),
    ('Hint 2', 'Approach', '"Use Kadane\'s algorithm. Track max ending here vs global max."', (30, 64, 175), (219, 234, 254)),
    ('Hint 3', 'Detailed', '"Line 7 resets m to 0. Instead, take max(current element, sum + current)."', (107, 33, 168), (237, 233, 254)),
]
hy = 790
for title, sub, text, bg, fg in hints:
    rr(d, [50, hy, 1150, hy+120], bg, 12)
    d.text((80, hy+15), title, font=get_font(20), fill=fg)
    d.text((80, hy+42), sub, font=get_light_font(14), fill=fg)
    d.text((80, hy+72), text, font=get_light_font(16), fill=fg)
    hy += 140

# Progressive arrows between hints
draw_arrow(d, 600, 910, 600, 925, LIGHT, 2, 8)
draw_arrow(d, 600, 1050, 600, 1065, LIGHT, 2, 8)

# Bottom message
rr(d, [150, 1250, 1050, 1350], DARK_CARD, 16, outline=PURPLE)
d.text((600, 1275), 'Each hint gets more specific.', font=get_font(22), fill=WHITE, anchor='mt')
d.text((600, 1310), 'Try to solve it yourself before moving to the next level!', font=get_light_font(17), fill=GRAY, anchor='mt')

# Footer CTA
rr(d, [300, 1430, 900, 1490], PURPLE, 25)
d.text((600, 1450), 'github.com/saiteja181/hintcode', font=get_font(20), fill=WHITE, anchor='mt')
d.text((600, 1475), 'Star it. Share it. Help students learn.', font=get_light_font(13), fill=(200, 200, 255), anchor='mt')

pages.append(img)

# Save as individual images (since PIL PDF support varies)
for i, page in enumerate(pages):
    page.save(f'walkthrough-{i+1}.png')
    print(f'Created walkthrough-{i+1}.png')

# Also try to save as PDF
try:
    rgb_pages = [p.convert('RGB') for p in pages]
    rgb_pages[0].save('HintCode_Installation_Guide.pdf', save_all=True, append_images=rgb_pages[1:], resolution=150)
    print('Created HintCode_Installation_Guide.pdf')
except Exception as e:
    print(f'PDF creation skipped: {e}')
    print('Use the individual PNG files instead')

print('\nDone! All walkthrough images created.')
