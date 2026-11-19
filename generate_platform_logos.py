import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
STATICFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles', 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATICFILES_DIR, exist_ok=True)

def get_font(size, bold=True):
    font_paths = [
        'C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/calibrib.ttf' if bold else 'C:/Windows/Fonts/calibri.ttf',
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_retail_mark(draw, cx, cy, radius, primary_color, secondary_color):
    """Faceted geometric modern hexagonal prism with POS till scanner diamond"""
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    
    # Outer hexagon glow / fill
    draw.polygon(points, fill=(14, 165, 233, 40), outline=primary_color, width=max(4, int(radius * 0.08)))
    
    # Inner facets
    for i in range(6):
        draw.line([points[i], (cx, cy)], fill=(56, 189, 248, 180), width=max(3, int(radius * 0.04)))
    
    # Center diamond / till core
    r_in = radius * 0.45
    inner_pts = [
        (cx, cy - r_in),
        (cx + r_in, cy),
        (cx, cy + r_in),
        (cx - r_in, cy)
    ]
    draw.polygon(inner_pts, fill=secondary_color, outline=(255, 255, 255, 240), width=max(3, int(radius * 0.05)))

def draw_wholesale_mark(draw, cx, cy, radius, primary_color, secondary_color):
    """Isometric enterprise distribution cube with nodes"""
    # 3D isometric cube
    h = radius * 0.85
    w = radius * 0.95
    top_face = [(cx, cy - h), (cx + w, cy - h * 0.45), (cx, cy + h * 0.1), (cx - w, cy - h * 0.45)]
    left_face = [(cx - w, cy - h * 0.45), (cx, cy + h * 0.1), (cx, cy + h), (cx - w, cy + h * 0.45)]
    right_face = [(cx + w, cy - h * 0.45), (cx, cy + h * 0.1), (cx, cy + h), (cx + w, cy + h * 0.45)]

    draw.polygon(top_face, fill=(96, 165, 250, 160), outline=(255, 255, 255, 220), width=max(4, int(radius * 0.06)))
    draw.polygon(left_face, fill=(37, 99, 235, 200), outline=(255, 255, 255, 180), width=max(4, int(radius * 0.06)))
    draw.polygon(right_face, fill=(29, 78, 216, 230), outline=(255, 255, 255, 200), width=max(4, int(radius * 0.06)))

    # Central distribution node
    draw.ellipse([cx - radius * 0.2, cy - radius * 0.2, cx + radius * 0.2, cy + radius * 0.2], fill=(255, 255, 255, 255))

def draw_transporter_mark(draw, cx, cy, radius, primary_color, secondary_color):
    """Aerodynamic velocity delta arrow with route waypoint"""
    pts = [
        (cx - radius * 0.8, cy + radius * 0.85),
        (cx, cy - radius * 0.9),
        (cx + radius * 0.8, cy + radius * 0.85),
        (cx, cy + radius * 0.35)
    ]
    draw.polygon(pts, fill=(13, 148, 136, 180), outline=(45, 212, 191, 255), width=max(5, int(radius * 0.08)))
    
    # Internal route line
    draw.line([(cx, cy - radius * 0.5), (cx, cy + radius * 0.3)], fill=(255, 255, 255, 240), width=max(4, int(radius * 0.06)))
    draw.ellipse([cx - radius * 0.15, cy - radius * 0.5 - radius * 0.15, cx + radius * 0.15, cy - radius * 0.5 + radius * 0.15], fill=(255, 255, 255, 255))

def draw_community_mark(draw, cx, cy, radius, primary_color, secondary_color):
    """Harmonic interconnected tri-portal shield"""
    # Outer shield
    shield_pts = [
        (cx - radius * 0.85, cy - radius * 0.8),
        (cx + radius * 0.85, cy - radius * 0.8),
        (cx + radius * 0.75, cy + radius * 0.1),
        (cx, cy + radius * 0.9),
        (cx - radius * 0.75, cy + radius * 0.1)
    ]
    draw.polygon(shield_pts, fill=(124, 58, 237, 160), outline=(167, 139, 250, 240), width=max(5, int(radius * 0.08)))
    
    # Inner triad rings
    r_sub = radius * 0.25
    offsets = [(0, -r_sub), (-r_sub * 0.9, r_sub * 0.7), (r_sub * 0.9, r_sub * 0.7)]
    for ox, oy in offsets:
        draw.ellipse([cx + ox - r_sub, cy + oy - r_sub, cx + ox + r_sub, cy + oy + r_sub], outline=(255, 255, 255, 230), width=max(3, int(radius * 0.05)))

PLATFORMS = [
    {
        'key': 'retail',
        'sub': 'RETAIL LAN',
        'desc': 'COUNTER POS & STOCK',
        'mark_func': draw_retail_mark,
        'pri': (14, 165, 233, 255),    # Light Blue / Sky
        'sec': (56, 189, 248, 255),
    },
    {
        'key': 'wholesale',
        'sub': 'WHOLESALE LAN',
        'desc': 'WAREHOUSE & SUPPLY',
        'mark_func': draw_wholesale_mark,
        'pri': (37, 99, 235, 255),    # Cobalt
        'sec': (96, 165, 250, 255),
    },
    {
        'key': 'transporter',
        'sub': 'TRANSPORTER HUB',
        'desc': 'FLEET & WAYBILLS',
        'mark_func': draw_transporter_mark,
        'pri': (13, 148, 136, 255),    # Teal / Emerald
        'sec': (45, 212, 191, 255),
    },
    {
        'key': 'community',
        'sub': 'COMMUNITY',
        'desc': 'HOSTEL & EVENTS',
        'mark_func': draw_community_mark,
        'pri': (124, 58, 237, 255),   # Violet
        'sec': (167, 139, 250, 255),
    }
]

def generate():
    SCALE = 4
    
    for p in PLATFORMS:
        # 1. Generate Mark (400x400 downsampled from 1600x1600)
        mark_dim = 400
        mark_hi = Image.new('RGBA', (mark_dim * SCALE, mark_dim * SCALE), (0, 0, 0, 0))
        draw_mark = ImageDraw.Draw(mark_hi)
        p['mark_func'](draw_mark, (mark_dim * SCALE) // 2, (mark_dim * SCALE) // 2, int(mark_dim * SCALE * 0.42), p['pri'], p['sec'])
        mark_final = mark_hi.resize((mark_dim, mark_dim), Image.Resampling.LANCZOS)
        
        mark_out_path = os.path.join(OUTPUT_DIR, f"clarity-{p['key']}-mark.png")
        mark_final.save(mark_out_path, 'PNG', optimize=True)
        mark_final.save(os.path.join(STATICFILES_DIR, f"clarity-{p['key']}-mark.png"), 'PNG', optimize=True)
        print(f"Generated pristine mark: {mark_out_path}")
        
        # 2. Generate Full Logo (Horizontal: 680x200 downsampled from 2720x800)
        w_lo, h_lo = 720, 200
        w_hi, h_hi = w_lo * SCALE, h_lo * SCALE
        logo_hi = Image.new('RGBA', (w_hi, h_hi), (0, 0, 0, 0))
        draw_logo = ImageDraw.Draw(logo_hi)
        
        # Draw emblem mark on left
        mark_cx = int(120 * SCALE)
        mark_cy = int((h_lo // 2) * SCALE)
        mark_r = int(68 * SCALE)
        p['mark_func'](draw_logo, mark_cx, mark_cy, mark_r, p['pri'], p['sec'])
        
        # Fonts
        font_main = get_font(int(58 * SCALE), bold=True)
        font_sub = get_font(int(24 * SCALE), bold=True)
        font_desc = get_font(int(15 * SCALE), bold=False)
        
        text_x = int(220 * SCALE)
        clarity_y = int(46 * SCALE)
        
        # Draw "CLARITY" in crisp Pure White (or dark readable)
        draw_logo.text((text_x, clarity_y), "CLARITY", font=font_main, fill=(255, 255, 255, 255))
        
        # Measure CLARITY width
        clarity_bbox = font_main.getbbox("CLARITY")
        clarity_w = clarity_bbox[2] - clarity_bbox[0]
        
        # Draw Subtitle Badge: e.g. "RETAIL LAN"
        sub_y = int(112 * SCALE)
        draw_logo.text((text_x, sub_y), p['sub'], font=font_sub, fill=p['sec'])
        
        # Draw descriptive tag
        desc_y = int(144 * SCALE)
        draw_logo.text((text_x, desc_y), p['desc'], font=font_desc, fill=(148, 163, 184, 220))
        
        logo_final = logo_hi.resize((w_lo, h_lo), Image.Resampling.LANCZOS)
        logo_out_path = os.path.join(OUTPUT_DIR, f"clarity-{p['key']}-logo.png")
        logo_final.save(logo_out_path, 'PNG', optimize=True)
        logo_final.save(os.path.join(STATICFILES_DIR, f"clarity-{p['key']}-logo.png"), 'PNG', optimize=True)
        print(f"Generated pristine logo: {logo_out_path}")

    print("All platform logos successfully recreated from scratch!")

if __name__ == '__main__':
    generate()
