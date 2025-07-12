// API Configuration
const API_URL = process.env.REACT_APP_API_URL || 'https://quick-ecommerce-api.onrender.com';

// Remove any trailing slashes from the API URL
const normalizedApiUrl = API_URL.endsWith('/') ? API_URL.slice(0, -1) : API_URL;

const config = {
  API_URL: normalizedApiUrl,
  AUTH_TOKEN_KEY: 'auth_token',
  USER_INFO_KEY: 'user_info',
};

export default config; 