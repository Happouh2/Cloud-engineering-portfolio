import boto3
from datetime import datetime, timezone

STALE_KEY_DAYS = 90
RISKY_PORT = 22


def check_public_s3_buckets():
    s3 = boto3.client("s3")
    findings = []

    for bucket in s3.list_buckets()["Buckets"]:
        name = bucket["Name"]

        try:
            pab = s3.get_public_access_block(Bucket=name)["PublicAccessBlockConfiguration"]
            blocked = all(pab.values())
        except s3.exceptions.ClientError:
            blocked = False

        if blocked:
            continue

        try:
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl["Grants"]:
                grantee = grant.get("Grantee", {})
                if grantee.get("URI", "").endswith("AllUsers") or grantee.get("URI", "").endswith("AuthenticatedUsers"):
                    findings.append(f"{name}: public via ACL grant ({grant['Permission']})")
        except s3.exceptions.ClientError as e:
            findings.append(f"{name}: could not check ACL ({e})")

        try:
            policy_status = s3.get_bucket_policy_status(Bucket=name)
            if policy_status["PolicyStatus"]["IsPublic"]:
                findings.append(f"{name}: public via bucket policy")
        except s3.exceptions.ClientError:
            pass

    return findings


def check_open_ssh_security_groups():
    ec2 = boto3.client("ec2")
    findings = []

    for sg in ec2.describe_security_groups()["SecurityGroups"]:
        for rule in sg.get("IpPermissions", []):
            from_port = rule.get("FromPort")
            to_port = rule.get("ToPort")
            if from_port is None or to_port is None:
                continue
            if not (from_port <= RISKY_PORT <= to_port):
                continue

            for ip_range in rule.get("IpRanges", []):
                if ip_range.get("CidrIp") == "0.0.0.0/0":
                    findings.append(
                        f"{sg['GroupId']} ({sg['GroupName']}): port {RISKY_PORT} open to 0.0.0.0/0"
                    )

    return findings


def check_stale_iam_keys():
    iam = boto3.client("iam")
    findings = []
    now = datetime.now(timezone.utc)

    for user in iam.list_users()["Users"]:
        username = user["UserName"]
        keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]

        for key in keys:
            age_days = (now - key["CreateDate"]).days
            if age_days > STALE_KEY_DAYS:
                findings.append(
                    f"{username}: access key {key['AccessKeyId']} is {age_days} days old (status: {key['Status']})"
                )

    return findings


def print_section(title, findings):
    print(f"\n=== {title} ===")
    if not findings:
        print("No issues found.")
        return
    for f in findings:
        print(f"  [!] {f}")


def main():
    print_section("Public S3 Buckets", check_public_s3_buckets())
    print_section(f"Security Groups with Port {RISKY_PORT} Open to the World", check_open_ssh_security_groups())
    print_section(f"IAM Access Keys Older Than {STALE_KEY_DAYS} Days", check_stale_iam_keys())


if __name__ == "__main__":
    main()