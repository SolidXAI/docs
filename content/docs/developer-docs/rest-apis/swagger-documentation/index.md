---
title: Swagger Documentation
description: This section provides details on how to access and use the Swagger documentation for SolidX REST APIs.
summary: This document provides comprehensive information about accessing and using SolidX's auto-generated Swagger/OpenAPI documentation. It explains how to access the documentation at the /api/docs endpoint, authenticate using JWT tokens via the login endpoint, and utilize the standard RESTful endpoints automatically generated for each resource. The documentation covers query parameters for filtering, sorting, pagination, population, and field selection, provides example requests for common operations, explains the standardized error handling format with common HTTP status codes, and outlines best practices for authentication, request optimization, error handling, and API documentation maintenance.
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

  <details>
    <summary>
      
      Authentication
    </summary>
    <ul>
      <li>Always use HTTPS</li>
      <li>Keep tokens secure</li>
      <li>Implement token refresh</li>
      <li>Handle token expiration</li>
    </ul>
  </details>

  <details>
    <summary>
      
       Request Optimization
    </summary>
    <ul>
      <li>Use field selection</li>
      <li>Implement pagination</li>
      <li>Optimize queries</li>
      <li>Cache responses</li>
    </ul>
  </details>

  <details>
    <summary>
      
       Error Handling
    </summary>
    <ul>
      <li>Validate input data</li>
      <li>Return meaningful errors</li>
      <li>Log API errors</li>
      <li>Handle rate limiting</li>
    </ul>
  </details>

  <details>
    <summary>
      
       Documentation
    </summary>
    <ul>
      <li>Keep examples up-to-date</li>
      <li>Document all parameters</li>
      <li>Include response examples</li>
      <li>Note any limitations</li>
    </ul>
  </details>

