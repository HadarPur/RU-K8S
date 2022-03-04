from locust.log import setup_logging
from locust.env import Environment
from locust.runners import STATE_SPAWNING, STATE_RUNNING, STATE_CLEANUP
from locust import HttpUser, between, task, User

class RegularFlow(object):
    def __init__(self, user: Type[User], count: int, spawn_rate: int) -> None:
        # setup Environment and Runner
        self.env = Environment(user_classes=[user])
        self.env.create_local_runner()
        self.count = count
        self.spawn_rate = spawn_rate

    def start(self):
        # start the test
        self.env.runner.start(self.count, spawn_rate=self.spawn_rate)

    def stop(self):
        self.env.runner.quit()
        self.env.runner.greenlet.join()
