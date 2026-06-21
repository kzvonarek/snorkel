import service from './index'

export const createProject = (data) => service.post('/api/projects', data)
export const listProjects = (limit = 50) => service.get('/api/projects', { params: { limit } })
export const getProject = (projectId) => service.get(`/api/projects/${projectId}`)
