export const stats = {
  pmfScore:       74,
  recommendPct:   68,
  objectionCount: 12,
  adoptionRate:   41,
}

export const sentimentBySegment = [
  { label: 'Power Users',           pct: 82, sentiment: 'pos' },
  { label: 'Casual Explorers',       pct: 61, sentiment: 'pos' },
  { label: 'Finance Professionals',  pct: 47, sentiment: 'neu' },
]

export const adoptionHeatmap = {
  cols: ['Free', 'Pro', 'Team', 'Enterprise'],
  rows: [
    { label: 'Power Users',          cells: ['Low', 'High', 'High', 'Med'] },
    { label: 'Casual Explorers',      cells: ['Med', 'Med',  'Low',  '—']   },
    { label: 'Finance Pros',          cells: ['—',   'Low',  'Med',  'High'] },
  ],
}

export const topObjections = [
  { rank: 1, text: 'Missing custom field mapping in export',         frequency: 34, severity: 'high' },
  { rank: 2, text: 'No audit log for compliance workflows',           frequency: 28, severity: 'high' },
  { rank: 3, text: 'Onboarding too complex for casual users',         frequency: 22, severity: 'med' },
  { rank: 4, text: 'API rate limits too restrictive for power users', frequency: 18, severity: 'med' },
  { rank: 5, text: 'Pricing tier gap between Pro and Team',          frequency: 14, severity: 'low' },
]

export const vsCompetitor = [
  { label: 'FinTrack v2',  pct: 74, sentiment: 'pos' },
  { label: 'YNAB',          pct: 68, sentiment: 'pos' },
  { label: 'Mint (legacy)', pct: 42, sentiment: 'neg' },
]
