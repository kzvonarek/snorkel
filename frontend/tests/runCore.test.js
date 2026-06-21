import assert from 'node:assert/strict'
import test from 'node:test'

import { expandPersonas, readStoredRun, RUN_STORAGE_KEY } from '../src/composables/runCore.js'

const segment = { id: 'power-users', name: 'Power Users', traits: ['API-first'], quote: 'Needs flexible exports', confidence: 'high', sources: [{ label: 'Support' }] }

test('expands segments into unique PersonaInput payloads', () => {
  const personas = expandPersonas([segment], 2)
  assert.equal(personas.length, 2)
  assert.notEqual(personas[0].identity, personas[1].identity)
  assert.equal(personas[0].segment, 'Power Users')
  assert.match(personas[0].user_char, /flexible exports/)
})

test('restores valid session state and ignores malformed state', () => {
  assert.deepEqual(readStoredRun({ getItem: key => key === RUN_STORAGE_KEY ? '{"mode":"fixture"}' : null }), { mode: 'fixture' })
  assert.deepEqual(readStoredRun({ getItem: () => '{bad json' }), {})
})
