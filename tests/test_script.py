import boto3, time, os
from platform_cli import ec2_manager, s3_manager, route53_manager

REGION = "us-east-1"

def main():
    session = boto3.Session(profile_name="default")

    # === EC2 TEST ===
    print("=== EC2 TEST ===")
    ec2 = session.client("ec2", region_name=REGION)

    current = ec2_manager.list_instances(session, REGION)
    print("Current:", current)

    # Launch
    iid = ec2_manager.launch_instance(session, REGION)
    print("Launched:", iid)

    # Wait until running
    print("Waiting for instance to enter running state...")
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[iid])

    # Stop
    ec2_manager.stop_instance(session, REGION, iid)
    print("Stopped:", iid)

    # Wait until stopped
    waiter = ec2.get_waiter("instance_stopped")
    waiter.wait(InstanceIds=[iid])

    # Start
    ec2_manager.start_instance(session, REGION, iid)
    print("Started:", iid)

    # Wait until running again
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[iid])

    # Terminate
    ec2_manager.terminate_instance(session, REGION, iid)
    print("Terminated:", iid)

    # === S3 TEST ===
    print("\n=== S3 TEST ===")
    bucket_name = f"test-bucket-{int(time.time())}"
    s3_manager.create_bucket(session, bucket_name, REGION, public=False)
    print("Created:", bucket_name)

    # Wait until bucket exists
    s3 = session.client("s3", region_name=REGION)
    print("Waiting for bucket to exist...")
    for _ in range(10):
        try:
            s3.head_bucket(Bucket=bucket_name)
            break
        except Exception:
            time.sleep(2)
    else:
        raise RuntimeError("Bucket not ready in time")

    # Upload file
    file_path = "test_file.txt"
    with open(file_path, "w") as f:
        f.write("hello world")
    s3_manager.upload_file(session, bucket_name, file_path, "test_file.txt")
    print("Uploaded file")

    # List buckets
    my_buckets = s3_manager.list_buckets(session)
    print("My buckets:", my_buckets)

    # Delete file
    s3_manager.delete_file(session, bucket_name, "test_file.txt")
    print("Deleted test file")

    # Delete bucket
    s3_manager.delete_bucket(session, bucket_name)
    print("Deleted:", bucket_name)

    os.remove(file_path)

    # === ROUTE53 TEST ===
    print("\n=== ROUTE53 TEST ===")
    zone_name = f"test{int(time.time())}.com"

    # Create hosted zone
    zone = route53_manager.create_zone(session, zone_name)
    print("Created zone:", zone)

    # List zones
    zones = route53_manager.list_zones(session)
    print("Zones:", zones)

    # Add record
    route53_manager.add_record(session, zone["id"], f"www.{zone_name}", "A", "1.2.3.4")
    print("Added record")

    # List records
    records = route53_manager.list_records(session, zone["id"])
    print("Records:", records)

    # Cleanup: delete hosted zone
    route53_manager.delete_zone(session, zone["id"])
    print("Deleted zone:", zone_name)


if __name__ == "__main__":
    main()
