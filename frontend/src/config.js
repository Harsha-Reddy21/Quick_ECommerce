// API Configuration
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const config = {
  API_URL,
  AUTH_TOKEN_KEY: 'auth_token',
  USER_INFO_KEY: 'user_info',
};

export default config; 