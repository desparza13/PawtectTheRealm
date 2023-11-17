from abc import ABC, abstractmethod

# Interface(Component)
class Atack(ABC):
    @abstractmethod
    def use(self):
        pass

#Concrete Components
class BallAtack(Atack):
    def use(self) -> str:
        return 'assets/weapons'

#Decorator
class Decorator(Atack):
    def __init__(self, ball: Atack) -> None:
        self._ball = ball

    @property
    def ball(self) -> str:
        return self._ball

#Concrete Decorators
class BlueBallAtack(Decorator):
    def use(self):
        return f"{self.ball.use()}/ballattack_b.png"
    
class OrangeBallAtack(Decorator):
    def use(self):
        return f"{self.ball.use()}/ballattack_o.png"


class YellowBallAtack(Decorator):
    def use(self):
        return f"{self.ball.use()}/ballattack_y.png"

