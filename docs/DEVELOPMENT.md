# Development Guide

## Setting Up Your Development Environment

### 1. Prerequisites
```bash
# Check Python version
python --version  # Should be 3.9+

# Check Git
git --version
```

### 2. Initial Setup
```bash
# Clone repository
git clone https://github.com/dta123457-creator/digital-village-resource-mapping.git
cd digital-village-resource-mapping

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-cov black flake8 mypy
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your local settings
```

## Project Structure Understanding

```
app/
├── api/              # FastAPI backend
│   ├── main.py      # App initialization
│   └── routes/      # Endpoint definitions
├── models/          # SQLAlchemy ORM models
├── ml/              # Machine learning modules
├── utils/           # Utility functions
├── main.py          # Streamlit frontend
├── config.py        # Configuration
└── logger.py        # Logging setup
```

## Running the Application

### Option 1: Local Development
```bash
# Terminal 1: API
uvicorn app.api.main:app --reload

# Terminal 2: Frontend
streamlit run app/main.py
```

### Option 2: Docker
```bash
docker-compose up --build
```

## Code Style & Standards

### Formatting
```bash
# Format code with Black
black app/

# Check style
flake8 app/
```

### Type Checking
```bash
# Run type checker
mypy app/
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_api.py
```

### Writing Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## Common Development Tasks

### Adding a New API Endpoint

1. **Create route file** (`app/api/routes/new_route.py`):
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "success"}
```

2. **Include in main app** (`app/api/main.py`):
```python
from app.api.routes import new_route
app.include_router(new_route.router, prefix="/api/new", tags=["New"])
```

### Adding a New Database Model

1. **Create model file** (`app/models/new_model.py`):
```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
```

2. **Create migration**:
```bash
alembic revision --autogenerate -m "Add new_model table"
alembic upgrade head
```

### Adding a New Utility Function

1. **Create function** (`app/utils/new_util.py`):
```python
def calculate_something(data):
    """Calculate something useful."""
    # Implementation
    return result
```

2. **Use in code**:
```python
from app.utils.new_util import calculate_something
```

## Debugging

### Debug API
```python
# Add debug logging
from app.logger import logger

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Debug Streamlit
```python
import streamlit as st

# Show debug info
st.write("Debug:", variable)
st.json({"key": "value"})
```

### Using Debugger
```python
import pdb
pdb.set_trace()  # Breakpoint
```

## Database Management

### Creating Migrations
```bash
# Auto-generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Database Shell
```bash
# Connect to PostgreSQL
psql -U user -d village_mapping

# Useful commands
\dt              # List tables
\d table_name    # Describe table
\q              # Quit
```

## Performance Profiling

```python
# Measure function execution time
import time

start = time.time()
# Code to profile
end = time.time()
print(f"Execution time: {end - start}s")
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add .
git commit -m "Add feature description"

# Push to remote
git push origin feature/your-feature

# Create pull request on GitHub
```

## Common Issues & Solutions

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Connection Issues
```bash
# Check PostgreSQL
psql -U user -h localhost

# Check connection string
echo $DATABASE_URL
```

### Port Already in Use
```bash
# Kill process on port
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [PostGIS Docs](https://postgis.net/documentation/)

## Getting Help

- Check existing issues: GitHub Issues
- Ask questions: GitHub Discussions
- Read documentation: `docs/` folder
- Contact: dta123457@gmail.com
