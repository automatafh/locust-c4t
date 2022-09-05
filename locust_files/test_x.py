import requests
import json
from locust import HttpUser, task
import sendxchaintx


class XChainLocustTest(HttpUser):

    @task
    def send_x_chain_tx(self):
        result = sendxchaintx.send_tx_x_chain()
        return result
