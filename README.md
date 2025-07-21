# 📷 Photo Storage

A Photo Storage service with AWS S3 storage, JWT authentication and Redis caching.  

## 🚀 Stack of technologies
**Backend**   | Python (FastAPI), Go
**Storage**    | AWS S3           
**Auth**       | JWT              
**Caching**    | Redis            
**Frontend**   | JavaScript/jQuery

## 📦 Installation

### Prerequisites
- Python 3.10+
- Go 1.20+
- Redis 7.0+
- AWS account with S3 access

### Backend Setup
1. Clone the repository:
```bash
git https://github.com/RenSafary/Photo-Storage.git
```
2. Install Python dependencies and start main server (port :8000)
```bash
cd Photo-Storage/app
pip install -r requirements.txt
python3 main.py
```
3. Install Golang dependencies and start microservices (port :8080)
```bash
cd go_services
go mod download
go run main.go 
```
### 🔧 Evironment variables
# JWT Configuration
JWT_SECRET_KEY=your_very_secure_secret
JWT_ALGORITHM=HS256

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your-region
S3_BUCKET_NAME=your-bucket-name
