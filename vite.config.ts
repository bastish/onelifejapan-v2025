import { defineConfig } from 'vite';
console.log('host: ', process.env.DEV_HOST);
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
    define: {
        __DEV_HOST__: JSON.stringify(process.env.DEV_HOST || 'localhost'),
    },
});
