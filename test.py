import time
from locust import HttpUser, task, between


class InitialTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def cat_facts(self):
        self.client.get(url="/facts")

    @task
    def cat_breeds(self):
        self.client.get(url="/breeds")
