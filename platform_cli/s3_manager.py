import time

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

    # wait until bucket exists
    for _ in range(10):
        try:
            s3.head_bucket(Bucket=bucket_name)
            break
        except Exception:
            time.sleep(2)

    # set default private + encryption
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

    # add owner tag
    s3.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={"TagSet": [{"Key": OWNER_TAG_KEY, "Value": owner_tag}]}
    )
    return bucket_name

def list_buckets(session, owner_tag=None):
    if owner_tag is None:
        owner_tag = DEFAULT_OWNER

    s3 = session.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])
    my_buckets = []
    for b in buckets:
        try:
            tags = s3.get_bucket_tagging(Bucket=b["Name"]).get("TagSet", [])
            tags_dict = {t["Key"]: t["Value"] for t in tags}
            if tags_dict.get(OWNER_TAG_KEY) == owner_tag:
                my_buckets.append(b["Name"])
        except Exception:
            continue
    return my_buckets

def upload_file(session, bucket_name, file_path, key):
    s3 = session.client("s3")
    s3.upload_file(file_path, bucket_name, key)

def delete_file(session, bucket_name, key):
    s3 = session.client("s3")
    s3.delete_object(Bucket=bucket_name, Key=key)

def delete_bucket(session, bucket_name):
    s3 = session.resource("s3")
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
