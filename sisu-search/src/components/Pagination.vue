<template>
  <div class="pagination" v-if="totalPages > 1">
    <button
      class="pagination-btn"
      :disabled="currentPage === 1"
      @click="$emit('page-change', currentPage - 1)"
    >
      上一页
    </button>
    <button
      v-for="n in visiblePages"
      :key="n"
      class="pagination-btn"
      :class="{ active: n === currentPage }"
      @click="$emit('page-change', n)"
    >
      {{ n }}
    </button>
    <button
      class="pagination-btn"
      :disabled="currentPage === totalPages"
      @click="$emit('page-change', currentPage + 1)"
    >
      下一页
    </button>
  </div>
</template>

<script>
export default {
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    },
    visiblePages: {
      type: Array,
      required: true
    }
  },
  emits: ['page-change']
}
</script>
