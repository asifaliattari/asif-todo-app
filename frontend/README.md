# TaskFlow Frontend

Modern Next.js 15 frontend for TaskFlow todo application.

**Created by Asif Ali AstolixGen** for GIAIC Hackathon 2026

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Date Formatting**: date-fns
- **Authentication**: Custom JWT with localStorage

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with AuthProvider
│   ├── page.tsx            # Dashboard (protected)
│   ├── login/page.tsx      # Login page
│   └── signup/page.tsx     # Signup page
├── components/
│   ├── AuthGuard.tsx       # Route protection
│   ├── TaskForm.tsx        # Create task form
│   ├── TaskList.tsx        # Task list with sections
│   └── TaskItem.tsx        # Individual task item
├── contexts/
│   └── AuthContext.tsx     # Auth state management
├── lib/
│   └── api.ts             # API client
└── app/globals.css        # Global styles
```

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=TaskFlow
NEXT_PUBLIC_AUTHOR=Asif Ali AstolixGen
NEXT_PUBLIC_HACKATHON=GIAIC Hackathon 2026
```

### 3. Start Backend

Make sure the FastAPI backend is running on port 8000:

```bash
cd ../backend
uv run uvicorn main:app --reload --port 8000
```

### 4. Run Development Server

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

## Features

### Authentication
- ✅ User signup with validation
- ✅ User login with JWT tokens
- ✅ Protected routes with AuthGuard
- ✅ Automatic token storage in localStorage
- ✅ Logout functionality

### Task Management
- ✅ Create tasks with title and description
- ✅ View all user tasks (separated by status)
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task details inline
- ✅ Delete tasks with confirmation
- ✅ Real-time task counter
- ✅ Relative timestamps

### UI/UX
- ✅ Dark theme with purple accents
- ✅ Responsive design (mobile-friendly)
- ✅ Loading states
- ✅ Error handling with user feedback
- ✅ Smooth transitions and hover effects
- ✅ Accessible form inputs

## API Integration

The frontend communicates with the FastAPI backend through the API client (`lib/api.ts`).

### Authentication Flow

1. User signs up or logs in
2. Backend returns JWT token + user data
3. Token stored in localStorage
4. Token sent with all subsequent requests via `Authorization: Bearer {token}` header
5. AuthContext manages user state
6. AuthGuard protects dashboard route

### Task Operations

All task operations require authentication:

- **GET** `/api/tasks` - Fetch user tasks
- **POST** `/api/tasks` - Create new task
- **PUT** `/api/tasks/{id}` - Update task
- **PATCH** `/api/tasks/{id}/complete` - Toggle completion
- **DELETE** `/api/tasks/{id}` - Delete task

## Pages

### `/login` - Login Page
- Email and password form
- Error handling
- Link to signup
- Redirects to dashboard on success

### `/signup` - Signup Page
- Name, email, password form
- Password validation (min 6 chars)
- Error handling
- Link to login
- Redirects to dashboard on success

### `/` - Dashboard (Protected)
- Requires authentication
- Create new tasks
- View active and completed tasks
- Edit, toggle, delete tasks
- Logout button
- Refresh button

## Components

### `AuthContext`
Manages global authentication state:
- Current user
- Login/signup/logout methods
- Token persistence
- Loading state

### `AuthGuard`
Protects routes from unauthenticated access:
- Checks user state
- Redirects to `/login` if not authenticated
- Shows loading spinner during check

### `TaskForm`
Form to create new tasks:
- Title input (required)
- Description textarea (optional)
- Submit button with loading state

### `TaskList`
Displays all tasks grouped by status:
- Active tasks section
- Completed tasks section
- Empty state message

### `TaskItem`
Individual task with actions:
- Toggle completion checkbox
- Edit mode (inline editing)
- Delete with confirmation
- Relative timestamp
- Visual completion indicator

## Styling

The app uses a dark theme with:
- Background: Gradient from gray-900 to purple-900
- Primary color: Purple (600-700)
- Text: White/gray scale
- Borders: Gray-700
- Tailwind CSS utility classes

## Build & Deploy

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.

**Important**: Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL` - Your deployed backend URL

## Development Notes

### SSR Considerations
- `localStorage` access is wrapped in client-side checks
- All interactive components are marked with `'use client'`
- AuthContext only runs in browser environment

### Error Handling
- API errors are caught and displayed to users
- Network failures show error messages
- Invalid tokens redirect to login

### Type Safety
- Full TypeScript coverage
- Strict type checking enabled
- API response types defined

## Troubleshooting

### "localStorage is not defined"
- Make sure components using localStorage are client components (`'use client'`)
- Check that localStorage access is wrapped in `typeof window !== 'undefined'` checks

### CORS Errors
- Ensure backend CORS is configured to allow frontend origin
- Check `NEXT_PUBLIC_API_URL` matches backend URL

### Authentication Issues
- Verify token is stored in localStorage
- Check network tab for Authorization header
- Ensure backend SECRET_KEY matches

## License

Created for GIAIC Hackathon 2026 by Asif Ali AstolixGen
