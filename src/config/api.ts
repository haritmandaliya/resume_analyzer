// API Configuration
// Centralized API base URL configuration

const getApiBaseUrl = (): string => {
  // In development, use the backend URL directly
  // In production, this could be an environment variable
  if (import.meta.env.DEV) {
    // Development mode - use backend URL
    return 'http://localhost:8000';
  }
  // Production mode - use relative URLs or environment variable
  return import.meta.env.VITE_API_URL || 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();

// Helper function to create full API URL
export const getApiUrl = (endpoint: string): string => {
  // Remove leading slash if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  // Ensure endpoint starts with /api
  const apiEndpoint = cleanEndpoint.startsWith('api/') ? cleanEndpoint : `api/${cleanEndpoint}`;
  return `${API_BASE_URL}/${apiEndpoint}`;
};

// Common API endpoints
export const API_ENDPOINTS = {
  RESUMES: getApiUrl('resumes'),
  RESUME: (filename: string) => getApiUrl(`resume/${encodeURIComponent(filename)}`),
  RESUME_ANALYSIS: (filename: string) => getApiUrl(`resume-analysis/${encodeURIComponent(filename)}`),
  JD_HISTORY: getApiUrl('jd-history'),
  UPLOAD: getApiUrl('upload'),
  UPLOAD_RESUME: getApiUrl('upload-resume/'),
  PROCESS_INPUT: getApiUrl('process_input/'),
  BATCH_ANALYZE: getApiUrl('batch-analyze/'),
  SMART_CHAT: getApiUrl('smart-chat'),
  CHAT: getApiUrl('chat'),
  IMPROVE_JD: getApiUrl('improve-jd'),
} as const;

