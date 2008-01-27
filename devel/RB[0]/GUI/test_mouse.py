import time

import pygame
from pygame.locals import *

class GUIMouse(object):
    def __init__(self):
        self.old_pos = pygame.mouse.get_pos()
        self.cur_pos = pygame.mouse.get_pos()

        self.movement = (0, 0)

        self.left_button_hold = False
        self.left_button_down = False
        self.left_button_click = False
        self.left_button_double_click = False
        self.left_button_last_click = 0
        self.max_double_click_time = 0.25

        self.right_button_hold = False
        self.right_button_down = False
        self.right_button_click = False

        self.middle_button_hold = False
        self.middle_button_down = False
        self.middle_button_click = False

        self.scroll = 0

    def update(self, events):
        if self.left_button_down or self.right_button_down or self.middle_button_down:
            self.scroll = 0
            print "Scroll, 0"

        if self.left_button_down:
            self.left_button_hold = True
            print "Left button hold"

        if self.right_button_down:
            self.right_button_hold = True
            print "Right button hold"

        if self.middle_button_down:
            self.middle_button_hold = True
            print "Middle button hold"

        self.left_button_click = False
        self.left_double_click = False
        self.right_button_click = False
        self.middle_button_click = False

        self.old_pos = self.cur_pos
        self.cur_pos = pygame.mouse.get_pos()
        self.movement = (self.cur_pos[0] - self.old_pos[0],
                         self.cur_pos[1] - self.old_pos[1])
        if self.movement[0] or self.movement[1]:
            print "pos/old/change:", self.cur_pos, self.old_pos, self.movement

        for event in events:
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    print "Left button click"
                    self.left_button_down = False
                    self.left_button_hold = False
                    self.left_button_click = True
                    if time.time() - self.left_button_last_click < self.max_double_click_time:
                        self.left_double_click = True
                        self.left_button_last_click = 0
                        print "Left button double click"
                    else:
                        self.left_button_last_click = time.time()

                if event.button == 2:
                    self.middle_button_down = False
                    self.middle_button_hold = False
                    self.middle_button_click = True
                    print "Middle button click"

                if event.button == 3:
                    self.right_button_down = False
                    self.right_button_hold = False
                    self.right_button_click = True
                    print "Right button click"

                if event.button == 4:
                    if not self.left_button_down or self.right_button_down or self.middle_button_down:
                        self.scroll += 1
                    print "SCROLL,", self.scroll

                if event.button == 5:
                    if not self.left_button_down or self.right_button_down or self.middle_button_down:
                        self.scroll -= 1
                    print "SCROLL,", self.scroll

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_button_down = True
                    print "Left button down"

                if event.button == 2:
                    self.middle_button_down = True
                    print "Middle button down"

                if event.button == 3:
                    self.right_button_down = True
                    print "Right button down"

pygame.init()
pygame.display.set_mode((300,200))
pygame.display.set_caption('Mouse Input Demonstration')
running = True

mm = GUIMouse()
while running:
    events = pygame.event.get()
    mm.update(events)
    for event in events:
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

pygame.display.quit()
