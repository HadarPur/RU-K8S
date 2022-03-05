from typing import Type
from locust.env import Environment
from locust import User


class Attacker(object):
    def __init__(self, user: Type[User], count: int, spawn_rate: int):
        self.environment = Environment(user_classes=[user])
        self.environment.create_local_runner()
        self.count = count
        self.spawn_rate = spawn_rate

    def start(self):
        self.environment.runner.start(self.count, spawn_rate=self.spawn_rate)

    def stop(self):
        self.environment.runner.quit()
        self.environment.runner.greenlet.join()
