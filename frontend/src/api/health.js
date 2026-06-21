import service from './index'

export function getBackendHealth() {
  return service.get('/health')
}