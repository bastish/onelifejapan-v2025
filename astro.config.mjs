// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
    outDir: './dist',
    style: {
        sass: {
            site: 'https://www.onelifejapan.com',
            // Tell Sass to look in the node_modules directory for imports
            includePaths: ['./node_modules'],
            integrations: [react(), sitemap()],
        },
    },
});
