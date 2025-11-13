import os, math
import pygame
from constants import *

# Fonts
def load_game_font(size):
   for fname in CUSTOM_FONT_FILENAMES:
        if os.path.exists(fname):
            try:
                return pygame.font.Font(fname, size)
            except Exception:
                pass
   for fn in ["Verdana","impact","comicsansms"]:
        try:
            return pygame.font.SysFont(fn, size, bold=True)
        except Exception:
            pass
   return pygame.font.SysFont(None, size)

# Load background & icons
def load_image(path):
    if not os.path.exists(path):
        print("PATH ",path,"DOES NOT EXIST")
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(e)
        return None

def load_icon(path, size=ICON_SIZE):
    img = load_image(path)
    if img is None:
        return None
    iw, ih = img.get_size()
    sw, sh = size
    scale = min(sw / iw, sh / ih)
    new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
    try:
        return pygame.transform.smoothscale(img, new_size)
    except Exception:
        return img

BG_IMG = load_image(BACKGROUND_IMAGE)
MUSIC_ICON = load_icon(MUSIC_ICON_PATH, ICON_SIZE)
SFX_ICON = load_icon(SFX_ICON_PATH, ICON_SIZE)

def blit_bg_with_zoom(surface, img, zoom):
    if img is None:
        surface.fill(GREEN_BG); return
    iw, ih = img.get_size()
    sw, sh = surface.get_size()
    base_scale = max(sw / iw, sh / ih)
    scale = base_scale * zoom
    new_size = (int(iw * scale), int(ih * scale))
    scaled = pygame.transform.smoothscale(img, new_size)
    x = (sw - new_size[0]) // 2
    y = (sh - new_size[1]) // 2
    surface.blit(scaled, (x, y))

def draw_geometric_overlay(surface):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    for i in range(-3, 14):
        pts = [(i * 110, 0), ((i + 2) * 110, 0), ((i - 2) * 110, SCREEN_H), ((i - 4) * 110, SCREEN_H)]
        alpha = 12 if (i % 2 == 0) else 20
        pygame.draw.polygon(overlay, (255,255,255,alpha), pts)
    pygame.draw.polygon(overlay, (0,0,0,30), [(0,0),(200,0),(0,120)])
    pygame.draw.polygon(overlay, (255,255,255,20), [(SCREEN_W,SCREEN_H),(SCREEN_W-260,SCREEN_H),(SCREEN_W,SCREEN_H-180)])
    surface.blit(overlay, (0,0))

# Generic button draw that returns actual drawn rect
def draw_button_scaled(surface, base_rect, text, hover_val, scale_override=1.0, border_width=3, border_color=BLACK):
    scale = (1.0 + 0.06 * hover_val) * scale_override
    w, h = int(base_rect.w * scale), int(base_rect.h * scale)
    cx, cy = base_rect.center
    rect = pygame.Rect(0,0,w,h); rect.center = (cx, cy)

    pulse = 0.6 + 0.4 * math.sin(pygame.time.get_ticks() / 220.0) if hover_val > 0.02 else 0.0
    glow_alpha = int(80 * hover_val * (0.6 + 0.4 * pulse))
    if glow_alpha > 0:
        glow_surf = pygame.Surface((rect.w+18, rect.h+18), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (180,255,200,glow_alpha), glow_surf.get_rect(), border_radius=14)
        surface.blit(glow_surf, (rect.x-9, rect.y-9), special_flags=pygame.BLEND_PREMULTIPLIED)

    color = (
        int(BOX[0] + (HOVER[0] - BOX[0]) * hover_val),
        int(BOX[1] + (HOVER[1] - BOX[1]) * hover_val),
        int(BOX[2] + (HOVER[2] - BOX[2]) * hover_val),
    )
    pygame.draw.rect(surface, color, rect, border_radius=12)
    pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=12)

    txt_surf = BUTTON_FONT.render(text, True, ACCENT)
    surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))
    return rect

# Helper for safely retrieving drawn rects and inflating for clicks
def get_inflated_drawn(ui_drawn, key):
    try:
        r = ui_drawn[key].inflate(CLICK_PAD, CLICK_PAD)
        return r
    except Exception:
        return pygame.Rect(BUTTON_X, PLAY_Y, BUTTON_W, BUTTON_H).inflate(CLICK_PAD, CLICK_PAD)


TITLE_FONT = load_game_font(65)
BUTTON_FONT = load_game_font(30)
SETTINGS_FONT = load_game_font(28)
SMALL_FONT = load_game_font(20)
