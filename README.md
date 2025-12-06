# External Wrapper - API Gateway

A Django-based API gateway service that securely wraps internal APIs for external client access with JWT authentication and service-level permissions.

## Overview

This gateway acts as a bridge between external clients and internal APIs, providing:
- JWT-based authentication
- Service-level access control via user groups
- HTTP method enforcement
- Automatic pagination URL rewriting

## Quick Start

### Prerequisites
- Python 3.12
- Oracle database
- Docker (optional)

### Environment Setup

1. **Create environment directory:**
   ```bash
   mkdir -p .app_envs/development
   cp sample_envs/development/sample_env .app_envs/development/.env
   ```

2. **Configure your `.env` file** with database credentials, secret keys, and service URLs.

### Running Without Docker

```bash
pip install -r requirements/development.txt

python manage.py collectstatic

python manage.py migrate

python manage.py runserver
```

### Running With Docker

```bash
# Build and run
ENVIRONMENT=development DOCKER_TAG=dev1 DOCKER_REPO_URL=docker.io \
APP_LOG_PATH=/app/logs APP_EXTERNAL_PORT=8000 APP_INTERNAL_PORT=8000 \
APP_ENVIRONMENT_VARIABLES_PATH=./.app_envs/development/.env docker compose -f docker-compose-dev.yaml up --build
```

## Admin Panel Configuration

### 1. Access Admin Panel
Navigate to `/admin` and login with superuser credentials.

### 2. Create Gateway Service
Go to **Gateway Services** and click **Add**:

- **Service Name**: Unique identifier (snake_case, e.g., `user_profile`)
- **Base URL**: Internal service URL (e.g., `http://internal-api.sos.com`)
- **Internal API URL**: API endpoint path (e.g., `/api/v1/users/profile/`)
- **HTTP Method**: Allowed method (GET, POST, PUT, PATCH, DELETE)
- **Visible to All**: Enable for public access, or specify a **Required Group**
- **Is Active**: Toggle to enable/disable service

**Service Code** is auto-generated from the service ID.

### 3. Assign User Permissions
- Create a Group (if using group-based access)
- Add users to the group
- Link the group to the Gateway Service via **Required Group** field

## API Usage

### Making Requests

External clients must include:
- **Authorization Header**: `Bearer <JWT_TOKEN>`
- **Service-Code Header**: The service's numeric code

**Example:**
```bash
curl -X GET https://claim.isos.co/external-wrapper/gate/api/v1/services/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Service-Code: 123"
```

The gateway will:
1. Authenticate the user
2. Verify service permissions
3. Forward the request to the internal API
4. Return the response with rewritten pagination URLs

## Architecture

```
External Client → Gateway (JWT Auth + Service Check) → Internal API
```

**Key Components:**
- `ServiceGatewayAPIView`: Core proxy logic with httpx connection pooling
- `GatewayService`: Model defining service routing and permissions
- Automatic pagination URL rewriting for seamless client experience

## Environment Files

Place environment files in:
- `.app_envs/development/.env`
- `.app_envs/staging/.env`
- `.app_envs/production/.env`
- `.app_envs/docker/.env`

Use `sample_envs/` as templates.

## Health Check

Access `/health/` to verify service status.

## Support

Please attempt to resolve your issue before asking for help.
Get your hands dirty. Code is washable.
