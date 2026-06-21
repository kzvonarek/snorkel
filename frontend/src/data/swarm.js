export const swarmDots = [
  // Power Users cluster
  { id: 'd1', cx: 18, cy: 22, cluster: 'Power Users',          sentiment: 'idle', agent: 'Agent #1' },
  { id: 'd2', cx: 22, cy: 28, cluster: 'Power Users',          sentiment: 'idle', agent: 'Agent #2' },
  { id: 'd3', cx: 15, cy: 32, cluster: 'Power Users',          sentiment: 'idle', agent: 'Agent #3' },
  { id: 'd4', cx: 26, cy: 18, cluster: 'Power Users',          sentiment: 'idle', agent: 'Agent #4' },
  { id: 'd5', cx: 20, cy: 38, cluster: 'Power Users',          sentiment: 'idle', agent: 'Agent #5' },
  // Casual Explorers cluster
  { id: 'd6', cx: 52, cy: 25, cluster: 'Casual Explorers',     sentiment: 'idle', agent: 'Agent #6' },
  { id: 'd7', cx: 56, cy: 32, cluster: 'Casual Explorers',     sentiment: 'idle', agent: 'Agent #7' },
  { id: 'd8', cx: 48, cy: 38, cluster: 'Casual Explorers',     sentiment: 'idle', agent: 'Agent #8' },
  { id: 'd9', cx: 60, cy: 20, cluster: 'Casual Explorers',     sentiment: 'idle', agent: 'Agent #9' },
  { id: 'd10', cx: 54, cy: 44, cluster: 'Casual Explorers',    sentiment: 'idle', agent: 'Agent #10' },
  // Finance Professionals cluster
  { id: 'd11', cx: 82, cy: 30, cluster: 'Finance Professionals', sentiment: 'idle', agent: 'Agent #11' },
  { id: 'd12', cx: 78, cy: 36, cluster: 'Finance Professionals', sentiment: 'idle', agent: 'Agent #12' },
  { id: 'd13', cx: 86, cy: 22, cluster: 'Finance Professionals', sentiment: 'idle', agent: 'Agent #13' },
  { id: 'd14', cx: 80, cy: 45, cluster: 'Finance Professionals', sentiment: 'idle', agent: 'Agent #14' },
]

export const sentimentSequence = [
  'pos', 'pos', 'neg', 'pos', 'neu', 'pos', 'pos', 'neg',
  'neu', 'pos', 'pos', 'neg', 'pos', 'neu', 'pos', 'pos',
]

export const feedScript = [
  { t: 500,  msg: 'Agent #1 (Power Users) exploring export settings panel…' },
  { t: 1200, msg: 'Agent #6 (Casual Explorers) landed on dashboard — low friction noted.' },
  { t: 2000, msg: 'Agent #11 (Finance Professionals) triggered audit log — path blocked.' },
  { t: 2800, msg: 'Agent #2 (Power Users) sent API request — latency spike flagged.' },
  { t: 3600, msg: 'Agent #7 (Casual Explorers) rated budgeting widget positively.' },
  { t: 4400, msg: 'Agent #12 (Finance Professionals) requested compliance export.' },
  { t: 5000, msg: 'Round 1 complete — 5 of 14 agents registered friction points.' },
  { t: 6000, msg: 'Round 2 starting. Agents re-entering with updated context…' },
  { t: 7200, msg: 'Agent #3 (Power Users) successfully mapped custom fields.' },
  { t: 8100, msg: 'Agent #8 (Casual Explorers) abandoned onboarding at step 3.' },
  { t: 9000, msg: 'Simulation complete. Aggregating results…' },
]

export const transcripts = {
  'd1': [
    { role: 'system', text: 'Agent #1 initialised as Power User persona.' },
    { role: 'agent',  text: 'Opening export settings. Looking for custom field mapping.' },
    { role: 'agent',  text: 'Found export dialog — field mapping is missing from this version.' },
    { role: 'system', text: 'Friction recorded: missing feature.' },
  ],
  'd6': [
    { role: 'system', text: 'Agent #6 initialised as Casual Explorer persona.' },
    { role: 'agent',  text: 'Dashboard loaded quickly. The summary view is clean.' },
    { role: 'agent',  text: 'Tried to set a budget goal — intuitive flow.' },
    { role: 'system', text: 'Positive signal: core flow satisfaction.' },
  ],
}
