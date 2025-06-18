<template>
  <div class="result-item" @click="$emit('view-details', item)">
    <h3 class="result-title">
      <span v-html="highlightMatches(item.title, query)"></span>
    </h3>
    <div class="result-meta">
      <span class="result-meta-item" v-if="item.author">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
        {{ item.author }}
      </span>
      <span class="result-meta-item" v-if="item.date">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        {{ item.date }}
      </span>
    </div>
    <p class="result-snippet" v-html="highlightMatches(item.snippet, query)"></p>
  </div>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true
    },
    query: {
      type: String,
      default: ''
    }
  },
  methods: {
    highlightMatches(text, searchTerm) {
      if (!searchTerm || !text) return text;
      const terms = searchTerm.split(" ").filter((term) => term.length > 0);
      let highlighted = text;
      terms.forEach((term) => {
        const regex = new RegExp(term, "gi");
        highlighted = highlighted.replace(
          regex,
          (match) => `<span class="highlight">${match}</span>`
        );
      });
      return highlighted;
    }
  },
  emits: ['view-details']
}
</script>
