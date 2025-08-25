import time

OWNER_TAG_KEY = "CreatedBy"
DEFAULT_OWNER = "yoav"

def get_owner_tag_value():
    return DEFAULT_OWNER

def list_instances(session, region, owner_tag=None):
    """List only instances owned by DEFAULT_OWNER (or provided tag)."""
    if owner_tag is None:
        owner_tag = DEFAULT_OWNER

    ec2 = session.client("ec2", region_name=region)
    resp = ec2.describe_instances()
    instances = []

    for res in resp.get("Reservations", []):
        for inst in res.get("Instances", []):
            if inst["State"]["Name"] == "terminated":
                continue

            tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
            if tags.get(OWNER_TAG_KEY) == owner_tag:
                instances.append({
                    "id": inst["InstanceId"],
                    "state": inst["State"]["Name"],
                    "type": inst["InstanceType"]
                })
    return instances

def _get_latest_ami(session, region, os_type="amazon"):
    """Fetch latest AMI via SSM for Amazon Linux 2023 or Ubuntu 22.04."""
    ssm = session.client("ssm", region_name=region)
    params = {
        "amazon": "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64",
        "ubuntu": "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
    }
    key = params.get(os_type, params["amazon"])
    return ssm.get_parameter(Name=key)["Parameter"]["Value"]

def launch_instance(session, region, instance_type="t3.micro", os_type="amazon", owner_tag=None):
    """Launch instance with owner tag and restrictions."""
    if owner_tag is None:
        owner_tag = DEFAULT_OWNER

    if instance_type not in ["t3.micro", "t2.small"]:
        raise ValueError("Instance type must be t3.micro or t2.small")

    # Limit to 2 running instances per owner
    current_instances = list_instances(session, region, owner_tag)
    if len(current_instances) >= 2:
        raise RuntimeError("Maximum 2 instances allowed per owner")

    ec2 = session.client("ec2", region_name=region)
    ami_id = _get_latest_ami(session, region, os_type)

    resp = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{
            "ResourceType": "instance",
            "Tags": [{"Key": OWNER_TAG_KEY, "Value": owner_tag}]
        }]
    )
    return resp["Instances"][0]["InstanceId"]

def stop_instance(session, region, instance_id):
    ec2 = session.client("ec2", region_name=region)
    ec2.stop_instances(InstanceIds=[instance_id])
    return instance_id

def start_instance(session, region, instance_id):
    ec2 = session.client("ec2", region_name=region)
    ec2.start_instances(InstanceIds=[instance_id])
    return instance_id

def terminate_instance(session, region, instance_id):
    ec2 = session.client("ec2", region_name=region)
    ec2.terminate_instances(InstanceIds=[instance_id])
    return instance_id
