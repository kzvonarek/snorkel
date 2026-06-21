import service, { requestWithRetry } from './index'

export const listReports = (simulationId, limit = 50) => {
  const params = { limit }
  if (simulationId) {
    params.simulation_id = simulationId
  }
  return service.get('/api/report/list', { params })
}

export const getReport = (reportId) => {
  return service.get(`/api/report/${reportId}`)
}

export const generateReport = (data) => {
  return requestWithRetry(() => service.post('/api/report/generate', data), 3, 1000)
}

export const chatWithReport = (data) => {
  return requestWithRetry(() => service.post('/api/report/chat', data), 3, 1000)
}

export const getReportBySimulation = (simulationId) => service.get(`/api/report/by-simulation/${simulationId}`)
export const getReportStatus = (data) => service.post('/api/report/generate/status', data)

export const reportDownloadUrl = (reportId) => {
  const base = import.meta.env.VITE_API_BASE_URL || ''
  return `${base}/api/report/${reportId}/download`
}
