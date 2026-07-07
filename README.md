# 🔐 JWT Authentication API (FastAPI + PostgreSQL)

A REST API built with FastAPI that demonstrates secure user authentication using JWT access tokens and **refresh token rotation with reuse protection**.

This project was built to learn modern backend architecture, authentication security patterns, database design, and testing practices using Python.

**Last updated:** 07-07-2026

---

## ✨ Features

- User registration and authentication
- JWT-based access tokens (short-lived)
- Refresh token rotation (SPA-ready)
- Refresh token reuse protection
- Logout (single session)
- Logout from all sessions
- Token cleanup endpoint (maintenance)
- Protected API routes
- PostgreSQL database integration (Neon)
- Database migrations with Alembic
- Swagger / OpenAPI documentation
- Clean layered architecture (routes, services, models, schemas)
- Manual unit test suite for JWT validation
- Manual integration test suite for full authentication flows (no pytest required)
- Vue 3 frontend integration for testing authentication flows

---

## 🧰 Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- Alembic
- PyJWT
- Pydantic
- Requests (for integration tests)
- Vue 3 (frontend client)

---

## 🏗️ Project Architecture

The project follows a layered architecture to improve maintainability and separation of concerns.

- routes → API endpoints (HTTP layer)
- services → Business logic and authentication flows
- models → SQLAlchemy database models
- schemas → Pydantic request/response validation
- security → Password hashing and JWT handling
- db → Database configuration and session management
- tests → Manual unit and integration test suites

---

## 🔐 Authentication Flow

This project uses JWT authentication with **refresh token rotation and reuse protection**.

1. User logs in using username and password  
2. Server validates credentials and returns:
   - JWT access token
   - Refresh token
3. Client stores both tokens
4. Access token is used for protected API requests
5. When access token expires:
   - Client sends refresh token to `/refresh-token-spa`
   - Server validates refresh token (JWT + database check)
   - Server issues:
     - New access token
     - New refresh token
   - Old refresh token is invalidated (rotation)
6. If a refresh token is reused:
   - Request is rejected (401 Unauthorized)

This prevents replay attacks using stolen refresh tokens.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

git clone <your-repository-url>  
cd <your-project-folder>

---

### 2. Create a Virtual Environment

python -m venv venv

Activate it:

**Windows (PowerShell)**

venv\Scripts\activate

---

### 3. Install Dependencies

pip install -r requirements.txt

---

### 4. Configure Environment Variables

Create a `.env` file:

DATABASE_URL=your_postgres_connection  
SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=2  
REFRESH_TOKEN_EXPIRE_MINUTES=5  

---

### 5. Run Database Migrations

alembic upgrade head

---

## 🛠️ Development: Creating New Migrations

After modifying a model:

alembic revision --autogenerate -m "describe your change"

Then apply:

alembic upgrade head

---

## 🌐 Vue 3 Frontend (Testing Client)

A companion frontend is available:

https://github.com/persteenolsen/vue-fastapi-jwt-refresh-auth-client

### Features:

- Login flow
- Token storage
- Protected routes
- Refresh token handling

---

## 🧪 Manual Tests

This project includes two manual test suites.

---

### 1. JWT Unit Tests

Pure JWT helper tests (no API calls)

Run:

python -m tests.test_auth_manual

What is tested:

- Valid access token
- Wrong token type rejection
- Expired token rejection
- Invalid signature rejection

---

### 2. Integration Tests (Full Auth Flow)

End-to-end FastAPI authentication tests.

Run:

python -m tests.test_integration_auth

What is tested:

- Login flow
- Refresh token rotation
- Old refresh token reuse rejection
- Logout flow
- Refresh after logout rejection
- Cleanup endpoint
- Admin purge endpoint (optional)

---

## 📊 Example Output

FASTAPI AUTH INTEGRATION TESTS

REFRESH TOKEN ROTATION FLOW
- Login successful
- First refresh successful
- Old refresh token rejected (401)
- Second refresh successful

LOGOUT FLOW
- Logout successful

REVOKED TOKEN REUSE
- Revoked token rejected (401)

TOKEN CLEANUP
- Cleanup executed successfully

JWT VALIDATION TESTS
- Access token accepted
- Wrong type rejected
- Expired token rejected
- Invalid signature rejected

---

## 📡 API Endpoints

### Public

- POST `/token` → Login (access token only)
- POST `/tokens-spa` → Login (access + refresh token)
- POST `/refresh-token-spa` → Refresh tokens (rotation enabled)
- POST `/register` → Create user

### Protected

- GET `/users/me` → Current user
- GET `/protected-route` → Auth test endpoint
- GET `/get-all-users` → List all users

### Admin

- POST `/cleanup-tokens` → Remove expired/revoked tokens
- POST `/admin/purge-refresh-tokens` → Delete all refresh tokens

---

## 🛡️ Security Notes

- Passwords are securely hashed
- Access tokens are short-lived
- Refresh tokens are rotated on each use
- Old refresh tokens are invalidated immediately
- Reused refresh tokens are rejected
- Refresh tokens are stored hashed in DB
- Token identity tracked using `jti`

---

## 🚀 Future Improvements

- Move refresh tokens to HttpOnly cookies
- Add refresh token reuse detection alerts
- Add rate limiting
- Add pytest-based test suite
- Add CI/CD pipeline
- Add Redis session tracking
- Add multi-device session management

---

## 🎯 Learning Goals

- JWT authentication
- Refresh token rotation
- FastAPI backend design
- PostgreSQL + migrations
- Full-stack integration with Vue 3
- Manual testing strategies
- Real-world security patterns

---

## 👨‍💻 Author

Built by Per Olsen

Backend-focused portfolio project exploring authentication systems and scalable API design.