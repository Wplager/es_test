<template>
  <a href="#" class="logo" @click.prevent="$emit('go-home')">
    <div class="logo-icon">P</div>
    <span class="logo-text">健康知识检索系统</span>
  </a>
</template>

<script>
export default {
  emits: ['go-home']
}
</script>
