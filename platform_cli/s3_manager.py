import time
import os

OWNER_TAG_KEY = "CreatedBy"
DEFAULT_OWNER = "yoav"

def get_owner_tag_value():
    return DEFAULT_OWNER

def create_bucket(session, bucket_name, region, public=False, owner_tag=None):
    if owner_tag is None:
        owner_tag = DEFAULT_OWNER

    s3 = session.client("s3", region_name=region)
    kwargs = {"Bucket": bucket_name}
    if region != "us-east-1":
        kwargs["CreateBucketConfiguration"] = {"LocationConstraint": region}

    s3.create_bucket(**kwargs)

    # Wait until bucket exists
    for _ in range(10):
        try:
            s3.head_bucket(Bucket=bucket_name)
            break
        except Exception:
            time.sleep(2)

    # Set default private + encryption
    if not public:
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            }
        )
    s3.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
        }
    )

    # Add owner tag
    s3.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={"TagSet": [{"Key": OWNER_TAG_KEY, "Value": owner_tag}]}
    )

    return bucket_name

def list_buckets(session, owner_tag=None):
    if owner_tag is None:
        owner_tag = DEFAULT_OWNER

    s3 = session.client("s3")
    resp = s3.list_buckets()
    result = []

    for b in resp.get("Buckets", []):
        try:
            tags_resp = s3.get_bucket_tagging(Bucket=b["Name"])
            tags = {t["Key"]: t["Value"] for t in tags_resp.get("TagSet", [])}
        except s3.exceptions.ClientError:
            tags = {}
        if tags.get(OWNER_TAG_KEY) == owner_tag:
            result.append(b["Name"])
    return result

def upload_file(session, bucket_name, file_path, key=None):
    if key is None:
        key = os.path.basename(file_path)
    s3 = session.client("s3")
    s3.upload_file(file_path, bucket_name, key)
    return key

def delete_file(session, bucket_name, key):
    s3 = session.client("s3")
    s3.delete_object(Bucket=bucket_name, Key=key)
    return key

def delete_bucket(session, bucket_name):
    s3 = session.client("s3")
    # delete all objects first
    objs = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    for o in objs:
        s3.delete_object(Bucket=bucket_name, Key=o["Key"])
    s3.delete_bucket(Bucket=bucket_name)
    return bucket_name
