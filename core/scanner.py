import requests
import socket
from time import sleep
from core.config_loader import load_config

def safe_request(method, url):
    config = load_config()
    timeout = config.get("timeout", 5)

    for _ in range(2):
        try:
            return requests.request(method, url, timeout=timeout, verify=True)
        except requests.RequestException:
            sleep(1)

    print(f"[!] Request failed: {url}")
    return None


def check_port(host, port):
    config = load_config()
    timeout = config.get("timeout", 3)

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

