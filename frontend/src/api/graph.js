import service, { requestWithRetry } from './index'

export const buildGraph = (data) => {
  return requestWithRetry(() => service.post('/api/graph/build', data), 3, 1000)
}

export const getProject = (projectId) => {
  return service.get(`/api/graph/project/${projectId}`)
}