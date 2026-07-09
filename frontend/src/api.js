import axios from 'axios';

// In production (Vercel), VITE_API_URL = https://resume-intelligence-system.onrender.com
// In development (local), it's empty so axios uses the Vite proxy (/api → localhost:8080)
const baseURL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL,
});

export default api;
