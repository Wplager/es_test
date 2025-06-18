<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

// 提供全局导航方法给子组件
const goHome = () => router.push("/");
const goBackToResults = () => {
  // 从当前路由获取查询参数
  const currentQuery = router.currentRoute.value.query.q;
  router.push({ name: "results", query: { q: currentQuery } });
};

// 暴露全局方法给子组件
defineExpose({
  goHome,
  goBackToResults
});
</script>
