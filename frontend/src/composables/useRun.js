import { reactive } from 'vue'
import { createProject } from '@/api/projects'
import { createSimulation, getActions, getAgentStats, getPosts, getPrepareStatus, getRunStatus, getTimeline, prepareSimulation, startSimulation } from '@/api/simulation'
import { chatWithReport, generateReport, getReport, getReportStatus } from '@/api/report'
import { createFixtureSnapshot, fixtureReport } from '@/data/demoFixture'
import { getDemoTopic, topicMarkdown } from '@/data/demoTopics'
import { expandPersonas, readStoredRun, RUN_STORAGE_KEY } from './runCore'

export { expandPersonas, RUN_STORAGE_KEY }
const terminalStatuses = new Set(['completed', 'stopped', 'failed'])
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms))
const unwrap = response => response?.data ?? response

function initialState() {
  return { mode: 'live', fixtureReason: '', projectId: '', simulationId: '', reportId: '', topicId: '', phase: 'idle', isRunning: false, currentRound: 0, totalRounds: 0, progress: 0, actions: [], timeline: [], agentStats: [], posts: [], report: null, error: '', updatedAt: '' }
}

function restore() {
  if (typeof sessionStorage === 'undefined') return initialState()
  return { ...initialState(), ...readStoredRun(sessionStorage) }
}

const state = reactive(restore())
function persist() {
  state.updatedAt = new Date().toISOString()
  if (typeof sessionStorage !== 'undefined') sessionStorage.setItem(RUN_STORAGE_KEY, JSON.stringify({ ...state }))
}
function assign(values) { Object.assign(state, values); persist() }

export function activateFixture(reason) { assign(createFixtureSnapshot(reason)); return state }
export function resetRun() { Object.assign(state, initialState()); persist() }

export function launchDemoTopic(topicId) {
  const topic = getDemoTopic(topicId)
  resetRun()
  assign({
    mode: 'demo', topicId: topic.id, projectId: `demo_${topic.id}`, simulationId: `sim_${topic.id}`,
    phase: 'running', isRunning: true, currentRound: 0, totalRounds: topic.rounds, progress: 0,
    agentStats: topic.agents.map(agent => ({ agent_id: agent.id, agent_name: agent.name, segment: agent.segment, total_actions: 0, action_types: {} })),
  })
  return state
}

export function appendDemoThought(topic, thoughtIndex) {
  const [agentId, content, sentiment] = topic.thoughts[thoughtIndex]
  const agent = topic.agents.find(item => item.id === agentId)
  const action = { round_num: Math.min(topic.rounds, Math.floor(thoughtIndex / 3) + 1), timestamp: new Date().toISOString(), platform: 'demo', agent_id: agentId, agent_name: agent.name, segment: agent.segment, sentiment, action_type: 'THINK', action_args: { content }, success: true }
  const actions = [...state.actions, action]
  const agentStats = state.agentStats.map(item => item.agent_id === agentId ? { ...item, total_actions: item.total_actions + 1, action_types: { ...item.action_types, THINK: (item.action_types.THINK || 0) + 1 } } : item)
  assign({ actions, agentStats, currentRound: action.round_num, progress: Math.round(actions.length / topic.thoughts.length * 100) })
}

export function completeDemoTopic(topic) {
  const report = { report_id: `report_${topic.id}`, simulation_id: `sim_${topic.id}`, status: 'completed', created_at: new Date().toISOString(), completed_at: new Date().toISOString(), markdown_content: topicMarkdown(topic), pdf_url: topic.pdfUrl }
  assign({ phase: 'completed', isRunning: false, currentRound: topic.rounds, progress: 100, report, reportId: report.report_id })
}

async function pollPreparation(taskId, simulationId) {
  for (let attempt = 0; attempt < 180; attempt += 1) {
    const status = unwrap(await getPrepareStatus({ task_id: taskId, simulation_id: simulationId }))
    assign({ phase: 'preparing', progress: Math.min(Number(status.progress || 0), 99) })
    if (status.status === 'ready' || status.status === 'completed') return
    if (status.status === 'failed') throw new Error(status.error || status.message || 'Simulation preparation failed')
    await wait(1000)
  }
  throw new Error('Simulation preparation timed out')
}

export async function launchRun({ product, environments = [], personas, rounds, agentsPerSegment }) {
  resetRun()
  const context = [product.name, ...environments.map(item => `${item.name}: ${item.notes}`)].join('\n')
  try {
    assign({ phase: 'creating', isRunning: true, totalRounds: rounds })
    const project = unwrap(await createProject({ name: product.name, simulation_requirement: `Evaluate product-market fit for ${product.name}. Identify strengths, friction, objections, and adoption requirements.`, document_text: context }))
    assign({ projectId: project.project_id })
    const simulation = unwrap(await createSimulation({ project_id: project.project_id, enable_twitter: true, enable_reddit: false }))
    assign({ simulationId: simulation.simulation_id, phase: 'preparing' })
    const preparation = unwrap(await prepareSimulation({ simulation_id: simulation.simulation_id, personas: expandPersonas(personas, agentsPerSegment), use_llm_for_profiles: false }))
    await pollPreparation(preparation.task_id, simulation.simulation_id)
    await startSimulation({ simulation_id: simulation.simulation_id, platform: 'twitter', max_rounds: rounds, enable_memory_indexing: false })
    assign({ phase: 'running', progress: 0 })
    return state
  } catch (error) {
    return activateFixture(error?.message || 'Live services were unavailable.')
  }
}

export async function refreshRun() {
  if (state.mode === 'fixture' || state.mode === 'demo' || !state.simulationId) return state
  const [statusRes, actionsRes, timelineRes, statsRes, postsRes] = await Promise.all([
    getRunStatus(state.simulationId), getActions(state.simulationId), getTimeline(state.simulationId), getAgentStats(state.simulationId), getPosts(state.simulationId),
  ])
  const status = unwrap(statusRes)
  const runnerStatus = status.runner_status || 'running'
  assign({
    phase: terminalStatuses.has(runnerStatus) ? runnerStatus : 'running', isRunning: !terminalStatuses.has(runnerStatus),
    currentRound: Number(status.current_round || 0), totalRounds: Number(status.total_rounds || state.totalRounds || 0),
    progress: terminalStatuses.has(runnerStatus) ? 100 : Math.round(Number(status.progress_percent || 0)),
    actions: unwrap(actionsRes)?.actions || [], timeline: unwrap(timelineRes)?.timeline || [],
    agentStats: unwrap(statsRes)?.stats || [], posts: unwrap(postsRes)?.posts || [],
  })
  return state
}

export async function buildReport() {
  if (state.mode === 'demo') return state.report
  if (state.mode === 'fixture') { assign({ report: fixtureReport, reportId: fixtureReport.report_id }); return fixtureReport }
  const generated = unwrap(await generateReport({ simulation_id: state.simulationId }))
  if (generated.status === 'completed') {
    const report = unwrap(await getReport(generated.report_id)); assign({ report, reportId: report.report_id }); return report
  }
  assign({ phase: 'reporting', reportId: generated.report_id })
  for (let attempt = 0; attempt < 240; attempt += 1) {
    const status = unwrap(await getReportStatus({ task_id: generated.task_id, simulation_id: state.simulationId }))
    if (status.status === 'completed') {
      const report = unwrap(await getReport(status.report_id || generated.report_id)); assign({ phase: 'completed', report, reportId: report.report_id }); return report
    }
    if (status.status === 'failed') throw new Error(status.error || status.message || 'Report generation failed')
    await wait(1000)
  }
  throw new Error('Report generation timed out')
}

export async function askReport(message, history = []) {
  if (state.mode === 'demo') {
    const topic = getDemoTopic(state.topicId)
    return { response: `${topic.name}: ${topic.recommendation} The strongest objections were ${topic.objections.join('; ')}.`, sources: ['Curated demo simulation'] }
  }
  if (state.mode === 'fixture') return { response: 'This answer comes from demo fixture data. Power users prioritized export flexibility, while finance professionals required audit history and compliance exports.', sources: ['Demo fixture'] }
  return unwrap(await chatWithReport({ simulation_id: state.simulationId, message, chat_history: history }))
}

export default state
