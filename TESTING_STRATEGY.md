# Trendit API Testing Strategy

## Admin Test User Endpoint

### Overview
A secure endpoint for creating consistent test users with known credentials and API keys. Perfect for testing, development, and CI/CD pipelines.

### Setup Requirements

1. **Environment Variable**: Add to your `.env` file:
   ```bash
   ADMIN_SECRET_KEY=your-secure-admin-key-here
   ```

2. **Deploy Changes**: The new endpoint is added to `backend/api/auth.py` and needs to be deployed.

### Usage

#### Create/Reset Test User
```bash
curl -X POST "https://api.potterlabs.xyz/auth/create-test-user" \
  -H "Content-Type: application/json" \
  -d '{"admin_key": "YOUR_ADMIN_SECRET_KEY"}'
```

#### Response
```json
{
  "message": "Test user created successfully",
  "user": {
    "id": 123,
    "email": "test@trendit.dev",
    "username": "trendit_tester", 
    "password": "TestPassword123"
  },
  "api_key": "tk_ABC123..." 
}
```

### Test User Specifications

- **Email**: `test@trendit.dev`
- **Username**: `trendit_tester` 
- **Password**: `TestPassword123`
- **Subscription Status**: `ACTIVE` (bypasses all limits)
- **API Key**: Automatically generated with `tk_` prefix

### Testing Workflow

```bash
# 1. Create/reset test user
RESPONSE=$(curl -s -X POST "https://api.potterlabs.xyz/auth/create-test-user" \
  -H "Content-Type: application/json" \
  -d '{"admin_key": "YOUR_ADMIN_KEY"}')

# 2. Extract API key
API_KEY=$(echo "$RESPONSE" | jq -r '.api_key')
echo "Test API Key: $API_KEY"

# 3. Test any endpoint
curl -X GET "https://api.potterlabs.xyz/api/scenarios/1/subreddit-keyword-search?subreddit=python&keywords=fastapi&date_from=2024-01-01&date_to=2024-12-31&limit=1" \
  -H "Authorization: Bearer $API_KEY"

# 4. Test JWT login (alternative)
curl -X POST "https://api.potterlabs.xyz/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@trendit.dev", "password": "TestPassword123"}'
```

### Security Features

- **Admin Key Protected**: Requires `ADMIN_SECRET_KEY` environment variable
- **Idempotent**: Can be called multiple times safely
- **Resets State**: Clears old API keys and creates fresh ones
- **Active Subscription**: Test user has ACTIVE status for unlimited testing

### Deployment Steps

1. **Add Environment Variable**: 
   ```bash
   # In your production environment
   ADMIN_SECRET_KEY=super-secret-admin-key-2024
   ```

2. **Deploy Backend**: Push the changes to your deployment platform (Render, etc.)

3. **Verify Deployment**: 
   ```bash
   curl -X POST "https://api.potterlabs.xyz/auth/create-test-user" \
     -H "Content-Type: application/json" \
     -d '{"admin_key": "wrong-key"}'
   # Should return 403 Forbidden
   ```

4. **Create Test User**:
   ```bash
   curl -X POST "https://api.potterlabs.xyz/auth/create-test-user" \
     -H "Content-Type: application/json" \
     -d '{"admin_key": "your-actual-admin-key"}'
   ```

### Error Responses

#### Invalid Admin Key (403)
```json
{
  "detail": "Invalid admin key"
}
```

#### Missing Admin Key Environment Variable (403)
```json
{
  "detail": "Invalid admin key"
}
```

### Alternative Testing Methods

If you prefer not to use the admin endpoint:

#### Method 1: Manual User Creation
```bash
# Create user manually
curl -X POST "https://api.potterlabs.xyz/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "mytest", "email": "mytest@example.com", "password": "MyPassword123"}'

# Login for JWT
curl -X POST "https://api.potterlabs.xyz/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "mytest@example.com", "password": "MyPassword123"}'

# Create API key with JWT
curl -X POST "https://api.potterlabs.xyz/auth/api-keys" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Test Key"}'
```

#### Method 2: Environment-based Test Script
Create a local script that manages test credentials:

```bash
#!/bin/bash
# test_credentials.sh

# Generate unique test user
TIMESTAMP=$(date +%s)
EMAIL="test-$TIMESTAMP@example.com"
PASSWORD="TestPass123"

# Register and get API key
register_response=$(curl -s -X POST "https://api.potterlabs.xyz/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

login_response=$(curl -s -X POST "https://api.potterlabs.xyz/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

JWT=$(echo "$login_response" | jq -r '.access_token')

api_key_response=$(curl -s -X POST "https://api.potterlabs.xyz/auth/api-keys" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Key"}')

API_KEY=$(echo "$api_key_response" | jq -r '.key')

echo "Test Credentials Created:"
echo "Email: $EMAIL"
echo "Password: $PASSWORD"
echo "API Key: $API_KEY"
echo ""
echo "Test command:"
echo "curl -H 'Authorization: Bearer $API_KEY' 'https://api.potterlabs.xyz/api/scenarios/examples'"
```

## Recommendation

**Use the Admin Test User Endpoint** for the most reliable testing experience:

1. ✅ Consistent credentials every time
2. ✅ ACTIVE subscription status (no limits)
3. ✅ Fresh API key on each call
4. ✅ Perfect for automation and CI/CD
5. ✅ Secure (admin key protected)

The endpoint will be available once you deploy the backend changes and set the `ADMIN_SECRET_KEY` environment variable.