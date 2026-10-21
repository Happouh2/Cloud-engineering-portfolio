# 08 -- Splunk Security Posture Dashboard

## What this does
Runs Splunk Enterprise locally via Docker and pulls real data from
three separate projects into one dashboard:
- Project 06's vulnerability pipeline runs (HTTP Event Collector)
- Project 07's self-healing Lambda invocations (CloudWatch Logs API)
- Project 05's CI/CD pass/fail history (GitHub REST API)

Plus a saved alert that fires the moment a pipeline run finds
anything.

## Stack
Splunk Enterprise (Docker), HTTP Event Collector, boto3,
GitHub REST API, SPL, Dashboard Studio, Python (requests)

## Files
- docker-compose.yml -- the whole Splunk environment, reproducible
- forwarder/send_to_splunk.py -- Project 06's pipeline results
- forwarder/send_cloudwatch_logs.py -- Project 07's Lambda logs
- forwarder/send_github_actions.py -- Project 05's workflow runs
- dashboards/security_posture_overview.json -- exported dashboard

## Real issues hit building this (and how they were fixed)
- **Docker Compose plugin missing**: `docker.io` alone doesn't include
  it on Ubuntu -- installed `docker-compose-v2` separately.
- **Splunk's newer license requirement**: the image now needs
  `SPLUNK_GENERAL_TERMS` alongside `SPLUNK_START_ARGS`, undocumented
  in the original setup.
- **HEC requires HTTPS despite the name**: plain `http://` to port
  8088 gets silently dropped -- switched to `https://` with
  `verify=False` against Splunk's self-signed local cert.
- **FilterLogEvents pagination**: CloudWatch's API can return an
  empty first page with a `nextToken` even when matching events
  exist -- the AWS CLI follows this automatically, raw boto3 calls
  don't. Fixed by looping until `nextToken` is exhausted.
- **Saved reports carry their own baked-in time range**: a
  dashboard panel referencing a report via `savedsearch` can silently
  inherit a stale time window from when the report was first created
  -- fixed by using an explicit `earliest=0 latest=now` in the panel's
  own query instead of trusting the saved report's default.
- **A genuinely real finding**: correlating GitHub Actions history
  surfaced that Project 06's scheduled pipeline had been failing
  for a week, caused by two repository secrets (`MOCK_MODE`,
  `NESSUS_URL`) that were never actually added on GitHub -- exactly
  the kind of thing this dashboard exists to catch.

## Reproduce it
cp .env.example .env   # fill in real values, never commit this file
docker compose up -d
# create a HEC token in the UI, add it to .env
python3 forwarder/send_to_splunk.py
python3 forwarder/send_cloudwatch_logs.py
python3 forwarder/send_github_actions.py

## A deliberate limitation
All three forwarders run locally, not from GitHub Actions --
Splunk here only listens on localhost, so a cloud-hosted runner
has no path to it. Scheduling, if wanted, is local cron, not a
GitHub Actions workflow.
