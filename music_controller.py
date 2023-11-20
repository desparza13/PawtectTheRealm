from abc import ABC, abstractmethod
import pygame
from config.constants import MUSIC_PATH, BOSS_MUSIC

# Publisher
class GameEventPublisher:
    """
    Publisher class to manage subscriptions and notifications for game events.

    Attributes:
        _in_boss_fight (bool): Indicates whether a boss fight is active.
        _observers (list): List of subscribed observers.
    """
    def __init__(self) -> None:
        """
        Initializes a new GameEventPublisher.
        """
        self._in_boss_fight = False  # Indicates whether a boss fight is active.
        self._observers = []  # List of subscribed observers.

    def subscribe(self, observer) -> None:
        """
        Subscribe an observer to receive notifications.
        """
        self._observers.append(observer)

    def unsubscribe(self, observer) -> None:
        """
        Unsubscribe an observer from receiving notifications.
        """
        self._observers.remove(observer)

    def notify(self) -> None:
        """
        Notify all subscribed observers about an event change.
        """
        for observer in self._observers:
            observer.update(self)

    def start_boss_fight(self) -> None:
        """
        Trigger the start of a boss fight and notify observers.
        """
        self._in_boss_fight = True
        self.notify()

    def end_boss_fight(self) -> None:
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
    def update(self, publisher: GameEventPublisher) -> None:
        """
        Update the observer with the current state of the game event.
        """
        pass

# Concrete Observer
class MusicController(MusicObserver):
    """
    Concrete implementation of MusicObserver that controls music playback.

    Attributes:
        current_track (str): The status/indicator of the current track being played.
    """
    
    def __init__(self):
        self.current_track = None # The current track being played.

    def update(self, publisher: GameEventPublisher) -> None:
        """
        Update the music playback based on the game event.
        """
        # If a boss fight has started and the boss track is not already playing, load and play it.
        if publisher._in_boss_fight and self.current_track != 'boss':
            pygame.mixer.music.load(BOSS_MUSIC)
            pygame.mixer.music.play(-1) # -1 for looped playback
            self.current_track = 'boss'
        # If the boss fight is over and the original track is not playing, load and play it.
        elif not publisher._in_boss_fight and self.current_track != 'original':
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.play(-1) # -1 for looped playback
            self.current_track = 'original'
