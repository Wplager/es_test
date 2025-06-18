<template>
    <header>
        <Header @go-home="goHome" />
    </header>
    <main class="container">
        <div class="hero">
            <h1 class="hero-title">探索健康知识宝库</h1>
            <p class="hero-subtitle">
                快速检索健康知识库内容
            </p>
            <form @submit.prevent="search" class="search-form">
                <input
                    type="text"
                    v-model="query"
                    placeholder="输入关键词、标题或作者..."
                />
                <button type="submit" class="search-btn">
                    <span v-if="!loading">搜索</span>
                    <span v-else class="loader"></span>
                </button>
            </form>
        </div>
    </main>
    <footer>
        <Footer />
    </footer>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";

const query = ref("");
const loading = ref(false);
const router = useRouter();

const search = () => {
  if (!query.value || !query.value.trim()) return;
  
  loading.value = true;
  
  // 导航到结果页
  router.push({ 
    name: "results", 
    query: { 
      q: query.value,
      page: 1 
    } 
  });
  
  loading.value = false;
};

const goHome = () => {
  router.push({ name: "home" });
};
</script>
