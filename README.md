# Platform CLI – Final Project

A command-line tool for managing AWS EC2, S3, and Route53 resources securely.

---

## Features

- **EC2**
  - List, launch, stop, start, and terminate instances.
  - Instance types restricted to `t3.micro` or `t2.small`.
  - Maximum 2 instances allowed per owner.
  - Automatically fetches the **latest AMI** (Amazon Linux 2023 or Ubuntu 22.04) from SSM Parameter Store.
  - All instances tagged with `CreatedBy=<owner>` for filtering and safety.

- **S3**
  - Create buckets (default: **private + encrypted**).
  - Optionally create **public buckets**, with confirmation prompt.
  - Upload and delete files.
  - List only buckets created by this CLI.
  - Buckets always tagged with `CreatedBy=<owner>`.

- **Route53**
  - Create hosted zones.
  - List hosted zones.
  - Add DNS records.
  - List records per zone.

- **Security & Safety**
  - Uses AWS profiles (`--profile`) – no hardcoded secrets.
  - Consistent resource tagging.
  - Clear CLI output with success/failure.
  - Default S3 settings: **private, encrypted**.

---

## Prerequisites

- Python 3.9+
- AWS CLI installed & configured with profiles:
  aws configure --profile myprofile
  
IAM user/role with permissions for EC2, S3, and Route53.

Installation

Clone the repository and install dependencies:

git clone https://github.com/yoavbrant/Platform-Engineering-Python-Exercise.git

cd Platform-Engineering-Python-Exercise

pip install -r requirements.txt

aws configure --profile <profile-name>

Platform CLI Demonstration

EC2 Commands

List all EC2 instances
python -m platform_cli --profile <profile-name> --region <region-name> ec2 list

Launch a new EC2 instance
python -m platform_cli --profile <profile-name> --region <region-name> ec2 launch --type t2.micro --os amazon

Stop an EC2 instance
python -m platform_cli --profile <profile-name> --region <region-name> ec2 stop --id i-0abc1234def56789

Start an EC2 instance
python -m platform_cli --profile <profile-name> --region <region-name> ec2 start --id i-0abc1234def56789

Terminate an EC2 instance
python -m platform_cli --profile <profile-name> --region <region-name> ec2 terminate --id i-0abc1234def56789

S3 Commands

List all buckets
python -m platform_cli --profile <profile-name> --region <region-name> s3 list

Create a new bucket
python -m platform_cli --profile <profile-name> --region <region-name> s3 create --name <bucket-name>

Create a public bucket (requires confirmation)
python -m platform_cli --profile <profile-name> --region <region-name> s3 create --name <bucket-name> --public

Upload a file
python -m platform_cli --profile <profile-name> --region <region-name> s3 upload --name <bucket-name> --file ./local_file.txt --key remote_file.txt

Delete a file
python -m platform_cli --profile <profile-name> --region <region-name> s3 delete-file --name <bucket-name> --key remote_file.txt

Delete a bucket
python -m platform_cli --profile <profile-name> --region <region-name> s3 delete-bucket --name <bucket-name>

Route53 Commands

List hosted zones
python -m platform_cli --profile <profile-name> --region <region-name> route53 list

Create a hosted zone
python -m platform_cli --profile <profile-name> --region <region-name> route53 create --zone example.com

Add a DNS record
python -m platform_cli --profile <profile-name> --region <region-name> route53 add-record --zone-id <zone-id> --record www.example.com --rtype A --value 1.2.3.4

List records in a hosted zone
python -m platform_cli --profile <profile-name> --region <region-name> route53 records --zone-id <zone-id>


Notes for Demonstration

Always replace <bucket-name>, <zone-id>, <instance-id>, <profile-name>, and <region-name> with actual values returned by previous commands.

The CLI enforces safe defaults (like requiring confirmation for public buckets).
