import pygame as pg
from pygame.display import update 


class Timer_Handler:

    def __init__(self):

        self.timers = []

    def update(self):

        for timer in self.timers:

            timer.update()


class Timer:

    timer_handler = None

    def __init__(self, time, repeat, event):

        self.creation_time = pg.time.get_ticks()

        self.stop = True
        self.wait_time = (time * 1000)
        self.next_time = self.creation_time + self.wait_time
        self.repeat = repeat
        self.event = event

        Timer.timer_handler.timers.append(self)

    def update_timer(self):

        if self.stop == True:
            self.stop = False

        if pg.time.get_ticks() >= self.next_time:

            self.event()

            if self.repeat:

                self.next_time = pg.time.get_ticks() + self.wait_time()
            else:

                Timer.timer_handler.timers.remove(self)
                del self

    def update(self):

        self.update_timer()

        

