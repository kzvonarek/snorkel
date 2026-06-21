import { reactive } from 'vue'

const state = reactive({
  isRunning: false,
  currentRound: 0,
  totalRounds: 5,
  progress: 0,       // 0–100
})

export function startRun(rounds = 5) {
  state.totalRounds = rounds
  state.currentRound = 0
  state.progress = 0
  state.isRunning = true
}

export function tickRun(roundsDone, progress) {
  state.currentRound = roundsDone
  state.progress = progress
}

export function endRun() {
  state.progress = 100
  state.isRunning = false
}

export default state
