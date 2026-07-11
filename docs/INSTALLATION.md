# Installation & Setup Guide

## Local Development Setup

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 12+ with PostGIS extension
- Redis 6+
- Git
- Virtual environment tool (venv or conda)

### Step 1: Clone Repository

```bash
git clone https://github.com/dta123457-creator/digital-village-resource-mapping.git
cd digital-village-resource-mapping
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n village-mapping python=3.11
conda activate village-mapping
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/village_mapping
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_SERVER_PORT=8501
```

### Step 5: Setup Database

```bash
# Create database
creatodb village_mapping

# Enable PostGIS extension
psql village_mapping
# In psql:
# CREATE EXTENSION postgis;
# \q
```

### Step 6: Run Application

**Terminal 1 - API Server:**
```bash
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run app/main.py --server.port 8501
```

**Access:**
- Frontend: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Quick Start

```bash
docker-compose up --build
```

Services will start at:
- Streamlit: http://localhost:8501
- API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Stop Services

```bash
docker-compose down
```

## Troubleshooting

### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql
```

### PostGIS Extension Not Found
```bash
# Install PostGIS
sudo apt-get install postgresql-12-postgis

# Or using Homebrew on macOS
brew install postgis
```

### Port Already in Use
```bash
# Change port in .env or use different port
streamlit run app/main.py --server.port 8502
```

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server
```

## Next Steps

1. Check out the [API Documentation](API.md)
2. Read the [Development Guide](DEVELOPMENT.md)
3. Review [Contributing Guidelines](CONTRIBUTING.md)
