from abc import ABC, abstractmethod
import config.constants as const

class Attack(ABC):
    """
    The Attack abstract class declares the interface (Component) common to all
    supported attack versions. This class is meant to define the use method that
    needs to be implemented by any concrete attack variant.
    """
    
    @abstractmethod
    def use(self) -> str:
        """
        Abstract method that should be overridden to return the path where
        the weapon's assets are located.
        """
        pass

class Ball(Attack):
    """
    Concrete Components are actual implementations of the Attack interface. The
    Ball class represents a basic form of attack.
    """
    
    def use(self) -> str:
        """
        Implements the use method to return the directory where basic ball
        assets are stored.
        """
        return const.WEAPONS_PATH

class Decorator(Attack):
    """
    The Decorator class follows the same interface as the other attacks. The
    purpose of this class is to define a wrapping interface for all concrete
    decorator classes, providing them with the ability to store a reference to
    an object of a Ball class.
    """
    
    def __init__(self, ball: Attack) -> None:
        """
        Initializes a Decorator object with a specific Attack instance.
        """
        self._ball = ball

    @property
    def ball(self) -> Attack:
        """
        Property that exposes the ball instance.
        """
        return self._ball

class BlueBall(Decorator):
    """
    BlueBall is a concrete decorator that adds responsibilities to the ball
    object, such as utilizing a specific 'blue' ball asset.
    """
    
    def use(self) -> str:
        """
        Adds a blue ball asset to the path provided by the wrapped ball object.
        """
        return f"{self.ball.use()}{const.BALLATTACK_B}"
    
class OrangeBall(Decorator):
    """
    OrangeBall is a concrete decorator that adds responsibilities to the ball
    object, such as utilizing a specific 'orange' ball asset.
    """
    
    def use(self) -> str:
        """
        Adds an orange ball asset to the path provided by the wrapped ball object.
        """
        return f"{self.ball.use()}{const.BALLATTACK_O}"

class YellowBall(Decorator):
    """
    YellowBall is a concrete decorator that adds responsibilities to the ball
    object, such as utilizing a specific 'yellow' ball asset.
    """
    
    def use(self) -> str:
        """
        Adds a yellow ball asset to the path provided by the wrapped ball object.
        """
        return f"{self.ball.use()}{const.BALLATTACK_Y}"
