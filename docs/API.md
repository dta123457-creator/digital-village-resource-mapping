# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently, API endpoints are public. JWT authentication can be enabled in production.

## Endpoints

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "village-resource-mapping-api",
  "version": "0.1.0"
}
```

### Readiness Check
```
GET /readiness
```

**Response:**
```json
{
  "status": "ready",
  "message": "Service is ready to accept requests"
}
```

## Resources Endpoints

### List Resources
```
GET /resources/?skip=0&limit=10&resource_type=School
```

**Parameters:**
- `skip` (int): Number of resources to skip (default: 0)
- `limit` (int): Maximum resources to return (default: 10, max: 100)
- `resource_type` (string, optional): Filter by resource type

**Response:**
```json
[
  {
    "id": 1,
    "name": "School A",
    "resource_type": "School",
    "latitude": 20.593,
    "longitude": 78.963,
    "status": "Active",
    "description": "Primary School"
  }
]
```

### Get Resource
```
GET /resources/{resource_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "School A",
  "resource_type": "School",
  "latitude": 20.593,
  "longitude": 78.963,
  "status": "Active",
  "description": "Primary School"
}
```

### Create Resource
```
POST /resources/
Content-Type: application/json

{
  "name": "New School",
  "resource_type": "School",
  "latitude": 20.595,
  "longitude": 78.965,
  "status": "Active",
  "description": "New Educational Institution"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "name": "New School",
  "resource_type": "School",
  "latitude": 20.595,
  "longitude": 78.965,
  "status": "Active",
  "description": "New Educational Institution"
}
```

### Update Resource
```
PUT /resources/{resource_id}
Content-Type: application/json

{
  "name": "Updated School",
  "resource_type": "School",
  "latitude": 20.595,
  "longitude": 78.965,
  "status": "Active",
  "description": "Updated description"
}
```

### Delete Resource
```
DELETE /resources/{resource_id}
```

**Response (204 No Content)**

## Analysis Endpoints

### Analyze Distribution
```
POST /analysis/distribution
Content-Type: application/json

{
  "resource_type": "School",
  "region": "Maharashtra",
  "time_period": "monthly"
}
```

**Response:**
```json
{
  "resource_type": "School",
  "total_count": 42,
  "average_quality": 0.85,
  "distribution": {
    "urban": 30,
    "rural": 12
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Get Statistics
```
GET /analysis/statistics/{region}
```

**Response:**
```json
{
  "region": "Maharashtra",
  "total_resources": 245,
  "resource_types": {
    "schools": 45,
    "hospitals": 12,
    "wells": 89,
    "roads": 99
  },
  "coverage_percentage": 78.5
}
```

### Quality Assessment
```
POST /analysis/quality-assessment
Content-Type: application/json

{
  "resource_ids": [1, 2, 3, 4, 5]
}
```

**Response:**
```json
{
  "resources_assessed": 5,
  "average_quality_score": 0.82,
  "recommendations": [
    "Upgrade water infrastructure",
    "Improve road maintenance",
    "Expand educational facilities"
  ]
}
```

## Geospatial Endpoints

### Find Nearby Resources
```
POST /geo/nearby-resources
Content-Type: application/json

{
  "point": {
    "latitude": 20.593,
    "longitude": 78.963
  },
  "radius_km": 5.0,
  "resource_type": "School"
}
```

**Response:**
```json
{
  "center": {
    "latitude": 20.593,
    "longitude": 78.963
  },
  "radius_km": 5.0,
  "resources_found": [
    {
      "id": 1,
      "name": "School A",
      "distance_km": 2.3
    },
    {
      "id": 2,
      "name": "Hospital B",
      "distance_km": 3.1
    }
  ]
}
```

### Query by Bounding Box
```
POST /geo/bbox-query
Content-Type: application/json

{
  "min_lat": 20.55,
  "min_lon": 78.90,
  "max_lat": 20.65,
  "max_lon": 79.00
}
```

**Response:**
```json
{
  "bounding_box": {
    "min_lat": 20.55,
    "min_lon": 78.90,
    "max_lat": 20.65,
    "max_lon": 79.00
  },
  "resources_count": 15,
  "resources": [
    {
      "id": 1,
      "name": "School A",
      "latitude": 20.593,
      "longitude": 78.963
    }
  ]
}
```

### Calculate Distance
```
GET /geo/distance/20.593/78.963/20.595/78.965
```

**Response:**
```json
{
  "from": {
    "latitude": 20.593,
    "longitude": 78.963
  },
  "to": {
    "latitude": 20.595,
    "longitude": 78.965
  },
  "distance_km": 0.25
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Testing API

### Using cURL
```bash
# Get all resources
curl http://localhost:8000/api/resources/

# Create a resource
curl -X POST http://localhost:8000/api/resources/ \
  -H "Content-Type: application/json" \
  -d '{"name": "School", "resource_type": "School", "latitude": 20.593, "longitude": 78.963, "status": "Active"}'
```

### Using Python
```python
import requests

API_URL = "http://localhost:8000/api"

# Get resources
response = requests.get(f"{API_URL}/resources/")
print(response.json())

# Create resource
data = {
    "name": "School",
    "resource_type": "School",
    "latitude": 20.593,
    "longitude": 78.963,
    "status": "Active"
}
response = requests.post(f"{API_URL}/resources/", json=data)
print(response.json())
```

### Using Postman
1. Import the API collection from `docs/postman_collection.json`
2. Set base URL to `http://localhost:8000/api`
3. Test endpoints using pre-configured requests
