# Task 6 - AWS EC2 + S3 Deployment Guide

This guide provides step-by-step instructions for deploying the MLOps project on AWS.

## Prerequisites

- AWS Account (Free Tier eligible)
- AWS CLI installed locally
- Docker Hub account for pulling images

---

## TASK 6.1 - Create AWS S3 Bucket

### Option A: Using AWS Console (Manual)

1. Go to **AWS Console**: https://console.aws.amazon.com
2. Search for **S3** service
3. Click **Create bucket**
4. Fill in details:
   - **Bucket name**: `mlops-assignment2-bucket-[YOUR-ID]` (globally unique)
   - **Region**: `us-east-1`
5. Click **Create bucket**

### Upload Dataset

1. Click on bucket name
2. Click **Upload** button
3. Select `data/dataset.csv` from your local machine
4. Click **Upload**

### Get S3 URL

1. Click on `dataset.csv` file
2. Copy **Object URL** (format: `https://bucket-name.s3.amazonaws.com/dataset.csv`)

### Option B: Using AWS CLI

```bash
# Set your AWS credentials
aws configure

# Create bucket
BUCKET_NAME="mlops-assignment2-bucket-$(date +%s)"
aws s3 mb s3://$BUCKET_NAME

# Upload dataset
aws s3 cp data/dataset.csv s3://$BUCKET_NAME/

# Get public URL
echo "https://$BUCKET_NAME.s3.amazonaws.com/dataset.csv"
```

---

## TASK 6.2 - Launch EC2 Instance + Deploy API

### Option A: Using CloudFormation (Recommended - Infrastructure as Code)

**This is the automated way:**

```bash
# 1. Go to AWS Console → CloudFormation
# 2. Click "Create Stack"
# 3. Select "Upload a template file"
# 4. Upload: cloudformation-template.yaml
# 5. Fill in parameters:
#    - KeyName: Select your EC2 key pair
#    - BucketName: mlops-assignment2-bucket
# 6. Review and click "Create stack"
# 7. Wait 5-10 minutes for stack creation
# 8. Go to Outputs tab to see results
```

**Outputs will show:**
- S3 Bucket Name
- S3 Bucket URL
- EC2 Instance ID
- EC2 Public IP
- API Endpoint URL
- Swagger UI URL
- SSH Command

### Option B: Using AWS CLI Script

```bash
# Make script executable
chmod +x deploy.sh

# Run deployment script (will prompt for AWS credentials)
./deploy.sh
```

The script will:
1. Create S3 bucket and upload dataset
2. Create EC2 key pair
3. Create security group
4. Launch EC2 instance (t2.micro - Free Tier)
5. Deploy Docker container with API
6. Output all connection details

### Option C: Manual AWS Console Setup

#### Step 1: Create Key Pair

```
EC2 → Key Pairs → Create key pair
- Name: mlops-key
- File format: .pem
- Download and save securely
```

#### Step 2: Create Security Group

```
EC2 → Security Groups → Create security group
- Name: mlops-api-sg
- Rules:
  - SSH (22) - 0.0.0.0/0
  - HTTP (80) - 0.0.0.0/0
  - Custom TCP (8000) - 0.0.0.0/0
```

#### Step 3: Launch Instance

```
EC2 → Instances → Launch instances
- AMI: Ubuntu 22.04 LTS (Free Tier eligible)
- Instance Type: t2.micro
- Key Pair: mlops-key
- Security Group: mlops-api-sg
- Storage: 8 GB (Free Tier default)
- Launch
```

#### Step 4: Connect to Instance

```bash
# Get Public IP from EC2 Dashboard
# Open terminal and run:
ssh -i mlops-key.pem ubuntu@YOUR_PUBLIC_IP
```

#### Step 5: Install Docker and Deploy

```bash
# On the EC2 instance terminal:

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Add user to docker group
sudo usermod -aG docker ubuntu

# Exit and reconnect
exit
ssh -i mlops-key.pem ubuntu@YOUR_PUBLIC_IP

# Pull and run container
docker pull gondal2003/mlops-app:v1
docker run -d -p 8000:8000 --name mlops-api gondal2003/mlops-app:v1

# Verify
docker ps
```

---

## Testing the Deployed API

### Health Check

```bash
curl http://YOUR_EC2_PUBLIC_IP:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Swagger UI

Open in browser:
```
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

Click "Try it out" on any endpoint to test.

### Make Prediction

```bash
curl -X POST http://YOUR_EC2_PUBLIC_IP:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "feature1": 0.496714,
    "feature2": 1.399355,
    "feature3": -0.675178,
    "feature4": -1.907808
  }'
```

Expected response:
```json
{
  "prediction": 1,
  "probability": 0.95,
  "message": "Successfully predicted class 1"
}
```

---

## Pricing (Free Tier)

- **EC2**: 750 hours/month (1 instance)
- **S3**: 5 GB storage + 20,000 GET requests free
- **Data Transfer**: 1 GB/month out

**Total Cost: $0 (within Free Tier limits)**

---

## Important Notes

1. **Security**: 
   - Keep `mlops-key.pem` secure
   - In production, restrict security group rules to specific IPs
   - Use IAM roles instead of access keys

2. **Cost Management**:
   - Stop instance when not in use: `aws ec2 stop-instances --instance-ids i-xxx`
   - Terminate when done: `aws ec2 terminate-instances --instance-ids i-xxx`

3. **Monitoring**:
   - CloudWatch for logs
   - EC2 Dashboard for instance status
   - Use `docker logs mlops-api` on instance

---

## Troubleshooting

### Container won't start
```bash
ssh -i mlops-key.pem ubuntu@YOUR_PUBLIC_IP
docker logs mlops-api
```

### Can't connect on port 8000
```bash
# Check security group allows port 8000
# Check if container is running:
docker ps
```

### Model loading errors
```bash
# Verify Docker image has model
docker pull gondal2003/mlops-app:v1
docker run -it gondal2003/mlops-app:v1 ls -la models/
```

---

## Cleanup

To avoid charges, delete resources when done:

```bash
# Via CloudFormation
aws cloudformation delete-stack --stack-name mlops-stack

# Via CLI
aws ec2 terminate-instances --instance-ids i-xxx
aws s3 rm s3://bucket-name --recursive
aws s3api delete-bucket --bucket bucket-name
```

---

## Summary

| Component | Details |
|-----------|---------|
| **S3 Bucket** | Dataset storage and access |
| **EC2 Instance** | t2.micro (Free Tier) Ubuntu 22.04 |
| **API Container** | gondal2003/mlops-app:v1 on port 8000 |
| **Cost** | Free (within Free Tier) |
| **Access** | Public IP + port 8000 |

**API Endpoint Format:** `http://YOUR_EC2_PUBLIC_IP:8000`
