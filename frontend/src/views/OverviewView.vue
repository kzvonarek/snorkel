<template>
  <div class="overview">
    <div class="overview-section">
      <h2 class="section-heading">Build &amp; simulate</h2>
      <div class="tile-grid">
        <router-link
          v-for="tile in buildTiles"
          :key="tile.to"
          :to="tile.to"
          class="tile"
        >
          <Thumbnail :color="tile.color" :glyph="tile.glyph" />
          <div class="tile-label">{{ tile.label }}</div>
          <div class="tile-desc">{{ tile.desc }}</div>
        </router-link>
      </div>
    </div>

    <div class="overview-section">
      <h2 class="section-heading">Analyse &amp; share</h2>
      <div class="tile-grid tile-grid--3">
        <router-link
          v-for="tile in outputTiles"
          :key="tile.to"
          :to="tile.to"
          class="tile"
        >
          <Thumbnail :color="tile.color" :glyph="tile.glyph" />
          <div class="tile-label">{{ tile.label }}</div>
          <div class="tile-desc">{{ tile.desc }}</div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import Thumbnail from "@/components/ui/Thumbnail.vue";

const buildTiles = [
  {
    to: "/connect",
    label: "Connect data",
    desc: "Link your product, support & behaviour signals.",
    color: "#4B5FA8",
    glyph: "⇌",
  },
  {
    to: "/personas",
    label: "Personas",
    desc: "AI-built segments from your connected data.",
    color: "#3B7355",
    glyph: "◎",
  },
  {
    to: "/market",
    label: "Market context",
    desc: "Upload competitive intel & environment files.",
    color: "#8E6B4E",
    glyph: "◈",
  },
  {
    to: "/products",
    label: "Product material",
    desc: "Upload specs, decks & prototype screenshots.",
    color: "#6B4E8E",
    glyph: "⬕",
  },
  {
    to: "/sandbox",
    label: "Configure run",
    desc: "Drag segments & assets onto the simulation canvas.",
    color: "#4E7E8E",
    glyph: "⧉",
  },
  {
    to: "/swarm",
    label: "Live feed",
    desc: "Watch agents react in real time.",
    color: "#8E4E6B",
    glyph: "◉",
  },
];

const outputTiles = [
  {
    to: "/results",
    label: "Results dashboard",
    desc: "PMF score, adoption heatmap & objection ranking.",
    color: "#3B6B55",
    glyph: "◫",
  },
  {
    to: "/report",
    label: "Report & chat",
    desc: "Download the curated PDF and ask follow-up questions.",
    color: "#4B5FA8",
    glyph: "▤",
  },
  {
    to: "/projects",
    label: "All projects",
    desc: "Browse and manage your PMF studies.",
    color: "#7882A0",
    glyph: "▦",
  },
];
</script>

<style scoped>
.overview {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.section-heading {
  font-family: "Newsreader", serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 16px;
}

.tile-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.tile-grid--3 {
  grid-template-columns: repeat(3, 1fr);
}

.tile {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
  transition:
    box-shadow 0.15s,
    transform 0.15s;
  text-decoration: none;
}

.tile:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.tile-label {
  font-size: 13px;
  font-weight: 700;
  color: var(--ink);
}

.tile-desc {
  font-size: 12px;
  color: var(--text-3);
  line-height: 1.45;
}
</style>
