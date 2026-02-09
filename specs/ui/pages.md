# UI Pages Specification

**Author**: Asif Ali AstolixGen
**Phase**: Phase II
**Framework**: Next.js 15 (App Router)

## Overview

The application has three main pages: Login, Signup, and Dashboard. Navigation is controlled by authentication status.

## Page Structure

```
app/
├── layout.tsx          # Root layout (global styles, providers)
├── login/
│   └── page.tsx        # Login page
├── signup/
│   └── page.tsx        # Signup page
└── page.tsx            # Dashboard (protected)
```

## Page: Login (/login)

### Purpose
Allow existing users to authenticate and access their tasks.

### Layout
- Centered card on full-height page
- Dark gradient background
- Logo/branding at top
- Form in the middle
- Link to signup at bottom

### Components
- Email input field
- Password input field
- Login button
- "Sign up" link
- Error message display

### User Flow
1. User enters email and password
2. User clicks "Login" button
3. If valid: Redirect to dashboard
4. If invalid: Show error message

### Redirect Rules
- If already logged in → Redirect to `/`
- After successful login → Redirect to `/`

### See Also
- `@specs/features/authentication.md`
- `@specs/ui/components.md`

## Page: Signup (/signup)

### Purpose
Allow new users to create an account.

### Layout
- Centered card on full-height page
- Dark gradient background
- Logo/branding at top
- Form in the middle
- Link to login at bottom

### Components
- Name input field
- Email input field
- Password input field
- Confirm password input field
- Signup button
- "Login" link
- Error message display

### User Flow
1. User enters name, email, password
2. User confirms password
3. User clicks "Sign up" button
4. If valid: Account created, redirect to dashboard
5. If invalid: Show error message

### Validation
- All fields required
- Email must be valid format
- Password min 8 characters
- Passwords must match

### Redirect Rules
- If already logged in → Redirect to `/`
- After successful signup → Redirect to `/`

### See Also
- `@specs/features/authentication.md`
- `@specs/ui/components.md`

## Page: Dashboard (/)

### Purpose
Main application page where users manage their tasks.

### Layout
```
┌─────────────────────────────────────────┐
│  Header (User info, Logout button)      │
├─────────────────────────────────────────┤
│  Task Statistics (Total, Completed)     │
├─────────────────────────────────────────┤
│  Add Task Form                          │
├─────────────────────────────────────────┤
│  Task List                              │
│  ┌──────────────────────────────────┐  │
│  │  Task Item 1                      │  │
│  ├──────────────────────────────────┤  │
│  │  Task Item 2                      │  │
│  ├──────────────────────────────────┤  │
│  │  Task Item 3                      │  │
│  └──────────────────────────────────┘  │
├─────────────────────────────────────────┤
│  Footer                                 │
└─────────────────────────────────────────┘
```

### Components
- Header with user name and logout button
- Task statistics display
- Task creation form
- Task list (array of Task Items)
- Empty state (if no tasks)
- Footer

### User Flow
1. Page loads, fetches tasks from API
2. Display tasks in list
3. User can:
   - Add new task
   - Edit existing task
   - Mark task complete/incomplete
   - Delete task

### Redirect Rules
- If not logged in → Redirect to `/login`

### See Also
- `@specs/features/task-crud.md`
- `@specs/ui/components.md`

## Navigation

### Public Routes
- `/login` - Accessible when logged out
- `/signup` - Accessible when logged out

### Protected Routes
- `/` - Requires authentication

### Automatic Redirects
- Logged out user visits `/` → Redirect to `/login`
- Logged in user visits `/login` or `/signup` → Redirect to `/`

## Common Elements

### Layout.tsx
- Global styles (Tailwind)
- Auth Provider (Better Auth context)
- Meta tags (title, description)
- Font configuration

### Loading States
- Show spinner while checking authentication
- Show skeleton while loading tasks
- Show disabled button during form submission

### Error States
- Network error: "Connection failed. Please try again."
- Auth error: Redirect to login
- Server error: "Something went wrong. Please try again."

## Responsive Design

### Mobile (< 768px)
- Single column layout
- Stack form fields vertically
- Full-width buttons
- Simplified header

### Tablet (768px - 1024px)
- Maintain single column
- Increase padding
- Larger touch targets

### Desktop (> 1024px)
- Max width container (7xl)
- Larger font sizes
- Side-by-side layouts where appropriate

## Accessibility

- Semantic HTML elements
- Proper form labels
- Keyboard navigation support
- ARIA labels where needed
- Focus states on interactive elements
- Color contrast ratios (WCAG AA)

## Performance

- Server components by default
- Client components only when needed
- Lazy load images
- Prefetch critical routes
- Optimize fonts (Next.js font optimization)

## Theme

### Colors
- Background: Dark gradient (gray-950 to black)
- Primary: Blue-400 to Purple-500 gradient
- Text: White (primary), Gray-400 (secondary)
- Success: Emerald-400
- Error: Red-400
- Borders: Gray-800

### Typography
- Font: System font stack
- Headings: Bold, larger sizes
- Body: Regular weight

### Spacing
- Consistent padding (4, 6, 8, 12, 16, 24)
- Card padding: 6 or 8
- Section gaps: 8 or 12

## Future Enhancements (Not Phase II)

- Settings page
- Profile page
- Task details page (separate route)
- Categories/tags page
- Search page
- Statistics/analytics page

