import pygame


#Wait Class returns true every interval


class TimeWait():
    
    def __init__(self, start, wait):
        self.start = start
        self.wait = wait

    def update(self, clock):
        time_since_enter = pygame.time.get_ticks() - self.start
        if pygame.time.get_ticks() - self.start >= self.wait*1000:
            self.start = pygame.time.get_ticks()
            return True
        return False
    

    
        
        