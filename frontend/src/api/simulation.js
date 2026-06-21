import service, { requestWithRetry } from './index'

export const listSimulations = (projectId) => {
  const params = projectId ? { project_id: projectId } : {}
  return service.get('/api/simulation/list', { params })
}

export const getSimulation = (simulationId) => {
  return service.get(`/api/simulation/${simulationId}`)
}

export const createSimulation = (data) => service.post('/api/simulation/create', data)
export const prepareSimulation = (data) => service.post('/api/simulation/prepare', data)
export const getPrepareStatus = (data) => service.post('/api/simulation/prepare/status', data)

export const startSimulation = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/start', data), 3, 1000)
}

export const interviewAgents = (data) => {
  return requestWithRetry(() => service.post('/api/simulation/interview/batch', data), 3, 1000)
}

export const getRunStatus = (simulationId) => service.get(`/api/simulation/${simulationId}/run-status`)
export const getRunDetail = (simulationId) => service.get(`/api/simulation/${simulationId}/run-status/detail`, { params: { platform: 'twitter' } })
export const getActions = (simulationId, limit = 200) => service.get(`/api/simulation/${simulationId}/actions`, { params: { platform: 'twitter', limit } })
export const getTimeline = (simulationId) => service.get(`/api/simulation/${simulationId}/timeline`)
export const getAgentStats = (simulationId) => service.get(`/api/simulation/${simulationId}/agent-stats`)
export const getPosts = (simulationId, limit = 100) => service.get(`/api/simulation/${simulationId}/posts`, { params: { platform: 'twitter', limit } })
