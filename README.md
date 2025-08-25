# Platform CLI – Final Project

A command-line tool for managing AWS EC2, S3, and Route53 resources securely, with strong restrictions and best practices.

---

## ✅ Features

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
  ```bash
  aws configure --profile myprofile
IAM user/role with permissions for EC2, S3, and Route53.

Install dependencies:

bash
Copy
Edit
pip install boto3
▶️ Running the CLI
On Linux/macOS
bash
Copy
Edit
python3 -m platform_cli --profile myprofile --region us-east-1 ec2 list
On Windows (PowerShell / CMD)
bash
Copy
Edit
python -m platform_cli --profile myprofile --region us-east-1 ec2 list
🧪 Testing
Run the automated test:

bash
Copy
Edit
python test_script.py
Or run individual commands manually (see below).

📋 Example CLI Commands
These commands replicate the functionality tested in test_script.py.

EC2
bash
Copy
Edit
# List instances
python -m platform_cli --profile myprofile --region us-east-1 ec2 list

# Launch instance (Amazon Linux 2023, t3.micro)
python -m platform_cli --profile myprofile --region us-east-1 ec2 launch --type t3.micro --ami amazon

# Stop instance
python -m platform_cli --profile myprofile --region us-east-1 ec2 stop --id i-xxxxxxxxxxxx

# Start instance
python -m platform_cli --profile myprofile --region us-east-1 ec2 start --id i-xxxxxxxxxxxx

# Terminate instance
python -m platform_cli --profile myprofile --region us-east-1 ec2 terminate --id i-xxxxxxxxxxxx
S3
bash
Copy
Edit
# Create private bucket
python -m platform_cli --profile myprofile --region us-east-1 s3 create --name my-test-bucket

# Create public bucket (asks confirmation)
python -m platform_cli --profile myprofile --region us-east-1 s3 create --name my-public-bucket --public

# Upload file
python -m platform_cli --profile myprofile --region us-east-1 s3 upload --bucket my-test-bucket --file ./localfile.txt --key remote.txt

# Delete file
python -m platform_cli --profile myprofile --region us-east-1 s3 delete-file --bucket my-test-bucket --key remote.txt

# List buckets created by CLI
python -m platform_cli --profile myprofile --region us-east-1 s3 list

# Delete bucket
python -m platform_cli --profile myprofile --region us-east-1 s3 delete --bucket my-test-bucket
Route53
bash
Copy
Edit
# Create hosted zone
python -m platform_cli --profile myprofile --region us-east-1 route53 create --domain test1234.com

# List hosted zones
python -m platform_cli --profile myprofile --region us-east-1 route53 list

# Add DNS record
python -m platform_cli --profile myprofile --region us-east-1 route53 add-record --zone-id Z12345ABCDE --name www.test1234.com --type A --value 1.2.3.4 --ttl 60

# List records in a zone
python -m platform_cli --profile myprofile --region us-east-1 route53 list-records --zone-id Z12345ABCDE
📌 Notes
S3 buckets must have globally unique names.

Public buckets will ask for confirmation before creation.

EC2 instance limit: 2 per owner.

Default AMIs pulled dynamically via SSM Parameter Store.
