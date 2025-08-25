# platform_cli/utils.py
import boto3
from typing import Optional, List, Dict

TAG_KEY = "CreatedBy"
TAG_VALUE = "platform-cli"

def make_session(profile: Optional[str], region: Optional[str]):
    # Creates an explicit boto3 Session (no secrets in code)
    return boto3.Session(profile_name=profile, region_name=region)

def default_tags(owner: str, project: str, env: str):
    return [
        {"Key": TAG_KEY, "Value": TAG_VALUE},
        {"Key": "Owner", "Value": owner},
        {"Key": "Project", "Value": project},
        {"Key": "Environment", "Value": env},
    ]

def is_cli_created(tags: Optional[List[Dict]]) -> bool: 
    if not tags:
        return False
    return any(t.get("Key") == TAG_KEY and t.get("Value") == TAG_VALUE for t in tags)
