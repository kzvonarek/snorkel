import axios from 'axios'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 300000,
  headers: {
    'Content-Type': 'application/json'
  }
})

service.interceptors.response.use(
  response => {
    const data = response.data
    if (data && data.success === false) {
      return Promise.reject(new Error(data.error || data.message || 'Request failed'))
    }
    return data
  },
  error => Promise.reject(error)
)

export const requestWithRetry = async (requestFn, maxRetries = 3, delay = 1000) => {
  for (let attempt = 0; attempt < maxRetries; attempt += 1) {
    try {
      return await requestFn()
    } catch (error) {
      if (attempt === maxRetries - 1) throw error
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, attempt)))
    }
  }
}

export default service