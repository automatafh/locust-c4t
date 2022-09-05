import requests
import json
import time


def send_tx_x_chain():

    request_meta = {
        "request_type": "xmlrpc",
        "name": "Cchain",
        "start_time": time.time(),
        "response_length": 0,  # calculating this for an xmlrpc.client response would be too hard
        "response": None,
        "context": {},  # see HttpUser if you actually want to implement contexts
        "exception": None,
    }
    start_perf_counter = time.perf_counter()

    url = "http://127.0.0.1:9650/ext/bc/X"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "avm.send",
        "params": {
            "assetID": "2fombhL7aGPwj3KH4bfrmJwW6PVnMobf9Y2fn9GwxiAAJyFDbe",
            "amount": 10,
            "from": [
                "X-local1sfce28z5zgwyheynaghhhpq0mh7r0nep6st5ne"
            ],
            "to": "X-local1sfce28z5zgwyheynaghhhpq0mh7r0nep6st5ne",
            "username": "ivan",
            "password": "[RASENldmk-30404-23]"
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        request_meta['response'] = response
    except Exception as e:
        request_meta["exception"] = e

    request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
    return request_meta
