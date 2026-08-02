# forwarder/send_to_splunk.py
import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HEC_URL = os.getenv("SPLUNK_HEC_URL")
HEC_TOKEN = os.getenv("HEC_TOKEN")

def send_event(event_data, sourcetype):
    headers = {"Authorization": f"Splunk {HEC_TOKEN}"}
    payload = {
        "event": event_data,
        "sourcetype": sourcetype,
        "time": time.time()
    }
    response = requests.post(HEC_URL, headers=headers, json=payload, timeout=15, verify=False)
    if response.status_code == 200:
        print(f"Sent event: {sourcetype}")
    else:
        print(f"HEC error: {response.status_code} -- {response.text}")

def forward_pipeline_results(path="pipeline_results.json"):
    if not os.path.exists(path):
        print(f"{path} not found -- run Project 06's pipeline at least once first")
        return
    with open(path) as f:
        data = json.load(f)
    send_event(data, sourcetype="vuln_pipeline_run")

if __name__ == "__main__":
    forward_pipeline_results()
