/**
 * Authentication utilities
 */

export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

export interface AuthCredentials {
  email: string;
  password: string;
  name?: string;
}

// Simulated user database (replace with real backend)
const USERS_KEY = 'taskflow_users';
const CURRENT_USER_KEY = 'taskflow_current_user';

export class AuthService {
  // Get all users from localStorage
  private static getUsers(): User[] {
    if (typeof window === 'undefined') return [];
    const users = localStorage.getItem(USERS_KEY);
    return users ? JSON.parse(users) : [];
  }

  // Save users to localStorage
  private static saveUsers(users: User[]): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
  }

  // Hash password (simple version - use bcrypt in production)
  private static hashPassword(password: string): string {
    // Simple hash for demo - use proper hashing in production
    return btoa(password + 'salt_key_for_taskflow');
  }

  // Verify password
  private static verifyPassword(password: string, hash: string): boolean {
    return this.hashPassword(password) === hash;
  }

  // Sign up new user
  static async signup(credentials: AuthCredentials): Promise<{ success: boolean; user?: User; error?: string }> {
    try {
      const { email, password, name } = credentials;

      // Validate input
      if (!email || !password || !name) {
        return { success: false, error: 'All fields are required' };
      }

      if (password.length < 6) {
        return { success: false, error: 'Password must be at least 6 characters' };
      }

      if (!email.includes('@')) {
        return { success: false, error: 'Invalid email address' };
      }

      const users = this.getUsers();

      // Check if user already exists
      if (users.find(u => u.email.toLowerCase() === email.toLowerCase())) {
        return { success: false, error: 'Email already registered' };
      }

      // Create new user
      const newUser: User = {
        id: Date.now().toString(),
        email: email.toLowerCase(),
        name,
        createdAt: new Date().toISOString(),
      };

      // Store user with hashed password
      const userWithPassword = {
        ...newUser,
        passwordHash: this.hashPassword(password),
      };

      users.push(userWithPassword);
      this.saveUsers(users);

      // Set current user (without password)
      this.setCurrentUser(newUser);

      return { success: true, user: newUser };
    } catch (error) {
      return { success: false, error: 'Signup failed. Please try again.' };
    }
  }

  // Login user
  static async login(credentials: AuthCredentials): Promise<{ success: boolean; user?: User; error?: string }> {
    try {
      const { email, password } = credentials;

      if (!email || !password) {
        return { success: false, error: 'Email and password are required' };
      }

      const users = this.getUsers();
      const userWithPassword = users.find(u => u.email.toLowerCase() === email.toLowerCase()) as any;

      if (!userWithPassword) {
        return { success: false, error: 'Invalid email or password' };
      }

      // Verify password
      if (!this.verifyPassword(password, userWithPassword.passwordHash)) {
        return { success: false, error: 'Invalid email or password' };
      }

      // Create user object without password
      const user: User = {
        id: userWithPassword.id,
        email: userWithPassword.email,
        name: userWithPassword.name,
        createdAt: userWithPassword.createdAt,
      };

      this.setCurrentUser(user);

      return { success: true, user };
    } catch (error) {
      return { success: false, error: 'Login failed. Please try again.' };
    }
  }

  // Logout user
  static logout(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(CURRENT_USER_KEY);
  }

  // Get current user
  static getCurrentUser(): User | null {
    if (typeof window === 'undefined') return null;
    const user = localStorage.getItem(CURRENT_USER_KEY);
    return user ? JSON.parse(user) : null;
  }

  // Set current user
  static setCurrentUser(user: User): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user));
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    return this.getCurrentUser() !== null;
  }
}
