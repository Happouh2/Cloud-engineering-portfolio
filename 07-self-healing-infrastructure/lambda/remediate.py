# lambda/remediate.py
import json
import os
import base64
import urllib.request
import boto3

autoscaling = boto3.client('autoscaling')

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    alarm_name = message.get('AlarmName', 'unknown-alarm')
    dimensions = message.get('Trigger', {}).get('Dimensions', [])

    asg_name = None
    for d in dimensions:
        if d.get('name') == 'AutoScalingGroupName':
            asg_name = d.get('value')

    if not asg_name:
        print("No ASG name found in alarm payload -- nothing to remediate")
        return {"status": "no_action"}

    current = autoscaling.describe_auto_scaling_groups(
        AutoScalingGroupNames=[asg_name]
    )['AutoScalingGroups'][0]
    new_capacity = min(current['DesiredCapacity'] + 1, current['MaxSize'])

    autoscaling.set_desired_capacity(
        AutoScalingGroupName=asg_name,
        DesiredCapacity=new_capacity,
        HonorCooldown=False
    )
    print(f"Scaled {asg_name} to desired capacity {new_capacity}")

    create_servicenow_incident(alarm_name, asg_name, new_capacity)
    return {"status": "remediated", "asg": asg_name, "new_capacity": new_capacity}


def create_servicenow_incident(alarm_name, asg_name, new_capacity):
    instance = os.environ['SNOW_INSTANCE']
    username = os.environ['SNOW_USERNAME']
    password = os.environ['SNOW_PASSWORD']

    payload = json.dumps({
        "short_description": f"[AUTO-HEAL] {alarm_name} on {asg_name}",
        "description": (
            f"CloudWatch alarm '{alarm_name}' fired on Auto Scaling "
            f"Group '{asg_name}'. Lambda automatically scaled desired "
            f"capacity to {new_capacity}. No human was paged."
        ),
        "urgency": "3",
        "impact": "3",
        "category": "infrastructure"
    }).encode()

    creds = base64.b64encode(f"{username}:{password}".encode()).decode()
    req = urllib.request.Request(
        f"{instance}/api/now/table/incident",
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {creds}"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        print(f"ServiceNow response: {resp.status}")
        