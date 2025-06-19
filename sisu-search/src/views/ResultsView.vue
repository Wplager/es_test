<template>
    <header>
        <Header @go-home="goHome" />
    </header>
    <main class="container">
        <div class="results-header">
            <h2 class="results-title">{{ query ? '搜索结果' : '所有记录' }}</h2>
            <div class="results-count">共 {{ totalResults }} 条结果</div>
        </div>

        <div v-if="loading" class="loader-container">
            <div class="loader"></div>
        </div>

        <div v-else>
            <div v-for="result in paginatedResults" :key="result.id" class="result-item" @click="viewDetails(result)">
                <h3 class="result-title">{{ result.title }}</h3>
                <div class="result-meta">
                    <span class="result-meta-item" v-if="result.author">作者: {{ result.author }}</span>
                    <span class="result-meta-item" v-if="result.date">日期: {{ result.date }}</span>
                    <span class="result-meta-item" v-if="result.type">类型: {{ result.type }}</span>
                </div>
                <div class="result-snippet" v-html="highlightMatches(result.snippet, query)"></div>
            </div>

            <Pagination v-if="totalResults > itemsPerPage" :currentPage="currentPage" :totalPages="totalPages"
                :visiblePages="visiblePages" @page-change="goToPage" />
            <div v-else-if="totalResults > itemsPerPage" class="pagination-fallback">
                <button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages">
                    下一页
                </button>
            </div>
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
const totalResults = ref(0);

// 从路由参数获取查询和页码
const query = computed(() => route.query.q || "");
const initialPage = computed(() => parseInt(route.query.page) || 1);

// 分页计算
const totalPages = computed(() => {
    const pages = Math.ceil(totalResults.value / itemsPerPage);
    console.log('Calculated totalPages:', pages, 'from totalResults:', totalResults.value, 'itemsPerPage:', itemsPerPage);
    return pages;
});
const paginatedResults = computed(() => {
    // API already handles pagination, return results directly
    return results.value;
});

const visiblePages = computed(() => {
    // If total pages <= 5, show all pages
    if (totalPages.value <= 5) {
        return Array.from({ length: totalPages.value }, (_, i) => i + 1);
    }

    // Otherwise show up to 5 pages centered around current page
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

        if (!data.results || data.results.length === 0) {
            console.log('No results found for query:', query.value, 'on page:', currentPage.value);
            const allRes = await axios.get("/api/all");
            results.value = allRes.data.results || [];
            totalResults.value = results.value.length;
            console.log('Fallback to all records:', results.value.length, 'items');
        } else {
            results.value = data.results;
            totalResults.value = data.total_results;
            console.log('API response for page', currentPage.value, ':',
                results.value.length, 'items, total_results:', totalResults.value);
        }
        console.log('Current page:', currentPage.value);
        console.log('Total pages:', totalPages.value);
        console.log('Results:', results.value);
        // Reset to page 1 if current page exceeds total pages
        if (currentPage.value > totalPages.value) {
            currentPage.value = 1;
            router.replace({
                query: {
                    ...route.query,
                    page: 1
                }
            });
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
    console.log('Attempting to go to page:', page, 'Current totalPages:', totalPages.value);
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        console.log('Navigating to page:', page, 'with query:', { ...route.query, page });
        router.push({
            query: {
                ...route.query,
                page,
            },
        });
    } else {
        console.warn('Invalid page number:', page, 'valid range: 1 -', totalPages.value);
    }
};

// 监听路由变化
watch(
    () => route.query.page,
    (newPage) => {
        const pageNum = parseInt(newPage) || 1;
        console.log('Route page changed from', currentPage.value, 'to', pageNum);
        if (pageNum !== currentPage.value) {
            currentPage.value = pageNum;
            console.log('Fetching results for page', pageNum);
            fetchResults();
        } else {
            console.log('Page number unchanged, skipping fetch');
        }
    },
    { immediate: true }
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

// Watch for results changes
watch(results, (newVal, oldVal) => {
    console.log('Results changed from', oldVal.length, 'to', newVal.length, 'items');
    console.log('First item changed:',
        oldVal[0]?.id !== newVal[0]?.id ? 'Yes' : 'No');
}, { deep: true });
</script>
