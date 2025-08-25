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
    return {"zone": name, "id": resp["HostedZone"]["Id"]}

def list_zones(session):
    r53 = session.client("route53")
    zones = r53.list_hosted_zones()["HostedZones"]
    return [{"id": z["Id"], "name": z["Name"].rstrip(".")} for z in zones]

def add_record(session, zone_id, name, record_type, value, ttl=60):
    r53 = session.client("route53")
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
