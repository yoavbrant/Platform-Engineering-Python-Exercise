import boto3

OWNER_TAG_KEY = "CreatedBy"
DEFAULT_OWNER = "yoav"

def get_owner_tag_value():
    return DEFAULT_OWNER

def create_hosted_zone(session, name, caller_ref, owner_tag=None):
    if owner_tag is None:
        owner_tag = DEFAULT_OWNER

    r53 = session.client("route53")
    resp = r53.create_hosted_zone(
        Name=name,
        CallerReference=caller_ref,
        HostedZoneConfig={
            "Comment": f"Managed by platform-cli, owner={owner_tag}",
            "PrivateZone": False
        }
    )

    zone_id = resp["HostedZone"]["Id"].split("/")[-1]

    # Tag the hosted zone
    r53.change_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=zone_id,
        AddTags=[{"Key": OWNER_TAG_KEY, "Value": owner_tag}]
    )

    return {"zone": name, "id": resp["HostedZone"]["Id"], "owner": owner_tag}


def list_zones(session, owner_tag=None):
    r53 = session.client("route53")
    zones = r53.list_hosted_zones()["HostedZones"]
    result = []

    for z in zones:
        zone_id = z["Id"].split("/")[-1]
        tags_resp = r53.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone_id)
        tags = {t["Key"]: t["Value"] for t in tags_resp.get("ResourceTagSet", {}).get("Tags", [])}
        owner = tags.get(OWNER_TAG_KEY, "")

        if owner_tag is None or owner == owner_tag:
            result.append({"id": z["Id"], "name": z["Name"].rstrip("."), "owner": owner})

    return result


def add_record(session, zone_id, name, record_type, value, ttl=60):
    r53 = session.client("route53")

    # Safety check: make sure the record belongs to the hosted zone
    zone_info = r53.get_hosted_zone(Id=zone_id)
    zone_name = zone_info["HostedZone"]["Name"].rstrip(".")
    if not name.endswith(zone_name):
        raise ValueError(f"Cannot add record '{name}' outside zone '{zone_name}'")

    # Add or update the record
    r53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Changes": [{
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": name,
                    "Type": record_type,
                    "TTL": ttl,
                    "ResourceRecords": [{"Value": value}]
                }
            }]
        }
    )
    return True


def list_records(session, zone_id, zone_name):
    r53 = session.client("route53")
    resp = r53.list_resource_record_sets(HostedZoneId=zone_id)
    return {"zone": zone_name, "records": resp["ResourceRecordSets"]}
