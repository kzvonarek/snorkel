export const RUN_STORAGE_KEY = 'snorkel.activeRun.v1'

export function expandPersonas(selected, countPerSegment) {
  return selected.flatMap(segment => Array.from({ length: countPerSegment }, (_, index) => ({
    identity: `${segment.id}-${index + 1}`,
    username: `${segment.id.replace(/[^a-z0-9]/gi, '_')}_${index + 1}`,
    segment: segment.name,
    user_char: `You are representative ${index + 1} of the ${segment.name} segment. Traits: ${segment.traits.join(', ')}. Customer evidence: ${segment.quote}`,
    description: `${segment.name} customer representative`,
    confidence: segment.confidence === 'med' ? 'medium' : segment.confidence,
    traits: segment.traits,
    evidence_references: segment.sources.map(source => source.label),
  })))
}

export function readStoredRun(storage) {
  if (!storage) return {}
  try { return JSON.parse(storage.getItem(RUN_STORAGE_KEY) || '{}') } catch { return {} }
}
