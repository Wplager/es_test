<template>
  <form @submit.prevent="$emit('search')" class="search-form">
    <input
      type="text"
      :value="query"
      @input="$emit('update:query', $event.target.value)"
      placeholder="输入关键词、标题或作者..."
    />
    <button type="submit" class="search-btn">
      <span v-if="!loading">搜索</span>
      <span v-else class="loader"></span>
    </button>
  </form>
</template>

<script>
export default {
  props: {
    query: {
      type: String,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['search', 'update:query']
}
</script>
