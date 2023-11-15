# music_controller.py

from abc import ABC, abstractmethod

import pygame

# Publisher
class GameEventPublisher:
    _in_boss_fight = False
    _observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def start_boss_fight(self):
        self._in_boss_fight = True
        self.notify()

    def end_boss_fight(self):
        self._in_boss_fight = False
        self.notify()

# Observer interface
class MusicObserver(ABC):
    @abstractmethod
    def update(self, publisher: GameEventPublisher):
        pass

# Concrete Observer
class MusicController(MusicObserver):
    def __init__(self):
        self.current_track = None

    def update(self, publisher: GameEventPublisher):
        #Check if you are in a fight
        if publisher._in_boss_fight and self.current_track != 'boss':
            pygame.mixer.music.load('assets/audio/boss_music.mp3')
            pygame.mixer.music.play(-1)
            self.current_track = 'boss'
        #Check if normal musica
        elif not publisher._in_boss_fight and self.current_track != 'original':
            pygame.mixer.music.load('assets/audio/music.wav')
            pygame.mixer.music.play(-1)
            self.current_track = 'original'




