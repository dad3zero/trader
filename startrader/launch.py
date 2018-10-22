#!/usr/bin/env python 

import pygame


class App:
    def __init__(self):
        self._running = True
        self._screen = None
        self.size = self.weigth, self.height = 640, 480

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        background = pygame.Surface(self._screen.get_size())
        background.fill((255, 255, 255))
        self._screen.blit(background, (0, 0))
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False

    def on_cleanup(self):
        pygame.quit()

    def onloop(self):
        pass

    def on_render(self):
        pass

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.onloop()
            self.on_render()

        self.on_cleanup()


app = App()
app.on_execute()

#pygame.display.set_caption("Hello World")
#pygame.display.flip()


