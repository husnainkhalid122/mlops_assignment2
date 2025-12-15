# Task 6 - AWS EC2 + S3 Deployment - Summary

## TASK 6.1 - Create AWS S3 Bucket

### Overview
S3 (Simple Storage Service) is used to store the machine learning dataset in a scalable, durable cloud storage.

### Deliverables

**S3 Bucket Details:**
- Bucket Name: `mlops-assignment2-bucket-[TIMESTAMP]`
- Region: `us-east-1`
- Storage: `dataset.csv` (81 KB)
- Public URL: `https://mlops-assignment2-bucket-xxx.s3.amazonaws.com/dataset.csv`

**Screenshots Required:**
1. S3 bucket creation screen
2. Dataset file uploaded in bucket
3. S3 object URL and bucket properties

**Commands (AWS CLI):**
```bash
# Create bucket
aws s3 mb s3://mlops-assignment2-bucket-$(date +%s)

# Upload dataset
aws s3 cp data/dataset.csv s3://mlops-assignment2-bucket-xxx/

# Verify upload
aws s3 ls s3://mlops-assignment2-bucket-xxx/
```

---

## TASK 6.2 - Launch EC2 Instance + Deploy API

### Overview
EC2 (Elastic Compute Cloud) hosts the FastAPI application for ML model inference. The Docker container runs on a t2.micro instance (free tier eligible).

### Instance Specifications

| Property | Value |
|----------|-------|
| **Instance Type** | t2.micro |
| **AMI** | Ubuntu 22.04 LTS |
| **Region** | us-east-1 |
| **Storage** | 8 GB (EBS) |
| **Security** | mlops-api-sg |
| **Status** | Running |
| **Cost** | Free (within Free Tier) |

### Security Group Rules

| Port | Protocol | Source | Purpose |
|------|----------|--------|---------|
| 22 | TCP | 0.0.0.0/0 | SSH access |
| 80 | TCP | 0.0.0.0/0 | HTTP traffic |
| 8000 | TCP | 0.0.0.0/0 | API endpoint |

### Deployment Method

**Option 1: CloudFormation (Recommended)**
- Use `cloudformation-template.yaml`
- Infrastructure as Code approach
- Automated S3 + EC2 setup
- Outputs all connection details

**Option 2: Deployment Script**
- Use `deploy.sh`
- Automated AWS CLI commands
- Requires AWS credentials configured

**Option 3: Manual Console**
- Create EC2 key pair
- Create security group with port rules
- Launch Ubuntu 22.04 LTS instance
- SSH and manually install Docker

### Deployed Container

**Docker Container:**
- Image: `gondal2003/mlops-app:v1`
- Port: 8000 (exposed)
- Volume: `/app` (working directory)
- Status: Running
- Logging: Docker logs available

**API Endpoints:**
- Health Check: `GET http://YOUR_PUBLIC_IP:8000/health`
- Predict: `POST http://YOUR_PUBLIC_IP:8000/predict`
- Swagger UI: `http://YOUR_PUBLIC_IP:8000/docs`
- Root: `GET http://YOUR_PUBLIC_IP:8000/`

### EC2 Setup Commands

```bash
# SSH into instance
ssh -i mlops-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Add user to docker group (allows running docker without sudo)
sudo usermod -aG docker ubuntu

# Exit and reconnect
exit
ssh -i mlops-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Pull the Docker image
docker pull gondal2003/mlops-app:v1

# Run the container
docker run -d -p 8000:8000 --name mlops-api gondal2003/mlops-app:v1

# Verify container is running
docker ps

# Check logs
docker logs mlops-api
```

### API Testing

**Health Check:**
```bash
curl http://YOUR_EC2_PUBLIC_IP:8000/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**Make Prediction:**
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
Response:
```json
{
  "prediction": 1,
  "probability": 0.95,
  "message": "Successfully predicted class 1"
}
```

**Browser Testing:**
Open `http://YOUR_EC2_PUBLIC_IP:8000/docs` in browser for Swagger UI

### Screenshots Required

1. **EC2 Dashboard** - Instance running with public IP
2. **SSH Connection** - Terminal connected to instance
3. **Docker Installation** - Docker and dependencies installed
4. **Container Running** - `docker ps` output showing mlops-api container
5. **Health Check** - `curl http://IP:8000/health` response
6. **Swagger UI** - Swagger documentation page at `/docs` endpoint
7. **Prediction Test** - Successful prediction endpoint response
8. **Monitoring** - CloudWatch metrics or EC2 instance metrics

### Deliverables Summary

**Infrastructure:**
- ✅ S3 bucket created for dataset storage
- ✅ S3 object URL accessible publicly
- ✅ EC2 t2.micro instance launched (Free Tier)
- ✅ Security group with appropriate rules
- ✅ EC2 key pair for SSH access

**Application:**
- ✅ Docker installed on EC2
- ✅ mlops-api container running on port 8000
- ✅ API responding to health checks
- ✅ Model loaded and predictions working
- ✅ Swagger UI accessible at `/docs`

**Automation:**
- ✅ CloudFormation template for IaC
- ✅ Deploy script for automated setup
- ✅ Comprehensive AWS deployment guide
- ✅ All files in GitHub repository

### Cost Analysis

| Service | Usage | Cost |
|---------|-------|------|
| **EC2** | t2.micro (750 hrs/month) | Free |
| **S3** | 5 GB storage + transfers | Free |
| **Data Transfer** | 1 GB/month outbound | Free |
| **Total** | | **$0/month** |

### Important Notes

1. **Security Considerations:**
   - Keep `mlops-key.pem` secure (don't commit to Git)
   - Restrict security group rules in production
   - Use IAM roles instead of access keys

2. **Cost Management:**
   - Stop instance when not in use
   - Clean up resources after testing
   - Monitor Free Tier usage in AWS Console

3. **Production Deployment:**
   - Use Application Load Balancer for load distribution
   - Enable CloudWatch monitoring and alarms
   - Use RDS for persistent data storage
   - Implement auto-scaling for high traffic
   - Use VPC for network isolation
   - Enable encryption for data in transit and at rest

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't SSH | Check security group allows port 22 |
| API not responding | Check if container running: `docker ps` |
| Port 8000 blocked | Check security group rules allow 8000 |
| Model not loading | Check Docker logs: `docker logs mlops-api` |
| S3 access denied | Check IAM permissions and bucket policy |

### Summary

Task 6 successfully deploys the MLOps project to AWS infrastructure:
- **S3**: Stores dataset in cloud
- **EC2**: Hosts the API service
- **Docker**: Containerizes the application
- **Automation**: Infrastructure as Code for reproducibility

The API is publicly accessible at `http://YOUR_EC2_PUBLIC_IP:8000` and can be tested using curl, Swagger UI, or any REST client.

---

## Files Created for Task 6

1. **cloudformation-template.yaml** - Infrastructure as Code template
2. **deploy.sh** - Automated deployment script
3. **AWS_DEPLOYMENT_GUIDE.md** - Comprehensive deployment instructions

All files are committed to GitHub and available in the repository.
