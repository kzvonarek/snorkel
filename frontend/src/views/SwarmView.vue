<template>
  <div class="swarm-layout">
    <!-- Main canvas -->
    <div class="swarm-canvas">
      <div class="canvas-dark">
        <div class="cluster-label" style="left:14%;top:8%">Power Users</div>
        <div class="cluster-label" style="left:46%;top:8%">Casual Explorers</div>
        <div class="cluster-label" style="left:75%;top:8%">Finance Pros</div>

        <div
          v-for="dot in dots"
          :key="dot.id"
          class="swarm-dot"
          :class="`dot--${dot.sentiment}`"
          :style="{ left: dot.cx + '%', top: dot.cy + '%' }"
          @click="activeDot = activeDot === dot.id ? null : dot.id"
          :title="dot.agent"
        ></div>

        <div v-if="activeDot && transcripts[activeDot]" class="transcript-overlay">
          <div class="transcript-title">{{ dots.find(d => d.id === activeDot)?.agent }}</div>
          <div v-for="(line, i) in transcripts[activeDot]" :key="i" class="transcript-line">
            <span class="tl-role">{{ line.role }}</span>
            <span class="tl-text">{{ line.text }}</span>
          </div>
          <button class="transcript-close" @click="activeDot = null">✕</button>
        </div>

        <div class="swarm-progress-bar">
          <div class="progress-track-dark">
            <div class="progress-fill-dark" :style="{ width: runState.progress + '%' }"></div>
          </div>
          <div class="progress-info">
            <span>Round {{ runState.currentRound }} / {{ runState.totalRounds }}</span>
            <span>{{ runState.progress }}% complete</span>
          </div>
        </div>
      </div>

      <div v-if="!runState.isRunning && runState.progress === 100" class="complete-banner">
        Simulation complete —
        <router-link to="/results" class="complete-link">View results dashboard →</router-link>
      </div>
    </div>

    <!-- Live feed -->
    <div class="feed-panel">
      <div class="feed-heading">Live feed</div>
      <div class="feed-list" ref="feedList">
        <div v-for="(msg, i) in feed" :key="i" class="feed-item">
          <span class="feed-time">{{ msg.ts }}</span>
          <span class="feed-msg">{{ msg.msg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import runState, { tickRun, endRun, startRun } from '@/composables/useRun.js'
import { swarmDots, sentimentSequence, feedScript, transcripts } from '@/data/swarm.js'

const dots = reactive(swarmDots.map(d => ({ ...d })))
const feed = ref([])
const activeDot = ref(null)
const feedList = ref(null)

const timers = []

function now() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

function scrollFeed() {
  nextTick(() => { if (feedList.value) feedList.value.scrollTop = feedList.value.scrollHeight })
}

onMounted(() => {
  if (!runState.isRunning) startRun(5)

  let dotIdx = 0
  const totalRounds = runState.totalRounds || 5
  const totalMs = feedScript[feedScript.length - 1].t + 1500

  const dotInterval = setInterval(() => {
    if (dotIdx < dots.length) {
      dots[dotIdx].sentiment = sentimentSequence[dotIdx % sentimentSequence.length]
      dotIdx++
    }
    const pct = Math.round((dotIdx / dots.length) * 100)
    const round = Math.ceil((dotIdx / dots.length) * totalRounds)
    tickRun(Math.min(round, totalRounds), pct)
  }, 700)
  timers.push({ type: 'interval', id: dotInterval })

  feedScript.forEach(({ t, msg }) => {
    const id = setTimeout(() => {
      feed.value.push({ ts: now(), msg })
      scrollFeed()
    }, t)
    timers.push({ type: 'timeout', id })
  })

  const endId = setTimeout(() => {
    clearInterval(dotInterval)
    endRun()
    feed.value.push({ ts: now(), msg: '✓ Simulation finished. Results ready.' })
    scrollFeed()
  }, totalMs)
  timers.push({ type: 'timeout', id: endId })
})

onUnmounted(() => {
  timers.forEach(t => {
    if (t.type === 'interval') clearInterval(t.id)
    else clearTimeout(t.id)
  })
})
</script>

<style scoped>
.swarm-layout {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 16px;
  height: calc(100vh - var(--topbar-h) - 56px);
}

.swarm-canvas { display: flex; flex-direction: column; gap: 10px; }

.canvas-dark {
  flex: 1;
  background: #16181a;
  border-radius: var(--radius-card);
  position: relative;
  overflow: hidden;
}

.cluster-label {
  position: absolute;
  color: #6b7280;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.swarm-dot {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #4b5563;
  cursor: pointer;
  transform: translate(-50%, -50%);
  transition: background 0.4s, box-shadow 0.4s;
}
.dot--pos { background: #5ca642; box-shadow: 0 0 0 6px rgba(92,166,66,0.25); }
.dot--neg { background: #c44a4a; box-shadow: 0 0 0 6px rgba(196,74,74,0.25); }
.dot--neu { background: #c49a4a; box-shadow: 0 0 0 6px rgba(196,154,74,0.25); }

.transcript-overlay {
  position: absolute;
  top: 48px;
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid var(--border);
  padding: 14px;
  box-shadow: var(--shadow-md);
  z-index: 10;
}
.transcript-title { font-size: 13px; font-weight: 700; color: var(--ink); margin-bottom: 8px; }
.transcript-line {
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 5px 0;
  border-bottom: 1px solid var(--border);
  font-size: 11.5px;
}
.transcript-line:last-child { border-bottom: none; }
.tl-role { font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-3); }
.tl-text { color: var(--text-2); }
.transcript-close {
  position: absolute; top: 10px; right: 10px;
  font-size: 12px; color: var(--text-3); cursor: pointer;
  padding: 2px 6px; border-radius: 4px; background: var(--bg);
}

.swarm-progress-bar {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 10px 14px;
  background: rgba(22,24,26,0.85);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.progress-track-dark {
  height: 4px;
  background: rgba(255,255,255,0.15);
  border-radius: 2px;
  overflow: hidden;
}
.progress-fill-dark {
  height: 100%;
  background: var(--accent);
  border-radius: 2px;
  transition: width 0.5s ease;
}
.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: rgba(255,255,255,0.5);
}

.complete-banner {
  background: var(--success-bg);
  color: var(--success-fg);
  border: 1px solid var(--success-fg);
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 13.5px;
  font-weight: 600;
}
.complete-link { color: var(--success-fg); text-decoration: underline; margin-left: 6px; }

.feed-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.feed-heading {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-3);
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
}
.feed-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.feed-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 11.5px;
  color: var(--text-2);
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}
.feed-item:last-child { border-bottom: none; }
.feed-time { font-size: 10px; color: var(--text-3); font-weight: 600; }
</style>
