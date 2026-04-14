import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Interceptor to add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default {
    // Auth endpoints
    login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        return api.post('/auth/token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
    },
    register(username, email, password) {
        return api.post('/auth/register', { username, email, password });
    },

    // Notes endpoints
    getNotes(params) {
        return api.get('/notes/', { params });
    },
    getNote(id) {
        return api.get(`/notes/${id}`);
    },
    createNote(note) {
        return api.post('/notes/', note);
    },
    updateNote(id, note) {
        return api.put(`/notes/${id}`, note);
    },
    deleteNote(id) {
        return api.delete(`/notes/${id}`);
    }
}
