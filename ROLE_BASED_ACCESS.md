# Role-Based Access Control & Admin Authentication

## Overview
The platform now supports role-based access control with two distinct user types:
- **Users**: Automatic access to feedback submission and personal settings (no login required)
- **Admins**: Secure login required to access all dashboards and features

## How It Works

### 1. User Access (No Login)
Regular users automatically have access to:
- **User View**: Feedback form, AI chat support
- **Settings**: Profile, theme, language, AI personality preferences
- No login modal - they go directly to the user view
- No logout needed (they're always in user mode)

### 2. Admin Login
Admins must authenticate to access dashboards:
- Clicking "Admin Dashboard" or "Agent Dashboard" triggers the admin login modal
- Credentials are validated against the backend (or demo credentials)
- Session is stored in `localStorage` with a token
- Admin username is displayed in the logout button

### 3. Navigation Visibility
Based on the role:
- **Users** see navigation buttons for:
  - User View
  - Settings
  
- **Admins** see navigation buttons for:
  - User View
  - Admin Dashboard
  - Agent Dashboard
  - Settings

### 4. Admin Login Modal
When an admin tries to access admin features without being logged in:
- Username and password fields are presented
- Demo credentials are provided for testing
- Invalid credentials show an error message
- Successful login stores session data and grants access

### 5. Logout
- **User Logout**: Clears user state and refreshes to user view
- **Admin Logout**: Clears admin token and returns to login modal

## Code Changes

### State Management
Added authentication properties to the `state` object:
```javascript
userRole: null,        // 'user' or 'admin'
isAuthenticated: false // Authentication status
```

### Key Functions

#### `checkAuthentication()`
- Runs on page load
- Checks for admin login token in localStorage
- If found, initializes as admin
- Otherwise, initializes as regular user

#### `showAdminLoginModal()`
- Creates and displays the admin login form
- Includes demo credentials for testing
- Shows error messages for invalid attempts

#### `handleAdminLogin(e)`
- Validates username and password
- Generates a session token
- Stores credentials in localStorage
- Grants access to admin dashboards

#### `validateAdminCredentials(username, password)`
- Currently uses demo credentials (admin/admin123, manager/manager456)
- Should be replaced with API call to backend in production
- Returns true/false based on validation

#### `generateAdminToken(username)`
- Creates a session token from username and timestamp
- Used to maintain admin session (replace with JWT in production)

#### `initializeViewsBasedOnRole()` (Modified)
- For users: Shows user view and settings
- For admins: Checks login status before granting access
- Shows login modal if admin token is missing
- Displays appropriate buttons based on role

#### `addLogoutButton()` (Modified)
- Shows admin username in logout button if logged in
- Different behavior for user vs admin logout

#### `logout()` (Modified)
- Clears admin tokens for admin logout
- Refreshes user state for user logout
- Returns to appropriate state (login modal or user view)

#### `canAccessView(view)` (Existing)
- Returns true if user has permission to access the view
- Admins have access to all views
- Users only access "user" and "settings"

## Testing the Feature

### Test as Regular User:
1. Visit the platform
2. You're automatically taken to the User View (no login needed)
3. Notice only "User View" and "Settings" buttons are visible
4. Click "Settings" to change profile, theme, language, or AI personality
5. Admin Dashboard and Agent Dashboard buttons are hidden
6. Click "Logout (User)" if you want to reset user state

### Test as Admin:
1. Visit the platform (or logout as user)
2. Click the "Admin Dashboard" button
3. Admin login modal appears
4. Enter credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
   - OR
   - **Username**: `manager`
   - **Password**: `manager456`
5. Click "Login as Admin"
6. You now have access to all views and dashboards
7. Notice the logout button shows "Logout (Admin (admin))"
8. Click each dashboard to see the full functionality
9. Click "Logout (Admin (admin))" to logout and return to login modal

### Test Invalid Login:
1. Click "Admin Dashboard"
2. Try entering wrong credentials
3. Error message appears: "Invalid username or password"
4. Try again with correct credentials

## Browser Storage

### User Storage:
- `userRole`: Set to "user" for regular users

### Admin Storage:
- `adminToken`: Session token generated on login
- `adminUsername`: Username of logged-in admin

To reset:
1. Open DevTools (F12)
2. Go to Application/Storage > localStorage
3. Delete entries as needed
4. Refresh page

## Security Considerations

### Current Implementation (Demo/Development):
- **Frontend-only** authentication using demo credentials
- Simple Base64 token generation
- No password hashing
- Credentials stored in browser localStorage

### Production Recommendations:
1. **Backend Authentication**:
   - Implement proper login endpoint
   - Use bcrypt or similar for password hashing
   - Validate credentials server-side

2. **Token Management**:
   - Use JWT tokens instead of simple Base64
   - Set token expiration times (15-30 minutes)
   - Implement token refresh mechanism
   - Store tokens securely (HttpOnly cookies preferred)

3. **Session Management**:
   - Use server-side sessions
   - Implement logout on server (token blacklisting)
   - Track login history and admin actions

4. **Data Security**:
   - Encrypt sensitive data
   - Implement HTTPS only
   - Use CORS properly
   - Validate all inputs server-side

5. **Audit Logging**:
   - Log all admin actions
   - Track login/logout events
   - Monitor unauthorized access attempts
   - Store logs securely

## Future Enhancements

### Phase 1 (Immediate):
- [ ] Add password reset functionality
- [ ] Implement "Remember me" option
- [ ] Add admin action logging to UI
- [ ] Create admin audit report view

### Phase 2 (Short-term):
- [ ] Backend API integration
- [ ] JWT token implementation
- [ ] Email verification for admins
- [ ] Two-factor authentication (2FA)

### Phase 3 (Long-term):
- [ ] Role-based data filtering (admins see role-filtered feedback)
- [ ] Multiple admin levels (super-admin, manager, agent)
- [ ] Permission matrix system
- [ ] Granular access control
- [ ] OAuth2/SSO integration
