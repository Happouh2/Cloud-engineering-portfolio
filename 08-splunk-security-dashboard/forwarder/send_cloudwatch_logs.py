# forwarder/send_cloudwatch_logs.py
import os
import time
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

HEC_URL = os.getenv("SPLUNK_HEC_URL")
HEC_TOKEN = os.getenv("HEC_TOKEN")
LOG_GROUP = "/aws/lambda/self-healing-remediate"
STATE_FILE = "last_cloudwatch_forward.txt"

logs_client = boto3.client("logs", region_name="us-east-1")

def get_last_forwarded_time():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return int(f.read().strip())
    return int((time.time() - 2592000) * 1000)  # default: last 30 days

def save_last_forwarded_time(ts):
    with open(STATE_FILE, "w") as f:
        f.write(str(ts))

def forward_cloudwatch_logs():
    start_time = get_last_forwarded_time()
    events = []
    next_token = None
    while True:
        kwargs = {"logGroupName": LOG_GROUP, "startTime": start_time}
        if next_token:
            kwargs["nextToken"] = next_token
        response = logs_client.filter_log_events(**kwargs)
        events.extend(response.get("events", []))
        next_token = response.get("nextToken")
        if not next_token:
            break

    if not events:
        print("No new CloudWatch log events since last run")
        return

    headers = {"Authorization": f"Splunk {HEC_TOKEN}"}
    latest_ts = start_time
    for event in events:
        payload = {
            "event": event["message"],
            "sourcetype": "self_healing_lambda",
            "time": event["timestamp"] / 1000
        }
        requests.post(HEC_URL, headers=headers, json=payload, timeout=15, verify=False)
        latest_ts = max(latest_ts, event["timestamp"] + 1)

    save_last_forwarded_time(latest_ts)
    print(f"Forwarded {len(events)} CloudWatch log event(s)")

if __name__ == "__main__":
    forward_cloudwatch_logs()
