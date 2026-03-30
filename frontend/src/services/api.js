import { getDeviceId } from '../utils/device';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const TIMEOUT = 30000;

/**
 * Helper to build query string from params object
 */
const buildQueryString = (params) => {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, value);
    }
  });
  return searchParams.toString();
};

/**
 * Fetch with timeout
 */
const fetchWithTimeout = (url, options = {}) => {
  return Promise.race([
    fetch(url, options),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), TIMEOUT)
    ),
  ]);
};

/**
 * Handle response and parse JSON
 */
const handleResponse = async (response) => {
  const data = await response.json();
  console.log('📌 API Response Status:', response.status);
  console.log('📌 API Response Data:', data);
  
  if (!response.ok) {
    const error = new Error(data.message || 'API Error');
    error.response = { status: response.status, data };
    console.error('❌ API Error:', error);
    throw error;
  }
  return { status: response.status, data };
};

const deviceId = () => getDeviceId();

/**
 * GET request
 */
const get = (endpoint, options = {}) => {
  const params = { device_id: deviceId(), ...options.params };
  const queryString = buildQueryString(params);
  const url = `${BASE_URL}${endpoint}${queryString ? '?' + queryString : ''}`;
  
  return fetchWithTimeout(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json', ...options.headers },
  }).then(handleResponse);
};

/**
 * POST request
 */
const post = (endpoint, body = {}, options = {}) => {
  const data = { ...body, device_id: deviceId() };
  const url = `${BASE_URL}${endpoint}`;
  
  console.log('📤 POST Request to:', url);
  console.log('📤 POST Body:', JSON.stringify(data));
  
  return fetchWithTimeout(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...options.headers },
    body: JSON.stringify(data),
  })
    .catch((err) => {
      console.error('❌ Network Error:', err);
      throw err;
    })
    .then(handleResponse);
};

/**
 * DELETE request
 */
const deleteReq = (endpoint, options = {}) => {
  const params = { device_id: deviceId(), ...options.params };
  const queryString = buildQueryString(params);
  const url = `${BASE_URL}${endpoint}${queryString ? '?' + queryString : ''}`;
  
  return fetchWithTimeout(url, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json', ...options.headers },
  }).then(handleResponse);
};

// Dashboard
export const getDashboard = () => get('/dashboard/');

// Income
export const getIncome = (params = {}) => get('/income/', { params });
export const addIncome = (data) => post('/income/add/', data);
export const deleteIncome = (id) => deleteReq(`/income/${id}/`);

// Expense
export const getExpense = (params = {}) => get('/expense/', { params });
export const addExpense = (data) => post('/expense/add/', data);
export const deleteExpense = (id) => deleteReq(`/expense/${id}/`);

// Sales
export const getSales = (params = {}) => get('/sales/', { params });
export const addSale = (data) => post('/sales/add/', data);
export const deleteSale = (id) => deleteReq(`/sales/${id}/`);

// Profit
export const getProfit = (period = 'monthly') => get('/profit/', { params: { period } });

// Payment
export const getPayments = () => get('/payment/');
export const addPayment = (data) => post('/payment/add/', data);

// Market Prices
export const getMarketPrices = (commodity = '') => get('/market-prices/', { params: { commodity } });

// Schemes
export const getSchemes = (category = '') => get('/schemes/', { params: { category } });

// Mentors
export const getMentors = () => get('/mentors/');
export const getMentorChats = (mentorId) => get('/mentor-chat/', { params: { mentor_id: mentorId } });
export const sendMentorMessage = (data) => post('/mentor-chat/', data);

// User Profile
export const getUserProfile = () => get('/user/');
export const updateUserProfile = (data) => post('/user/', data);

// Voice / ML
export const predictIntent = (text, language) => post('/predict-intent/', { text, language });

// Default API utilities
const api = { get, post, deleteReq };
export default api;
