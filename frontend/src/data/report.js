export const sections = [
  { id: 'exec',        label: 'Executive summary' },
  { id: 'pmfscore',   label: 'PMF score' },
  { id: 'segments',   label: 'Segment breakdown' },
  { id: 'objections', label: 'Top objections' },
  { id: 'adoption',   label: 'Adoption heatmap' },
  { id: 'method',     label: 'Methodology' },
]

export const executiveSummary = `FinTrack v2 achieves a PMF score of 74/100, indicating strong product-market fit with Power Users and moderate fit with Casual Explorers. Finance Professionals remain underserved by the current feature set, representing the highest-upside expansion opportunity.

Key friction points centre on export customisation and compliance tooling. Addressing these two areas is projected to lift the overall PMF score to 82+ and unlock Enterprise tier adoption.`

export const methodology = `Simulation run: 3 segments × 14 agents × 5 rounds (social + interview interleaved).
Data sources: Mixpanel (92% match), Intercom (88% match).
Persona confidence: Power Users — High; Casual Explorers — Medium; Finance Professionals — High.`

export const chatHistory = [
  {
    role: 'bot',
    text: 'This is your PMF Report for FinTrack v2. I can help you refine sections, drill into segment data, or suggest copy edits. What would you like to explore?',
    time: '2:14 PM',
  },
]

export const suggestedEdits = [
  'Strengthen the Finance Professional recommendation',
  'Add a competitor comparison paragraph',
  'Shorten the executive summary to 3 sentences',
]

export const cannedReplies = {
  default: "I've updated the report section based on your input. The changes reflect the simulation data from round 5. Would you like me to adjust the tone or add supporting evidence from the agent transcripts?",
  strengthen: "I've expanded the Finance Professional section to highlight the compliance gap as a $2M ARR opportunity based on the segment size and willingness-to-pay signals from the Intercom data.",
  competitor: "Added a competitor comparison paragraph contrasting FinTrack v2's API-first positioning against YNAB's simplicity focus, noting the displaced Mint users as an immediate acquisition opportunity.",
  shorten: "Executive summary condensed to: FinTrack v2 scores 74/100 PMF. Power Users are highly satisfied; Finance Professionals are underserved. Closing the export and compliance gaps is the highest-leverage next step.",
}
