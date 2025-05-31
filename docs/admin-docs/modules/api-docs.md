---
sidebar_position: 5
---

# API Documentation

SOLID automatically generates comprehensive API documentation for all your endpoints using Swagger/OpenAPI specification. This documentation provides developers with an interactive interface to explore and test the APIs.

## Accessing API Documentation

To access the Swagger documentation:

1. Navigate to your SOLID installation
2. Go to `/api/docs` endpoint
3. You'll see the Swagger UI with all available endpoints

## Authentication

Before using the APIs, you'll need to authenticate:

1. Use the `/api/auth/login` endpoint
2. Provide your credentials
3. Receive a JWT token
4. Use this token in the Authorization header for subsequent requests

### Example Authentication Flow

```bash
# Login request
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "yourpassword"
}

# Response
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    ...
  }
}

# Using the token
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## API Structure

### Resource Endpoints

Each resource in your SOLID app automatically gets the following RESTful endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{resource}` | List resources |
| GET | `/api/{resource}/{id}` | Get single resource |
| POST | `/api/{resource}` | Create resource |
| PUT | `/api/{resource}/{id}` | Update resource |
| DELETE | `/api/{resource}/{id}` | Delete resource |

### Query Parameters

The list endpoint supports various query parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| filters | Filter records | `?filters[status]=active` |
| sort | Sort records | `?sort=created_at:desc` |
| pagination | Paginate results | `?page=1&limit=10` |
| populate | Include relationships | `?populate=author,comments` |
| fields | Select specific fields | `?fields=title,content` |

### Example Requests

#### List Records with Filtering
```bash
GET /api/posts?filters[status]=published&sort=created_at:desc
```

#### Create Record
```bash
POST /api/posts
{
  "title": "New Post",
  "content": "Post content",
  "status": "draft"
}
```

#### Update Record
```bash
PUT /api/posts/1
{
  "status": "published"
}
```

## Error Handling

All API errors follow a consistent format:

```json
{
  "error": {
    "status": 400,
    "name": "ValidationError",
    "message": "Title is required",
    "details": {
      "fields": {
        "title": ["This field is required"]
      }
    }
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation failed |
| 500 | Internal Server Error |

## Best Practices

1. **Authentication**
   - Always use HTTPS
   - Keep tokens secure
   - Implement token refresh
   - Handle token expiration

2. **Request Optimization**
   - Use field selection
   - Implement pagination
   - Optimize queries
   - Cache responses

3. **Error Handling**
   - Validate input data
   - Return meaningful errors
   - Log API errors
   - Handle rate limiting

4. **Documentation**
   - Keep examples up-to-date
   - Document all parameters
   - Include response examples
   - Note any limitations
