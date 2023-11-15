# music_controller.py

from abc import ABC, abstractmethod

import pygame

# Publisher
class GameEventPublisher:
    """
    Publisher class to manage subscriptions and notifications for game events.
    """
    def __init__(self):
        self._in_boss_fight = False  # Indicates whether a boss fight is active.
        self._observers = []  # List of subscribed observers.

    def subscribe(self, observer):
        """
        Subscribe an observer to receive notifications.
        """
        self._observers.append(observer)

    def unsubscribe(self, observer):
        """
        Unsubscribe an observer from receiving notifications.
        """
        self._observers.remove(observer)

    def notify(self):
        """
        Notify all subscribed observers about an event change.
        """
        for observer in self._observers:
            observer.update(self)

    def start_boss_fight(self):
        """
        Trigger the start of a boss fight and notify observers.
        """
        self._in_boss_fight = True
        self.notify()

    def end_boss_fight(self):
        """
        Trigger the end of a boss fight and notify observers.
        """
        self._in_boss_fight = False
        self.notify()

# Observer interface
class MusicObserver(ABC):
    """
    Abstract class for observers that respond to music-related game events.
    """
    @abstractmethod
    def update(self, publisher: GameEventPublisher):
        """
        Update the observer with the current state of the game event.
        """
        pass

# Concrete Observer
class MusicController(MusicObserver):
    """
    Concrete implementation of MusicObserver that controls music playback.
    """
    
    def __init__(self):
        self.current_track = None # The current track being played.

    def update(self, publisher: GameEventPublisher):
        """
        Update the music playback based on the game event.
        """
        # If a boss fight has started and the boss track is not already playing, load and play it.
        if publisher._in_boss_fight and self.current_track != 'boss':
            pygame.mixer.music.load('assets/audio/boss_music.mp3')
            pygame.mixer.music.play(-1) # -1 for looped playback
            self.current_track = 'boss'
        # If the boss fight is over and the original track is not playing, load and play it.
        elif not publisher._in_boss_fight and self.current_track != 'original':
            pygame.mixer.music.load('assets/audio/music.wav')
            pygame.mixer.music.play(-1) # -1 for looped playback
            self.current_track = 'original'




