import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        proxy: {
            // 配置代理
            "/api": {
                target: "http://localhost:5000", // 代理目标地址
                changeOrigin: true, // 允许跨域
            },
        },
    },
});
