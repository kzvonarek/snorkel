export const connectorGroups = [
  {
    category: 'Product behaviour',
    items: [
      { id: 'mixpanel',  name: 'Mixpanel',         icon: '📊', connected: true,  match: 92, progress: 92 },
      { id: 'amplitude', name: 'Amplitude',         icon: '📈', connected: false, match: 78, progress: 0  },
      { id: 'fullstory', name: 'FullStory',          icon: '🎥', connected: false, match: 65, progress: 0  },
    ]
  },
  {
    category: 'Support & sentiment',
    items: [
      { id: 'intercom',  name: 'Intercom',          icon: '💬', connected: true,  match: 88, progress: 88 },
      { id: 'zendesk',   name: 'Zendesk',            icon: '🎫', connected: false, match: 71, progress: 0  },
      { id: 'gong',      name: 'Gong (call intel)',  icon: '🎙', connected: false, match: 60, progress: 0  },
    ]
  },
  {
    category: 'Fallback',
    items: [
      { id: 'csv',       name: 'Upload CSV / JSON',  icon: '📄', connected: false, match: null, progress: 0 },
      { id: 'manual',    name: 'Manual entry',        icon: '✏️', connected: false, match: null, progress: 0 },
    ]
  },
]
