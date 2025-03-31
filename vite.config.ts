import { defineConfig } from 'vite';

export default defineConfig({
    // server: {
    //     proxy: {
    //         '/instagram-feed': {
    //             target: 'https://my.onelifejapan.com',
    //             changeOrigin: true,
    //             rewrite: (path) => path.replace(/^\/instagram-feed/, '/instagram-feed.php'),
    //         },
    //     },
    // },
    css: {
        preprocessorOptions: {
            scss: {
                // api: 'modern-compiler',
                // quietDeps: true,
                silenceDeprecations: ['legacy-js-api'],
            },
        },
    },
    define: {
        __DEV_HOST__: JSON.stringify(process.env.DEV_HOST || 'localhost'),
    },
});
