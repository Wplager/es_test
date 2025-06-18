<template>
    <header>
        <Header />
    </header>
    <main>
        <div class="detail-container">
            <h2 class="detail-title">{{ document.title }}</h2>
            <div class="detail-meta">
                <span class="detail-meta-item" v-if="document.author">
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
                        <path
                            d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"
                        ></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                    {{ document.author }}
                </span>
                <span class="detail-meta-item" v-if="document.date">
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
                        <rect
                            x="3"
                            y="4"
                            width="18"
                            height="18"
                            rx="2"
                            ry="2"
                        ></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    {{ document.date }}
                </span>
                <span class="detail-meta-item" v-if="document.type">
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
                        <path
                            d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                        ></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    {{ document.type }}
                </span>
            </div>
            <div
                class="detail-content"
                v-html="highlightMatches(document.content, query)"
            ></div>

            <div class="detail-actions">
                <button @click="goBackToResults" class="btn btn-secondary">
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
                        <polyline points="15 18 9 12 15 6"></polyline>
                    </svg>
                    返回列表
                </button>
                <button @click="goHome" class="btn btn-primary">
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
                        <path
                            d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"
                        ></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                    新的搜索
                </button>
            </div>
        </div>
    </main>
    <footer>
        <Footer />
    </footer>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import axios from 'axios'
const route = useRoute();
const router = useRouter();
const document = ref({});
const loading = ref(false);
const query = ref("");

// 从路由参数获取文档ID和查询
const id = computed(() => route.params.id);
query.value = route.query.q || "";

// 高亮匹配文本
function highlightMatches(text, term) {
    if (!term || !text) return text;
    const regex = new RegExp(term, "gi");
    return text.replace(
        regex,
        (match) => `<span class="highlight">${match}</span>`
    );
}

// 获取文档详情
const fetchDocument = async () => {
    if (!id.value) return;

    loading.value = true;
    try {
        const res = await axios.get(
            `/api/document/${id.value}`
        );
        document.value = res.data || {};
    } catch (error) {
        console.error("Error fetching document:", error);
        document.value = {}; // 设置默认值或处理错误
    } finally {
        loading.value = false;
    }
};

// 导航方法
const goBackToResults = () => {
    // 从当前路由获取查询参数
    const currentQuery = route.query.q;
    router.push({ name: "results", query: { q: currentQuery } });
};

const goHome = () => router.push("/");

// 监听路由变化
watch(
    () => route.params.id,
    (newId) => {
        if (newId) {
            fetchDocument();
        }
    }
);

// 组件挂载时获取文档详情
onMounted(() => {
    fetchDocument();
});
</script>
