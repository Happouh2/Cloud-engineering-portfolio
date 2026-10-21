# forwarder/send_github_actions.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEC_URL = os.getenv("SPLUNK_HEC_URL")
HEC_TOKEN = os.getenv("HEC_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def fetch_recent_runs(per_page=20):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers, params={"per_page": per_page}, timeout=15)
    response.raise_for_status()
    return response.json().get("workflow_runs", [])

def forward_github_actions():
    runs = fetch_recent_runs()
    if not runs:
        print("No workflow runs found")
        return

    hec_headers = {"Authorization": f"Splunk {HEC_TOKEN}"}
    for run in runs:
        event = {
            "workflow_name": run["name"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "run_number": run["run_number"],
            "created_at": run["created_at"],
            "html_url": run["html_url"]
        }
        payload = {"event": event, "sourcetype": "github_actions_run"}
        requests.post(HEC_URL, headers=hec_headers, json=payload, timeout=15, verify=False)

    print(f"Forwarded {len(runs)} GitHub Actions run(s)")

if __name__ == "__main__":
    forward_github_actions()
