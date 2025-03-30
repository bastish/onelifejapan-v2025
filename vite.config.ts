import { defineConfig } from 'vite';

const SCSS_Logger = {
    warn(message: string, options: any) {
        console.log('######################');
        console.log('######################');
        console.log('######################');
        console.log('######################');
        console.log('SCSS Logger triggered:', message, options);
        // Mute "Mixed Declarations" warning
        if (message.includes('Deprecation Warning')) {
            return;
        }
        if (options.deprecation && message.includes('mixed-decls')) {
            return;
        }
        // List all other warnings
        console.warn(`▲ [WARNING]: ${message}`);
    },
};

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
                logger: SCSS_Logger,
                api: 'modern',
                silenceDeprecations: ['mixed-decls'],
            },
        },
    },
});
