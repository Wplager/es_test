<template>
  <header>
    <div class="header-content">
      <Logo @go-home="$emit('go-home')" />
    </div>
  </header>
</template>

<script>
import Logo from './Logo.vue';

export default {
  components: {
    Logo
  },
  emits: ['go-home']
}
</script>
