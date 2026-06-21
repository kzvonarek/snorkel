import assert from 'node:assert/strict'
import { existsSync } from 'node:fs'
import test from 'node:test'

import { demoTopics, topicMarkdown } from '../src/data/demoTopics.js'

test('ships three complete demo topics with valid agent thoughts', () => {
  assert.equal(demoTopics.length, 3)
  for (const topic of demoTopics) {
    assert.equal(topic.agents.length, 9)
    assert.ok(topic.thoughts.length >= 12)
    const agentIds = new Set(topic.agents.map(agent => agent.id))
    assert.ok(topic.thoughts.every(([agentId]) => agentIds.has(agentId)))
    assert.match(topicMarkdown(topic), new RegExp(topic.name))
  }
})

test('every topic PDF is included in frontend public assets', () => {
  for (const topic of demoTopics) {
    assert.ok(existsSync(new URL(`../public${topic.pdfUrl}`, import.meta.url)))
  }
})
