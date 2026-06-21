const makeAgent = (id, name, segment, color, x, y) => ({ id, name, segment, color, x, y })

export const demoTopics = [
  {
    id: 'orbit-note', category: 'New tech product', name: 'Orbit Note',
    tagline: 'An AI meeting puck that turns room audio into decisions, owners, and follow-ups.',
    question: 'Will hybrid teams trust and pay for an always-on AI meeting device?',
    color: '#4B5FA8', glyph: 'AI', duration: 16000, rounds: 5,
    pdfUrl: '/reports/orbit-note-pmf-report.pdf',
    agents: [
      makeAgent('on-1','Maya Chen','Product lead','#6C7FD1',16,24), makeAgent('on-2','Theo Grant','Engineering manager','#4B5FA8',24,49), makeAgent('on-3','Priya Shah','Operations lead','#8998D8',18,72),
      makeAgent('on-4','Luis Romero','Remote employee','#3B8D7A',48,20), makeAgent('on-5','Avery Brooks','Design lead','#56A58F',54,48), makeAgent('on-6','Noor Haddad','Sales manager','#277363',46,76),
      makeAgent('on-7','Elena Park','Security buyer','#B46A55',80,25), makeAgent('on-8','Marcus Bell','Finance buyer','#C98772',76,52), makeAgent('on-9','Sam Okafor','IT administrator','#9E5340',83,74),
    ],
    thoughts: [
      ['on-1','The decision log is immediately useful. I spend Mondays reconstructing who promised what.','positive'],
      ['on-7','Always-on audio creates a consent problem before it creates a productivity win.','concern'],
      ['on-4','If it distinguishes room voices from remote voices, it fixes a real hybrid-work gap.','positive'],
      ['on-9','I need centralized retention controls and a hardware mute state I can verify remotely.','concern'],
      ['on-2','The Jira handoff is more valuable than another transcript. Show me reliable action extraction.','neutral'],
      ['on-8','$29 per room per month works; another $400 device in every room is harder to approve.','concern'],
      ['on-5','A physical object makes recording visible. That may feel more trustworthy than a hidden bot.','positive'],
      ['on-6','Automatic follow-up drafts could save each rep twenty minutes after a customer call.','positive'],
      ['on-7','The buying path opens if raw audio can be disabled and processing region selected.','neutral'],
      ['on-1','I would pilot this in three rooms if the summary links every claim back to the moment it was said.','positive'],
      ['on-9','SCIM, audit logs, and a documented deletion SLA are launch requirements.','concern'],
      ['on-2','Net: strong workflow fit, but accuracy and admin controls decide whether it survives the pilot.','neutral'],
    ],
    metrics: { fit: 78, positive: 5, concerns: 4, pilot: 6 },
    objections: ['Recording consent and visible privacy controls','Enterprise retention, deletion, and regional processing','Hardware cost compared with software meeting bots'],
    recommendation: 'Pilot in three hybrid meeting rooms with raw-audio storage disabled. Gate expansion on action-item precision, consent comprehension, and administrator controls.',
  },
  {
    id: 'emberwild', category: 'New video game', name: 'Emberwild',
    tagline: 'A four-player survival game where seasons reshape the map and alliances determine the ending.',
    question: 'Can a social survival game retain both coordinated groups and solo players?',
    color: '#8E6B4E', glyph: 'EW', duration: 16000, rounds: 5,
    pdfUrl: '/reports/emberwild-pmf-report.pdf',
    agents: [
      makeAgent('ew-1','Jules Kim','Co-op organizer','#D08857',16,24), makeAgent('ew-2','Rina Patel','Competitive player','#B66A3B',23,50), makeAgent('ew-3','Cal Morgan','Streamer','#E09A68',17,76),
      makeAgent('ew-4','Tess Nguyen','Solo explorer','#6B8E4E',49,21), makeAgent('ew-5','Andre Silva','Builder','#83A968',55,48), makeAgent('ew-6','Morgan Lee','Lore hunter','#55783A',47,75),
      makeAgent('ew-7','Ivy Walker','Time-limited parent','#6C6F91',80,24), makeAgent('ew-8','Dev Malik','Accessibility advocate','#8589AB',76,52), makeAgent('ew-9','Nia Foster','Lapsed survival fan','#555975',83,75),
    ],
    thoughts: [
      ['ew-1','A shared settlement that remembers our choices gives the group a reason to return next week.','positive'],
      ['ew-7','I cannot lose a whole season because I missed two evenings. Catch-up has to respect my time.','concern'],
      ['ew-3','Seasonal map transformations are streamable moments, especially if viewers can predict outcomes.','positive'],
      ['ew-4','Please let solo players hire companions or join public expeditions without voice chat.','concern'],
      ['ew-5','Blueprint sharing could create a whole creator economy without turning the game pay-to-win.','positive'],
      ['ew-8','Visual weather cues need audio and haptic equivalents. Storms cannot rely on color alone.','concern'],
      ['ew-2','Alliance betrayal is exciting once, but it becomes exhausting if every optimal strategy requires it.','neutral'],
      ['ew-6','The world-ending vote is a strong narrative payoff if earlier discoveries meaningfully change the options.','positive'],
      ['ew-9','I left survival games because of repetitive resource chores. Automate the boring loop by midgame.','concern'],
      ['ew-1','Eight-week seasons feel long enough to build history and short enough to invite a fresh group.','positive'],
      ['ew-7','A two-hour weekly expedition cap would make this feel possible instead of like a second job.','neutral'],
      ['ew-3','I would wishlist after a public demo that proves the social systems create stories, not just grind.','positive'],
    ],
    metrics: { fit: 81, positive: 6, concerns: 4, pilot: 7 },
    objections: ['Seasonal progress may punish time-limited players','Solo and no-voice matchmaking need first-class support','Resource grind could overwhelm the social differentiation'],
    recommendation: 'Ship a public co-op demo centered on one seasonal transformation. Measure group return intent while testing catch-up, solo companions, and reduced midgame resource chores.',
  },
]

export const getDemoTopic = id => demoTopics.find(topic => topic.id === id) || demoTopics[0]

export function topicMarkdown(topic) {
  return `# ${topic.name} PMF Simulation Report\n\n## Concept\n${topic.tagline}\n\n## Research question\n${topic.question}\n\n## Simulated signals\n- Fit signal: ${topic.metrics.fit}/100\n- Positive reactions: ${topic.metrics.positive}\n- Material concerns: ${topic.metrics.concerns}\n- Pilot or trial intent: ${topic.metrics.pilot} of ${topic.agents.length} personas\n\n## Leading objections\n${topic.objections.map(item => `- ${item}`).join('\n')}\n\n## Recommendation\n${topic.recommendation}\n\n## Methodology\nNine representative personas evaluated the concept across five simulated rounds. Findings summarize their stated priorities, objections, and pilot intent and should be validated with primary customer research.`
}
