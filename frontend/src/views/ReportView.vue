<template>
  <div class="report-layout">
    <!-- Section nav -->
    <nav class="section-nav">
      <div class="section-nav-heading section-nav-heading--compact">
        Live reports
      </div>
      <div v-if="loadingReports" class="report-source-note">
        Loading from backend…
      </div>
      <div v-else-if="reportError" class="report-source-note">
        {{ reportError }}
      </div>
      <button
        v-for="report in reports"
        :key="report.report_id"
        class="report-btn"
        :class="{ active: selectedReportId === report.report_id }"
        @click="selectReport(report.report_id)"
      >
        {{ report.report_id }}
      </button>

      <div class="section-nav-heading">Sections</div>
      <button
        v-for="s in sections"
        :key="s.id"
        class="section-btn"
        :class="{ active: activeSection === s.id }"
        @click="activeSection = s.id"
      >
        {{ s.label }}
      </button>
    </nav>

    <!-- PDF mock -->
    <div class="pdf-mock">
      <div class="pdf-page">
        <div class="pdf-header">
          <div class="pdf-title">{{ reportTitle }}</div>
          <div class="pdf-date">Generated {{ reportDate }}</div>
        </div>

        <div v-if="selectedReportDetails" class="report-meta-card">
          <div>
            <strong>Simulation:</strong>
            {{ selectedReportDetails.simulation_id }}
          </div>
          <div><strong>Status:</strong> {{ selectedReportDetails.status }}</div>
        </div>

        <div v-if="activeSection === 'exec'" class="pdf-section">
          <h2>Executive Summary</h2>
          <textarea
            v-model="execSummary"
            class="editable-area"
            rows="8"
          ></textarea>
        </div>

        <div v-else-if="activeSection === 'pmfscore'" class="pdf-section">
          <h2>PMF Score</h2>
          <div class="score-display">
            <div class="score-big">74</div>
            <div class="score-context">
              / 100 — Strong fit with Power Users, moderate fit overall
            </div>
          </div>
        </div>

        <div v-else-if="activeSection === 'segments'" class="pdf-section">
          <h2>Segment Breakdown</h2>
          <BarChartCss :rows="sentimentBySegment" />
        </div>

        <div v-else-if="activeSection === 'objections'" class="pdf-section">
          <h2>Top Objections</h2>
          <ol class="obj-list">
            <li v-for="o in topObjections" :key="o.rank">
              {{ o.text }} <em>({{ o.frequency }}x)</em>
            </li>
          </ol>
        </div>

        <div v-else-if="activeSection === 'adoption'" class="pdf-section">
          <h2>Adoption Heatmap</h2>
          <Heatmap :cols="adoptionHeatmap.cols" :rows="adoptionHeatmap.rows" />
        </div>

        <div v-else-if="activeSection === 'method'" class="pdf-section">
          <h2>Methodology</h2>
          <p class="method-text">{{ methodologyText }}</p>
        </div>
      </div>
    </div>

    <!-- Chat panel -->
    <div class="chat-panel">
      <div class="chat-heading">Ask &amp; refine</div>

      <div class="chat-messages" ref="chatEl">
        <ChatBubble
          v-for="(msg, i) in chat"
          :key="i"
          :role="msg.role"
          :text="msg.text"
          :time="msg.time"
        />
      </div>

      <div class="suggested-edits">
        <div class="suggested-label">Suggested edits</div>
        <button
          v-for="(edit, i) in suggestedEdits"
          :key="i"
          class="edit-chip"
          @click="applyEdit(edit)"
        >
          {{ edit }}
        </button>
      </div>

      <div v-if="selectedReportDetails" class="report-source-card">
        <div class="detail-heading">Backend report</div>
        <div class="report-source-title">
          {{ selectedReportDetails.report_id }}
        </div>
        <div class="report-source-note">
          {{
            selectedReportDetails.simulation_requirement ||
            "Loaded from the live backend"
          }}
        </div>
      </div>

      <div class="chat-input-row">
        <input
          v-model="userInput"
          class="chat-input"
          placeholder="Ask about the report…"
          @keydown.enter="sendMessage"
        />
        <button class="chat-send" @click="sendMessage">↑</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import ChatBubble from "@/components/ui/ChatBubble.vue";
import BarChartCss from "@/components/ui/BarChartCss.vue";
import Heatmap from "@/components/ui/Heatmap.vue";
import {
  sections,
  executiveSummary,
  methodology,
  chatHistory,
  suggestedEdits,
  cannedReplies,
} from "@/data/report.js";
import {
  sentimentBySegment,
  adoptionHeatmap,
  topObjections,
} from "@/data/results.js";
import { getReport, listReports } from "@/api/report";

const activeSection = ref("exec");
const execSummary = ref(executiveSummary);
const methodologyText = ref(methodology);
const reportTitle = ref("PMF Report — FinTrack v2");
const reportDate = ref(new Date().toLocaleDateString());
const chat = ref(chatHistory.map((m) => ({ ...m })));
const userInput = ref("");
const chatEl = ref(null);
const reports = ref([]);
const selectedReportId = ref("");
const selectedReportDetails = ref(null);
const loadingReports = ref(false);
const reportError = ref("");

function formatDate(value) {
  if (!value) return new Date().toLocaleDateString();
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleDateString();
}

async function selectReport(reportId) {
  selectedReportId.value = reportId;
  const summary = reports.value.find((report) => report.report_id === reportId);

  try {
    const response = await getReport(reportId);
    const data = response?.data ?? response;
    selectedReportDetails.value = data;
    reportTitle.value = data?.simulation_requirement
      ? `PMF Report — ${data.simulation_requirement}`
      : `PMF Report — ${reportId}`;
    reportDate.value = formatDate(data?.created_at || data?.completed_at);
    execSummary.value = data?.outline?.summary || executiveSummary;
    methodologyText.value = data?.outline?.methodology || methodology;
  } catch {
    selectedReportDetails.value = summary || null;
    reportTitle.value = summary?.simulation_requirement
      ? `PMF Report — ${summary.simulation_requirement}`
      : `PMF Report — ${reportId}`;
    reportDate.value = formatDate(summary?.created_at);
  }
}

async function loadReports() {
  loadingReports.value = true;
  reportError.value = "";

  try {
    const response = await listReports();
    const data = response?.data ?? response;
    reports.value = Array.isArray(data) ? data : [];

    if (reports.value.length) {
      await selectReport(reports.value[0].report_id);
    }
  } catch {
    reportError.value =
      "Backend report list unavailable, showing the local mock report.";
    reports.value = [];
    selectedReportDetails.value = null;
  } finally {
    loadingReports.value = false;
  }
}

onMounted(loadReports);

function scrollChat() {
  nextTick(() => {
    if (chatEl.value) chatEl.value.scrollTop = chatEl.value.scrollHeight;
  });
}

function ts() {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;
  chat.value.push({ role: "user", text, time: ts() });
  userInput.value = "";
  scrollChat();
  setTimeout(() => {
    chat.value.push({ role: "bot", text: cannedReplies.default, time: ts() });
    scrollChat();
  }, 800);
}

function applyEdit(edit) {
  const lc = edit.toLowerCase();
  const reply = lc.includes("finance")
    ? cannedReplies.strengthen
    : lc.includes("competitor")
      ? cannedReplies.competitor
      : lc.includes("shorten")
        ? cannedReplies.shorten
        : cannedReplies.default;
  chat.value.push({ role: "user", text: edit, time: ts() });
  scrollChat();
  setTimeout(() => {
    chat.value.push({ role: "bot", text: reply, time: ts() });
    scrollChat();
  }, 800);
}
</script>

<style scoped>
.report-layout {
  display: grid;
  grid-template-columns: 170px 1fr 280px;
  gap: 16px;
  height: calc(100vh - var(--topbar-h) - 56px);
}

.section-nav {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 14px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.section-nav-heading {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-3);
  margin-bottom: 6px;
  padding: 0 6px;
}

.section-nav-heading--compact {
  margin-bottom: 2px;
}

.report-btn {
  text-align: left;
  padding: 7px 10px;
  border-radius: 7px;
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-2);
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--bg);
}

.report-btn.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.report-source-note {
  font-size: 11.5px;
  color: var(--text-3);
  line-height: 1.5;
  padding: 0 6px;
}
.section-btn {
  text-align: left;
  padding: 7px 10px;
  border-radius: 7px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-2);
  cursor: pointer;
  transition:
    background 0.12s,
    color 0.12s;
}
.section-btn:hover {
  background: var(--bg);
  color: var(--ink);
}
.section-btn.active {
  background: var(--accent);
  color: #fff;
}

.pdf-mock {
  overflow-y: auto;
}

.pdf-page {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 32px 36px;
  min-height: 100%;
  box-shadow: var(--shadow-card);
}

.pdf-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  padding-bottom: 18px;
  border-bottom: 2px solid var(--ink);
}
.pdf-title {
  font-family: "Newsreader", serif;
  font-size: 22px;
  font-weight: 600;
  color: var(--ink);
}
.pdf-date {
  font-size: 12px;
  color: var(--text-3);
}

.report-meta-card {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid var(--border);
  background: var(--bg);
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 12px;
  color: var(--text-2);
  margin-bottom: 18px;
}

.pdf-section h2 {
  font-family: "Newsreader", serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 16px;
}

.editable-area {
  width: 100%;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  font-family: inherit;
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--ink);
  resize: vertical;
  background: var(--bg);
  outline: none;
  transition: border-color 0.15s;
}
.editable-area:focus {
  border-color: var(--accent);
}

.score-display {
  display: flex;
  align-items: baseline;
  gap: 16px;
}
.score-big {
  font-family: "Newsreader", serif;
  font-size: 64px;
  font-weight: 600;
  color: var(--accent);
  line-height: 1;
}
.score-context {
  font-size: 14px;
  color: var(--text-2);
  max-width: 280px;
}

.obj-list {
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.obj-list li {
  font-size: 13px;
  color: var(--ink);
}

.method-text {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.7;
  white-space: pre-line;
}

.chat-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-heading {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-3);
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggested-edits {
  padding: 10px 12px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.suggested-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-3);
  margin-bottom: 2px;
}

.report-source-card {
  margin-bottom: 14px;
  padding: 12px 14px;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}

.report-source-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--ink);
  margin-top: 4px;
  margin-bottom: 4px;
}
.edit-chip {
  text-align: left;
  font-size: 11.5px;
  color: var(--accent);
  background: var(--accent-light);
  border: 1px solid var(--accent);
  border-radius: 6px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background 0.12s;
}
.edit-chip:hover {
  background: var(--accent);
  color: #fff;
}

.chat-input-row {
  display: flex;
  gap: 6px;
  padding: 10px;
  border-top: 1px solid var(--border);
}
.chat-input {
  flex: 1;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 13px;
  outline: none;
  background: var(--bg);
  color: var(--ink);
  transition: border-color 0.15s;
}
.chat-input:focus {
  border-color: var(--accent);
}
.chat-send {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
}
.chat-send:hover {
  background: var(--accent-hover);
}
</style>
