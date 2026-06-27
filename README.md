# Serverless User Directory

A fully serverless REST API built on AWS that syncs users from an external source and exposes search, lookup, and listing endpoints. Deployed automatically via GitHub Actions using OpenID Connect (no long-lived AWS credentials).

---

## Architecture

```
GitHub Actions (OIDC)
        │
        ▼
   AWS SAM Deploy
        │
        ▼
┌──────────────────────────────────────────────────┐
│                  API Gateway                     │
│                                                  │
│  GET  /v1/health           → HealthFunction      │
│  GET  /v1/users            → UsersFunction       │
│  GET  /v1/users/{id}       → UserDetailsFunction │
│  GET  /v1/users/search     → SearchUsersFunction │
│  POST /v1/admin/sync-users → SyncUsersFunction   │
└──────────────────────────────────────────────────┘
        │                          │
        ▼                          ▼
   DynamoDB Table           Secrets Manager
   (users-table)        (user-directory-secrets)
                                   │
                                   ▼
                          External Users API
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Compute | AWS Lambda (Python 3.12) |
| API | AWS API Gateway (REST) |
| Database | AWS DynamoDB (on-demand) |
| Secrets | AWS Secrets Manager |
| IaC | AWS SAM (CloudFormation) |
| CI/CD | GitHub Actions + OIDC |

---

## API Endpoints

### Health Check
```
GET /v1/health
```
```json
{ "status": "healthy" }
```

### List All Users
```
GET /v1/users
```
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "firstName": "John",
    "lastName": "Doe"
  }
]
```

### Get User by ID
```
GET /v1/users/{id}
```
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe"
}
```
Returns `404` if user is not found. Returns `400` if the ID is not a valid number.

### Search Users
```
GET /v1/users/search?username=johndoe
GET /v1/users/search?email=john@example.com
GET /v1/users/search?firstName=John
GET /v1/users/search?lastName=Doe
```
Supported fields: `username`, `email`, `firstName`, `lastName`

### Sync Users (Admin)
```
POST /v1/admin/sync-users
```
Fetches users from the configured external API and upserts them into DynamoDB.
```json
{
  "message": "Users synced successfully",
  "usersProcessed": 10
}
```

---

## Project Structure

```
├── src/
│   ├── handlers/
│   │   ├── health.py           # GET /v1/health
│   │   ├── users.py            # GET /v1/users
│   │   ├── user_details.py     # GET /v1/users/{id}
│   │   ├── search_users.py     # GET /v1/users/search
│   │   └── sync_users.py       # POST /v1/admin/sync-users
│   ├── services/
│   │   ├── dynamodb_service.py # DynamoDB read/write with full pagination
│   │   ├── external_api_service.py # External API integration
│   │   └── secrets_service.py  # Secrets Manager access
│   └── utils/
│       └── json_utils.py       # Shared JSON encoder (DynamoDB Decimal support)
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── template.yaml               # SAM/CloudFormation infrastructure
├── samconfig.toml              # SAM deployment config
└── requirements.txt            # Python dependencies
```

---

## Deployment

### Prerequisites
- [AWS CLI](https://aws.amazon.com/cli/) configured
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) installed
- Python 3.12

### Local Build & Deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Build the SAM application
sam build

# Deploy (first time — interactive)
sam deploy --guided

# Deploy (subsequent)
sam deploy
```

### Secrets Setup

Before syncing users, create the following secret in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name user-directory-secrets \
  --secret-string '{
    "API_BASE_URL": "https://your-api.example.com/users",
    "API_KEY": "your-api-key"
  }'
```

### CI/CD via GitHub Actions

The pipeline triggers on every push to `main`. It uses **OIDC** to assume an IAM role — no AWS access keys are stored in GitHub Secrets.

**Required GitHub Actions secret:**
- The IAM role ARN is hardcoded in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) — update it to match your AWS account.

---

## Design Decisions

**Why DynamoDB on-demand?**
No capacity planning needed — the table scales automatically and costs nothing when idle, making it ideal for a portfolio/demo project.

**Why OIDC instead of IAM access keys in CI/CD?**
OIDC lets GitHub Actions assume an IAM role directly without storing long-lived credentials as secrets — a security best practice for production pipelines.

**Why Secrets Manager for the external API credentials?**
Keeps secrets out of environment variables and IAM policies enforce least-privilege access to the specific secret ARN.

---

## License

MIT
