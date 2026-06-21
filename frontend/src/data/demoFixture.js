export const fixtureActions = [
  { round_num: 1, timestamp: 'Demo', platform: 'twitter', agent_id: 0, agent_name: 'Power User 1', action_type: 'CREATE_POST', action_args: { content: 'The automated categories are useful, but I need custom export mappings.' }, success: true },
  { round_num: 1, timestamp: 'Demo', platform: 'twitter', agent_id: 2, agent_name: 'Casual Explorer 1', action_type: 'LIKE_POST', action_args: {}, success: true },
  { round_num: 2, timestamp: 'Demo', platform: 'twitter', agent_id: 4, agent_name: 'Finance Professional 1', action_type: 'CREATE_POST', action_args: { content: 'Audit history is the missing requirement for a finance rollout.' }, success: true },
  { round_num: 3, timestamp: 'Demo', platform: 'twitter', agent_id: 1, agent_name: 'Power User 2', action_type: 'CREATE_COMMENT', action_args: { content: 'The dashboard is clear and the setup feels faster than our current tool.' }, success: true },
  { round_num: 4, timestamp: 'Demo', platform: 'twitter', agent_id: 3, agent_name: 'Casual Explorer 2', action_type: 'LIKE_POST', action_args: {}, success: true },
  { round_num: 5, timestamp: 'Demo', platform: 'twitter', agent_id: 5, agent_name: 'Finance Professional 2', action_type: 'CREATE_COMMENT', action_args: { content: 'I would pilot this after compliance export and audit history ship.' }, success: true },
]

export const fixtureAgentStats = [
  { agent_id: 0, agent_name: 'Power User 1', total_actions: 8, action_types: { CREATE_POST: 3, LIKE_POST: 5 } },
  { agent_id: 1, agent_name: 'Power User 2', total_actions: 7, action_types: { CREATE_COMMENT: 2, LIKE_POST: 5 } },
  { agent_id: 2, agent_name: 'Casual Explorer 1', total_actions: 5, action_types: { CREATE_POST: 1, LIKE_POST: 4 } },
  { agent_id: 3, agent_name: 'Casual Explorer 2', total_actions: 4, action_types: { CREATE_COMMENT: 1, LIKE_POST: 3 } },
  { agent_id: 4, agent_name: 'Finance Professional 1', total_actions: 6, action_types: { CREATE_POST: 2, LIKE_POST: 4 } },
  { agent_id: 5, agent_name: 'Finance Professional 2', total_actions: 5, action_types: { CREATE_COMMENT: 2, LIKE_POST: 3 } },
]

export const fixtureReport = {
  report_id: 'report_demo_fixture', simulation_id: 'sim_demo_fixture', status: 'completed',
  created_at: new Date().toISOString(), completed_at: new Date().toISOString(),
  markdown_content: `# FinTrack v2 PMF Simulation\n\n## Executive summary\nThe simulated audience responded positively to the simplified budgeting workflow. This is fixture data for presentation continuity, not evidence from a live OASIS run.\n\n## Observed signals\n- Power users valued automation but requested custom export mappings.\n- Casual explorers reacted positively to the simpler dashboard.\n- Finance professionals consistently required audit history and compliance exports.\n\n## Recommendation\nPilot with power users while validating the two finance workflow requirements with real customers.`,
}

export function createFixtureSnapshot(reason = 'Live services were unavailable.') {
  return {
    mode: 'fixture', fixtureReason: reason, projectId: 'proj_demo_fixture', simulationId: 'sim_demo_fixture',
    reportId: fixtureReport.report_id, phase: 'completed', isRunning: false, currentRound: 5, totalRounds: 5,
    progress: 100, actions: fixtureActions, timeline: [], agentStats: fixtureAgentStats,
    posts: fixtureActions.filter(item => item.action_type === 'CREATE_POST'), report: fixtureReport,
    error: '', updatedAt: new Date().toISOString(),
  }
}
