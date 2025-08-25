import argparse
import boto3
from platform_cli import ec2_manager, s3_manager, route53_manager

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
            print(ec2_manager.list_instances(session, args.region))
        elif args.action == "launch":
            iid = ec2_manager.launch_instance(session, args.region, args.type, args.os)
            print("Launched:", iid)
        elif args.action == "stop":
            print("Stopped:", ec2_manager.stop_instance(session, args.region, args.id))
        elif args.action == "start":
            print("Started:", ec2_manager.start_instance(session, args.region, args.id))
        elif args.action == "terminate":
            print("Terminated:", ec2_manager.terminate_instance(session, args.region, args.id))

    elif args.command == "s3":
        if args.action == "list":
            print("My buckets:", s3_manager.list_buckets(session))
        elif args.action == "create":
            if args.public:
                ans = input("⚠️ Create PUBLIC bucket? (yes/no): ")
                if ans.lower() != "yes":
                    print("Cancelled.")
                    return
            bname = s3_manager.create_bucket(session, args.name, args.region, public=args.public)
            print("Created bucket:", bname)
        elif args.action == "upload":
            s3_manager.upload_file(session, args.name, args.file, args.key)
            print("Uploaded file")
        elif args.action == "delete-file":
            s3_manager.delete_file(session, args.name, args.key)
            print("Deleted file")
        elif args.action == "delete-bucket":
            s3_manager.delete_bucket(session, args.name)
            print("Deleted bucket")

    elif args.command == "route53":
        if args.action == "list":
            print(route53_manager.list_zones(session))
        elif args.action == "create":
            zone = route53_manager.create_hosted_zone(session, args.zone, args.ref)
            print("Created zone:", zone)
        elif args.action == "add-record":
            route53_manager.add_record(session, args.zone_id, args.record, args.rtype, args.value)
            print("Added record")
        elif args.action == "records":
            recs = route53_manager.list_records(session, args.zone_id, args.zone)
            print("Records:", recs)

if __name__ == "__main__":
    main()
