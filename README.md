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
2. Starting the main server:
- It will be started on port :8000
```bash
cd Photo-Storage/app
python3 main.py
```
3. Starting the microservices server
- It will be started on port :8080
```bash
cd go_services
go run main.go 
```
