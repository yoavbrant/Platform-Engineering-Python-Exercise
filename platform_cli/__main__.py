import argparse
import boto3
import uuid
import os
from platform_cli import ec2_manager, s3_manager, route53_manager

# Default owner for tagging
OWNER_TAG = ec2_manager.DEFAULT_OWNER

def main():
    parser = argparse.ArgumentParser(description="Platform CLI tool")
    parser.add_argument("--profile", help="AWS profile", required=True)
    parser.add_argument("--region", help="AWS region", default="us-east-1")

    subparsers = parser.add_subparsers(dest="command")

    # EC2
    ec2p = subparsers.add_parser("ec2", help="Manage EC2")
    ec2p.add_argument("action", choices=["list", "launch", "stop", "start", "terminate"])
    ec2p.add_argument("--id", help="Instance ID")
    ec2p.add_argument("--type", help="Instance type", default="t3.micro")
    ec2p.add_argument("--os", help="OS type", choices=["amazon", "ubuntu"], default="amazon")

    # S3
    s3p = subparsers.add_parser("s3", help="Manage S3")
    s3p.add_argument("action", choices=["list", "create", "upload", "delete-file", "delete-bucket"])
    s3p.add_argument("--name", help="Bucket name")
    s3p.add_argument("--file", help="Local file path")
    s3p.add_argument("--key", help="S3 key")
    s3p.add_argument("--public", action="store_true", help="Make bucket public")

    # Route53
    r53p = subparsers.add_parser("route53", help="Manage Route53")
    r53p.add_argument("action", choices=["list", "create", "add-record", "records"])
    r53p.add_argument("--zone", help="Zone name")
    r53p.add_argument("--zone-id", help="Zone ID")
    r53p.add_argument("--ref", help="Caller reference")
    r53p.add_argument("--record", help="Record name")
    r53p.add_argument("--rtype", help="Record type")
    r53p.add_argument("--value", help="Record value")

    args = parser.parse_args()
    session = boto3.Session(profile_name=args.profile)

    if args.command == "ec2":
        if args.action == "list":
            print(ec2_manager.list_instances(session, args.region, owner_tag=OWNER_TAG))
        elif args.action == "launch":
            iid = ec2_manager.launch_instance(session, args.region, args.type, args.os, owner_tag=OWNER_TAG)
            print("Launched:", iid)
        elif args.action == "stop":
            print("Stopped:", ec2_manager.stop_instance(session, args.region, args.id))
        elif args.action == "start":
            print("Started:", ec2_manager.start_instance(session, args.region, args.id))
        elif args.action == "terminate":
            print("Terminated:", ec2_manager.terminate_instance(session, args.region, args.id))

    elif args.command == "s3":
        if args.action == "list":
            print("My buckets:", s3_manager.list_buckets(session, owner_tag=OWNER_TAG))
        elif args.action == "create":
            if args.public:
                ans = input("⚠️ Create PUBLIC bucket? (yes/no): ")
                if ans.lower() != "yes":
                    print("Cancelled.")
                    return
            bname = s3_manager.create_bucket(session, args.name, args.region, public=args.public, owner_tag=OWNER_TAG)
            print("Created bucket:", bname)
        elif args.action == "upload":
            key = args.key if args.key else os.path.basename(args.file)
            s3_manager.upload_file(session, args.name, args.file, key)
            print(f"Uploaded file '{args.file}' as key '{key}'")
        elif args.action == "delete-file":
            key = args.key if args.key else os.path.basename(args.file)
            s3_manager.delete_file(session, args.name, key)
            print(f"Deleted file with key '{key}'")
        elif args.action == "delete-bucket":
            s3_manager.delete_bucket(session, args.name)
            print("Deleted bucket")

    elif args.command == "route53":
        if args.action == "list":
            zones = route53_manager.list_zones(session, owner_tag=OWNER_TAG)
            print(zones)
        elif args.action == "create":
            if not args.zone:
                print("Error: --zone is required to create a hosted zone")
                return
            caller_ref = args.ref if args.ref else args.zone
            zone = route53_manager.create_hosted_zone(session, name=args.zone, caller_ref=caller_ref, owner_tag=OWNER_TAG)
            print(f"Created zone: {zone}")
        elif args.action == "add-record":
            if not (args.zone_id and args.record and args.rtype and args.value):
                print("Error: --zone-id, --record, --rtype, and --value are required to add a record")
                return
            route53_manager.add_record(session, args.zone_id, args.record, args.rtype, args.value)
            print(f"Added record '{args.record}' of type '{args.rtype}' with value '{args.value}'")
        elif args.action == "records":
            if not args.zone_id:
                print("Error: --zone-id is required to list records")
                return
            recs = route53_manager.list_records(session, args.zone_id, args.zone if args.zone else "")
            print("Records:", recs)

if __name__ == "__main__":
    main()
