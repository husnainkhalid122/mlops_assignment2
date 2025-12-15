#!/bin/bash

# MLOps Project Deployment Guide
# This script helps automate AWS deployment

set -e

echo "=========================================="
echo "MLOps Project - AWS Deployment Setup"
echo "=========================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI not found. Installing..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
fi

# Configure AWS credentials
echo ""
echo "Configuring AWS credentials..."
echo "Enter your AWS Access Key ID:"
read -r AWS_ACCESS_KEY_ID
echo "Enter your AWS Secret Access Key:"
read -r AWS_SECRET_ACCESS_KEY
echo "Enter your AWS Region (e.g., us-east-1):"
read -r AWS_REGION

# Configure AWS CLI
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region "$AWS_REGION"

echo ""
echo "=========================================="
echo "Task 6.1 - Creating S3 Bucket"
echo "=========================================="

BUCKET_NAME="mlops-assignment2-bucket-$(date +%s)"

echo "Creating S3 bucket: $BUCKET_NAME"
aws s3 mb "s3://$BUCKET_NAME" --region "$AWS_REGION"

echo "Uploading dataset to S3..."
aws s3 cp data/dataset.csv "s3://$BUCKET_NAME/dataset.csv"

echo ""
echo "S3 Bucket created successfully!"
echo "Bucket URL: https://$BUCKET_NAME.s3.amazonaws.com/dataset.csv"

echo ""
echo "=========================================="
echo "Task 6.2 - Launching EC2 Instance"
echo "=========================================="

# Check if key pair exists
echo "Checking for EC2 key pair..."
KEY_NAME="mlops-key"

if aws ec2 describe-key-pairs --key-names "$KEY_NAME" --region "$AWS_REGION" 2>/dev/null; then
    echo "Key pair already exists"
else
    echo "Creating new key pair: $KEY_NAME"
    aws ec2 create-key-pair --key-name "$KEY_NAME" --region "$AWS_REGION" > "$KEY_NAME.pem"
    chmod 400 "$KEY_NAME.pem"
    echo "Key pair saved to: $KEY_NAME.pem"
fi

# Create security group
echo "Creating security group..."
SG_NAME="mlops-api-sg"
SG_ID=$(aws ec2 create-security-group \
    --group-name "$SG_NAME" \
    --description "Security group for MLOps API" \
    --region "$AWS_REGION" \
    --query 'GroupId' \
    --output text 2>/dev/null || echo "")

if [ -z "$SG_ID" ]; then
    SG_ID=$(aws ec2 describe-security-groups \
        --filters "Name=group-name,Values=$SG_NAME" \
        --region "$AWS_REGION" \
        --query 'SecurityGroups[0].GroupId' \
        --output text)
    echo "Using existing security group: $SG_ID"
else
    echo "Created security group: $SG_ID"
fi

# Add ingress rules
echo "Adding security group rules..."
aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 \
    --region "$AWS_REGION" 2>/dev/null || echo "SSH rule already exists"

aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0 \
    --region "$AWS_REGION" 2>/dev/null || echo "HTTP rule already exists"

aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0 \
    --region "$AWS_REGION" 2>/dev/null || echo "API port rule already exists"

# Get Ubuntu 22.04 LTS AMI ID (Free Tier eligible)
AMI_ID="ami-0c55b159cbfafe1f0"  # us-east-1
if [ "$AWS_REGION" != "us-east-1" ]; then
    echo "Note: AMI ID is for us-east-1. Please update for your region."
fi

# Launch EC2 instance
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type t2.micro \
    --key-name "$KEY_NAME" \
    --security-group-ids "$SG_ID" \
    --region "$AWS_REGION" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=mlops-api-server}]" \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Instance launched: $INSTANCE_ID"
echo "Waiting for instance to start..."
sleep 15

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$AWS_REGION" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo ""
echo "=========================================="
echo "EC2 Instance Details"
echo "=========================================="
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "Key file: $KEY_NAME.pem"
echo ""
echo "SSH Connection:"
echo "ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
echo ""

echo "=========================================="
echo "Deploying API on EC2"
echo "=========================================="

# Create deployment script
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "Updating system..."
sudo apt update
sudo apt upgrade -y

echo "Installing Docker..."
sudo apt install -y docker.io

echo "Adding user to docker group..."
sudo usermod -aG docker ubuntu

echo "Pulling Docker image..."
docker pull gondal2003/mlops-app:v1

echo "Starting API container..."
docker run -d -p 8000:8000 --name mlops-api gondal2003/mlops-app:v1

echo "Waiting for API to start..."
sleep 5

echo "Checking container status..."
docker ps

echo "API deployment completed!"
EOF

chmod +x deploy.sh

# Copy and execute deployment script on EC2
echo "Copying deployment script to EC2..."
scp -i "$KEY_NAME.pem" -o StrictHostKeyChecking=no deploy.sh "ubuntu@$PUBLIC_IP:~/deploy.sh"

echo "Executing deployment script on EC2..."
ssh -i "$KEY_NAME.pem" -o StrictHostKeyChecking=no "ubuntu@$PUBLIC_IP" "bash ~/deploy.sh"

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "S3 Bucket: $BUCKET_NAME"
echo "S3 URL: https://$BUCKET_NAME.s3.amazonaws.com/dataset.csv"
echo ""
echo "EC2 Instance: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "API Endpoint: http://$PUBLIC_IP:8000"
echo "API Health: http://$PUBLIC_IP:8000/health"
echo "Swagger UI: http://$PUBLIC_IP:8000/docs"
echo ""
echo "SSH Command:"
echo "ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
echo ""
echo "Test API (from local machine):"
echo "curl http://$PUBLIC_IP:8000/health"
echo ""
