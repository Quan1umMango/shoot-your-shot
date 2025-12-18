import pygame
from constants import *
from serde import *

class StaticBlock:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        
    def draw(self,screen):
        pygame.draw.rect(screen,BLOCK_COLOR,self.rect)

    def update(self):
        # do nothing
        pass

    def from_dict(self,dict_):
        self.rect = rect_from_dict(dict_['rect'])
    
    def to_dict(self):
        return {'rect':rect_to_dict(self.rect)}

class MovingBlock:
    def __init__(self,x,y,w,h,speed:float,checkpoints):
        if len(checkpoints) == 0:
            checkpoints = [pygame.Vector2(x,y)]
        self.rect = pygame.Rect(x,y,w,h)
        self.checkpoints = checkpoints 
        self.current_checkpoint = 0
        self.speed = speed

    def draw(self,screen):
        pygame.draw.rect(screen,BLOCK_COLOR,self.rect)

    def update(self):
        if len(self.checkpoints) == 0: return
        to = self.checkpoints[self.current_checkpoint]
        rect_v = pygame.math.Vector2(self.rect.x,self.rect.y)

        if (rect_v - to).magnitude() < 5:
            self.current_checkpoint = (self.current_checkpoint + 1)  % len(self.checkpoints)
        dir_ = (pygame.math.Vector2(self.rect.x,self.rect.y) - self.checkpoints[self.current_checkpoint]).normalize()
        self.rect.x -= dir_.x * self.speed 
        self.rect.y -= dir_.y * self.speed

    def from_dict(self,dict_):
        self.rect = rect_from_dict(dict_.get('rect'))
        self.current_checkpoint = dict_.get('current_checkpoint') or 0
        self.speed = dict_.get('speed') or 0
        self.checkpoints = [vector2_from_dict(d) for d in dict_.get('checkpoints') or [] ]
    
    def to_dict(self):
        d = {}
        d['rect'] = rect_to_dict(self.rect)
        d['checkpoints'] = [vector2_to_dict(v) for v in self.checkpoints]
        d['current_checkpoint'] = self.current_checkpoint
        d['speed'] = self.speed
        return d
    

class Block:
    def __init__(self,screen,inner=None):
        self.screen = screen
        self.inner = inner

    def update(self):
        if hasattr(self.inner,'update') or callable(self.inner,'update'):
            self.inner.update()

    def draw(self):
        self.inner.draw(self.screen)

    def from_dict(self,dict_):
        if dict_.get('inner') is None:return
        inner = dict_.get('inner')
        if inner.get('checkpoints') or inner.get('current_checkpoint') or inner.get('speed'):
            self.inner = MovingBlock(0,0,0,0,0,[])
            self.inner.from_dict(inner)
        else:
            self.inner = StaticBlock(0,0,0,0)
            self.inner.from_dict(inner)

    def to_dict(self):
        d = {'inner':self.inner.to_dict()}
        return d

    def rect(self):
        return self.inner.rect


