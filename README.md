# Platform CLI – Final Project

A command-line tool for managing AWS EC2, S3, and Route53 resources securely, with strong restrictions and best practices.

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

## 🔧 Prerequisites

- Python 3.9+
- AWS CLI installed & configured with profiles:
  aws configure --profile myprofile
  
IAM user/role with permissions for EC2, S3, and Route53.

Installation

Clone the repository and install dependencies:

git clone https://github.com/yoavbrant/Platform-Engineering-Python-Exercise.git
cd Platform-Engineering-Python-Exercise
pip install -r requirements.txt

Usage

Run the CLI using:

python -m platform_cli --profile <aws-profile> --region <aws-region> <service> <command>

EC2: Create / List / Start / Stop
$ python -m platform_cli --profile yoav --region us-east-1 ec2 create --type t2.micro
Launched instance: i-0abcd1234ef567890

$ python -m platform_cli --profile yoav --region us-east-1 ec2 list
Current EC2 instances:
[{'id': 'i-0abcd1234ef567890', 'state': 'pending', 'type': 't2.micro'}]

$ python -m platform_cli --profile yoav --region us-east-1 ec2 start --id i-0abcd1234ef567890
Started instance: i-0abcd1234ef567890

$ python -m platform_cli --profile yoav --region us-east-1 ec2 stop --id i-0abcd1234ef567890
Stopped instance: i-0abcd1234ef567890

S3: Create / Upload / List
$ python -m platform_cli --profile yoav --region us-east-1 s3 create --name demo-bucket-yoav-123
Created bucket: demo-bucket-yoav-123

$ python -m platform_cli --profile yoav --region us-east-1 s3 upload --bucket demo-bucket-yoav-123 --file ./README.md
Uploaded ./README.md to s3://demo-bucket-yoav-123/README.md

$ python -m platform_cli --profile yoav --region us-east-1 s3 list
S3 buckets:
['demo-bucket-yoav-123']

Route53: Zone + DNS Record
$ python -m platform_cli --profile yoav --region us-east-1 route53 create-zone --name example.com
Created hosted zone: Z123456789ABCDEFG (example.com)

$ python -m platform_cli --profile yoav --region us-east-1 route53 create-record \
    --zone-id Z123456789ABCDEFG \
    --name test.example.com \
    --type A \
    --value 1.2.3.4
Created record: test.example.com -> 1.2.3.4

