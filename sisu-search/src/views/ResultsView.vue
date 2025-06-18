<template>
    <header>
        <Header @go-home="goHome" />
    </header>
    <main class="container">
        <div class="results-header">
            <h2 class="results-title">{{ query ? '搜索结果' : '所有记录' }}</h2>
            <div class="results-count">共 {{ results.length }} 条结果</div>
        </div>

        <div v-if="loading" class="loader-container">
            <div class="loader"></div>
        </div>

        <div v-else>
            <div
                v-for="result in paginatedResults"
                :key="result.id"
                class="result-item"
                @click="viewDetails(result)"
            >
                <h3 class="result-title">{{ result.title }}</h3>
                <div class="result-meta">
                    <span class="result-meta-item" v-if="result.author"
                        >作者: {{ result.author }}</span
                    >
                    <span class="result-meta-item" v-if="result.date"
                        >日期: {{ result.date }}</span
                    >
                    <span class="result-meta-item" v-if="result.type"
                        >类型: {{ result.type }}</span
                    >
                </div>
                <div
                    class="result-snippet"
                    v-html="highlightMatches(result.snippet, query)"
                ></div>
            </div>

            <Pagination
                v-if="totalPages > 1"
                :currentPage="currentPage"
                :totalPages="totalPages"
                :visiblePages="visiblePages"
                @page-change="goToPage"
            />
        </div>
    </main>
    <footer>
        <Footer />
    </footer>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import Pagination from "../components/Pagination.vue";
import axios from 'axios'
const router = useRouter();
const route = useRoute();

const results = ref([]);
const currentPage = ref(1);
const itemsPerPage = 20;
const loading = ref(false);

// 从路由参数获取查询和页码
const query = computed(() => route.query.q || "");
const initialPage = computed(() => parseInt(route.query.page) || 1);

// 分页计算
const totalPages = computed(() =>
    Math.ceil(results.value.length / itemsPerPage)
);
const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    return results.value.slice(start, start + itemsPerPage);
});

const visiblePages = computed(() => {
    const maxVisiblePages = 5;
    const pages = [];
    let start = Math.max(
        1,
        currentPage.value - Math.floor(maxVisiblePages / 2)
    );
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1);

    if (end - start + 1 < maxVisiblePages) {
        start = Math.max(1, end - maxVisiblePages + 1);
    }

    for (let i = start; i <= end; i++) {
        pages.push(i);
    }
    return pages;
});

// 高亮匹配文本
function highlightMatches(text, term) {
    if (!term || !text) return text;
    const regex = new RegExp(term, "gi");
    return text.replace(
        regex,
        (match) => `<span class="highlight">${match}</span>`
    );
}

// 获取搜索结果
const fetchResults = async () => {
    loading.value = true;
    try {
        let res;
        if (query.value) {
            res = await axios.post(
                "/api/search",
                {
                    query: query.value,
                    page: currentPage.value,
                    per_page: itemsPerPage,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
        } else {
            res = await axios.get("/api/all");
            res.data = { results: res.data.results };
        }
        console.log(res.data);
        // 直接访问 res.data 获取解析后的数据
        const data = res.data;
        console.log("实际数据:", data);
        
        if ((!data.results || data.results.length == 0)) {
            // If search returned no results, try getting all records
            const allRes = await axios.get("/api/all");
            results.value = allRes.data.results || [];
        } else {
            results.value = data.results || [];
        }
    } catch (err) {
        console.error("搜索失败:", err);
    } finally {
        loading.value = false;
    }
};

// 查看详情
const viewDetails = (item) => {
    router.push({
        name: "details",
        params: { id: item.id },
        query: { q: query.value },
    });
};

const goHome = () => {
    router.push({ name: "home" });
};

// 跳转到指定页码
const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        router.push({
            query: {
                ...route.query,
                page,
            },
        });
    }
};

// 监听路由变化
watch(
    () => route.query.page,
    (newPage) => {
        const pageNum = parseInt(newPage) || 1;
        if (pageNum !== currentPage.value) {
            currentPage.value = pageNum;
            fetchResults();
        }
    }
);

// 监听查询参数变化
watch(
    () => route.query.q,
    (newQuery) => {
        if (newQuery !== query.value) {
            fetchResults();
        }
    }
);

// 组件挂载时获取结果
onMounted(() => {
    currentPage.value = initialPage.value;
    fetchResults();
});
</script>
