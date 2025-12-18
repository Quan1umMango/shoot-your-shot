import pygame
def rect_from_dict(dict_) -> pygame.Rect:
    rect = pygame.Rect(0,0,0,0)
    if dict_ is None: return rect
    rect.x = dict_.get('x') or 0
    rect.y = dict_.get('y') or 0
    rect.w = dict_.get('w') or 0
    rect.h = dict_.get('h') or 0
    return rect

def rect_to_dict(rect):
    d = {}
    d['x'] = rect.x
    d['y'] = rect.y
    d['w'] = rect.w
    d['h'] = rect.h
    return d

def vector2_from_dict(dict_) -> pygame.math.Vector2:
    v = pygame.math.Vector2(0,0)
    if dict_ is None: return v
    v.x = dict_.get('x') or 0
    v.y = dict_.get('y') or 0
    return v

def vector2_to_dict(v):
    d = {}
    d['x'] = v.x
    d['y'] = v.y
    return d

