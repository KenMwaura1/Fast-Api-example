import { defineStore } from 'pinia';
import Api from '../Api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;
      try {
        const response = await Api.login(username, password);
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        // For simplicity, we'll just set username as user object for now
        // In a real app, you'd fetch user profile
        this.user = { username };
        localStorage.setItem('user', JSON.stringify(this.user));
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Login failed';
        return false;
      } finally {
        this.loading = false;
      }
    },
    async register(username, email, password) {
      this.loading = true;
      this.error = null;
      try {
        await Api.register(username, email, password);
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Registration failed';
        return false;
      } finally {
        this.loading = false;
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },
});
