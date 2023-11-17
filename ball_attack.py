from abc import ABC, abstractmethod

# Interface(Component)
class Attack(ABC):
    @abstractmethod
    def use(self):
        pass

#Concrete Components
class BallAttack(Attack):
    def use(self) -> str:
        return 'assets/weapons'

#Decorator
class Decorator(Attack):
    def __init__(self, ball: Attack) -> None:
        self._ball = ball

    @property
    def ball(self) -> str:
        return self._ball

#Concrete Decorators
class BlueBallAttack(Decorator):
    def use(self):
        return f"{self.ball.use()}/ballattack_b.png"
    
class OrangeBallAttack(Decorator):
    def use(self):
        return f"{self.ball.use()}/ballattack_o.png"


class YellowBallAttack(Decorator):
    def use(self):
        return f"{self.ball.use()}/ballattack_y.png"

