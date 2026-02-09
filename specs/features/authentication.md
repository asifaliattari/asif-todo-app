# Feature: User Authentication

**Author**: Asif Ali AstolixGen
**Phase**: Phase II
**Priority**: Critical (Required)

## Overview

Implement secure user signup and login using Better Auth with JWT tokens. Users must authenticate to access the todo application.

## User Stories

### US-AUTH-1: User Signup
**As a new user**, I want to create an account so that I can use the todo application.

**Acceptance Criteria**:
- User can access signup page at `/signup`
- User provides: Name, Email, Password
- Email must be valid format and unique
- Password must be at least 8 characters
- Password is securely hashed before storage
- Account is created in database
- User is automatically logged in after signup
- JWT token is generated and stored
- User is redirected to dashboard

### US-AUTH-2: User Login
**As a registered user**, I want to log in so that I can access my tasks.

**Acceptance Criteria**:
- User can access login page at `/login`
- User provides: Email, Password
- System verifies credentials
- On success: JWT token generated and stored
- On success: User redirected to dashboard
- On failure: Error message displayed
- Password is never exposed in responses

### US-AUTH-3: Stay Logged In
**As a logged-in user**, I want to stay logged in across page refreshes so that I don't have to login repeatedly.

**Acceptance Criteria**:
- JWT token is stored in localStorage
- Token is included in all API requests
- Token is verified on each request
- User remains logged in until explicit logout
- Token expires after 7 days (configurable)

### US-AUTH-4: Logout
**As a logged-in user**, I want to log out so that others can't access my account.

**Acceptance Criteria**:
- User can click logout button
- JWT token is removed from storage
- User is redirected to login page
- Subsequent API calls fail (401 Unauthorized)

### US-AUTH-5: Protected Routes
**As a visitor**, I should not access the dashboard without logging in.

**Acceptance Criteria**:
- Unauthenticated users accessing `/` are redirected to `/login`
- Authenticated users accessing `/login` or `/signup` are redirected to `/`
- API endpoints return 401 if no valid token provided

## Technical Specifications

### Authentication Flow

```
User Signup Flow:
1. User fills signup form (name, email, password)
2. Frontend validates input
3. POST /api/auth/signup
4. Backend:
   - Validates email doesn't exist
   - Hashes password with bcrypt
   - Creates user in database
   - Generates JWT token
   - Returns { token, user: { id, name, email } }
5. Frontend:
   - Stores token in localStorage
   - Stores user info in context/state
   - Redirects to dashboard

User Login Flow:
1. User fills login form (email, password)
2. Frontend validates input
3. POST /api/auth/login
4. Backend:
   - Finds user by email
   - Verifies password hash
   - Generates JWT token
   - Returns { token, user: { id, name, email } }
5. Frontend:
   - Stores token in localStorage
   - Stores user info in context/state
   - Redirects to dashboard

API Request with Authentication:
1. Frontend makes API call (e.g., GET /api/tasks)
2. Frontend includes: Authorization: Bearer <JWT_TOKEN>
3. Backend middleware:
   - Extracts token from header
   - Verifies token signature
   - Decodes user_id from token
   - Attaches user_id to request
4. Route handler uses user_id to filter data
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id_123",
    "email": "user@example.com",
    "name": "User Name",
    "iat": 1234567890,
    "exp": 1234567890
  },
  "signature": "..."
}
```

### Password Hashing

- **Algorithm**: bcrypt
- **Salt Rounds**: 10 (configurable)
- **Storage**: Store only hash, never plaintext
- **Verification**: bcrypt.compare(plaintext, hash)

### JWT Secret

- **Environment Variable**: `BETTER_AUTH_SECRET`
- **Requirement**: Same secret on frontend and backend
- **Length**: At least 32 characters
- **Generation**: `openssl rand -base64 32`

## API Requirements

### Signup Endpoint

```
POST /api/auth/signup
Content-Type: application/json

Request:
{
  "name": "Asif Ali AstolixGen",
  "email": "asif@example.com",
  "password": "SecurePass123"
}

Success Response (201 Created):
{
  "token": "eyJhbGc...",
  "user": {
    "id": "user_123",
    "name": "Asif Ali AstolixGen",
    "email": "asif@example.com",
    "created_at": "2026-02-10T00:00:00Z"
  }
}

Error Responses:
400 Bad Request - Invalid input
409 Conflict - Email already exists
500 Internal Server Error - Server error
```

### Login Endpoint

```
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "asif@example.com",
  "password": "SecurePass123"
}

Success Response (200 OK):
{
  "token": "eyJhbGc...",
  "user": {
    "id": "user_123",
    "name": "Asif Ali AstolixGen",
    "email": "asif@example.com",
    "created_at": "2026-02-10T00:00:00Z"
  }
}

Error Responses:
400 Bad Request - Invalid input
401 Unauthorized - Invalid credentials
500 Internal Server Error - Server error
```

## Frontend Requirements

### Better Auth Configuration

```typescript
// lib/auth.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  // Other Better Auth config
});
```

### Auth Context

```typescript
// Create AuthContext to provide user state globally
// Store: user, token, loading, login(), signup(), logout()
// Use throughout app to check authentication status
```

### Protected Page Component

```typescript
// Redirect to /login if not authenticated
// Show loading spinner while checking auth
// Render children if authenticated
```

## Validation Rules

### Name
- Required
- 2-100 characters
- Letters, spaces, hyphens allowed

### Email
- Required
- Valid email format (contains @)
- Unique (not already registered)
- Case-insensitive comparison

### Password
- Required
- Minimum 8 characters
- Maximum 100 characters
- (Future: Require uppercase, lowercase, number, special char)

## Security Considerations

### Password Security
- Never log passwords
- Never return passwords in API responses
- Hash before storing
- Use bcrypt with appropriate salt rounds

### JWT Security
- Sign tokens with strong secret
- Set reasonable expiration (7 days)
- Verify signature on every request
- Include only necessary data in payload

### HTTPS
- Use HTTPS in production
- Prevent man-in-the-middle attacks
- Tokens transmitted securely

### CORS
- Configure CORS to allow only frontend domain
- Reject requests from unauthorized origins

### Input Sanitization
- Validate all inputs on backend
- Prevent SQL injection (use ORM)
- Prevent XSS (sanitize HTML)

## Error Handling

### Frontend Errors
- Invalid email: "Please enter a valid email address"
- Password too short: "Password must be at least 8 characters"
- Email exists: "Email already registered. Try logging in."
- Invalid credentials: "Invalid email or password"
- Network error: "Connection failed. Please try again."

### Backend Errors
- 400 Bad Request: Invalid input format
- 401 Unauthorized: Invalid credentials
- 409 Conflict: Email already exists
- 500 Internal Server Error: Database or server error

## Testing Scenarios

### Signup Tests
1. Valid signup → Success, token received, redirected
2. Duplicate email → Error: "Email already registered"
3. Invalid email → Error: "Invalid email"
4. Short password → Error: "Password too short"
5. Empty fields → Error: "All fields required"

### Login Tests
1. Valid credentials → Success, token received, redirected
2. Invalid email → Error: "Invalid credentials"
3. Invalid password → Error: "Invalid credentials"
4. Empty fields → Error: "All fields required"

### Protected Routes Tests
1. Access dashboard without token → Redirect to /login
2. Access dashboard with valid token → Show dashboard
3. Access dashboard with expired token → Redirect to /login
4. API call without token → 401 Unauthorized
5. API call with invalid token → 401 Unauthorized

### Logout Tests
1. Logout → Token removed, redirected to login
2. Access dashboard after logout → Redirect to login
3. API call after logout → 401 Unauthorized

## Performance Requirements

- Login/Signup complete in < 2 seconds
- Token verification in < 100ms
- No unnecessary re-renders on authentication check

## Dependencies

- Better Auth library
- bcrypt (backend)
- JWT library (backend)
- Database with users table

## Future Enhancements (Not Phase II)

- Email verification
- Password reset
- OAuth (Google, GitHub login)
- Two-factor authentication (2FA)
- Session management (logout all devices)
- Password strength meter

## Acceptance Testing

**Definition of Done**:
- [ ] Signup page functional
- [ ] Login page functional
- [ ] Logout button works
- [ ] Protected routes enforce authentication
- [ ] JWT tokens generated and verified
- [ ] Passwords securely hashed
- [ ] Error handling implemented
- [ ] User can stay logged in across refreshes
- [ ] Demo video shows signup, login, logout
