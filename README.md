# 🛠 Platform CLI – Final Project

A command-line tool for securely managing **AWS EC2**, **S3**, and **Route53** resources.

---

## Features

### EC2
- **List, launch, stop, start, and terminate instances.**
- Instance types restricted to `t3.micro` or `t2.small`.
- Maximum **2 instances per owner**.
- Automatically fetches the **latest AMI** (Amazon Linux 2023 or Ubuntu 22.04) from SSM Parameter Store.
- Instances are tagged with `CreatedBy=<owner>` for filtering and safety.

### S3
- Create buckets (**private + encrypted by default**).
- Optionally create **public buckets** (requires confirmation).
- Upload and delete files.
- List only buckets created by this CLI.
- Buckets are always tagged with `CreatedBy=<owner>`.

### Route53
- Create hosted zones.
- List hosted zones.
- Add DNS records.
- List records per zone.

### Security & Safety
- Uses AWS profiles (`--profile`) — no hardcoded secrets.
- Consistent tagging for all resources.
- Clear CLI output with success/failure messages.
- Safe defaults (private, encrypted S3 buckets).

---

## ⚙ Prerequisites

- Python 3.9+
- AWS CLI installed
- IAM user/role with permissions for **EC2, S3, and Route53**

# Clone the repository
git clone https://github.com/yoavbrant/Platform-Engineering-Python-Exercise.git

# Navigate into the project directory
cd Platform-Engineering-Python-Exercise

# Install dependencies
pip install -r requirements.txt

# Configure your AWS profile:
aws configure --profile <profile-name>

## Platform CLI Demonstration
Replace placeholders with real values.

### EC2 Commands

#### List all EC2 instances

python -m platform_cli --profile <profile-name> --region <region-name> ec2 list

#### Launch a new EC2 instance

python -m platform_cli --profile <profile-name> --region <region-name> ec2 launch --type t2.micro --os amazon

#### Stop an EC2 instance

python -m platform_cli --profile <profile-name> --region <region-name> ec2 stop --id <instance-id>

#### Start an EC2 instance

python -m platform_cli --profile <profile-name> --region <region-name> ec2 start --id <instance-id>

#### Terminate an EC2 instance

python -m platform_cli --profile <profile-name> --region <region-name> ec2 terminate --id <instance-id>

### S3 Commands

#### List all buckets

python -m platform_cli --profile <profile-name> --region <region-name> s3 list

#### Create a new bucket

python -m platform_cli --profile <profile-name> --region <region-name> s3 create --name <bucket-name>

#### Create a public bucket (requires confirmation)

python -m platform_cli --profile <profile-name> --region <region-name> s3 create --name <bucket-name> --public

#### Upload a file

python -m platform_cli --profile <profile-name> --region <region-name> s3 upload --name <bucket-name> --file ./local_file.txt --key remote_file.txt

#### Delete a file

python -m platform_cli --profile <profile-name> --region <region-name> s3 delete-file --name <bucket-name> --key remote_file.txt

#### Delete a bucket

python -m platform_cli --profile <profile-name> --region <region-name> s3 delete-bucket --name <bucket-name>

### Route53 Commands

#### List hosted zones

python -m platform_cli --profile <profile-name> --region <region-name> route53 list

#### Create a hosted zone

python -m platform_cli --profile <profile-name> --region <region-name> route53 create --zone example.com

#### Add a DNS record

python -m platform_cli --profile <profile-name> --region <region-name> route53 add-record --zone-id <zone-id> --record www.example.com --rtype A --value 1.2.3.4

#### List records in a hosted zone

python -m platform_cli --profile <profile-name> --region <region-name> route53 records --zone-id <zone-id>

### Notes for Demonstration

- Always replace placeholders with values returned by previous commands.

- Safe defaults: public S3 buckets require confirmation.

- All resources are tagged for ownership and easy filtering.
