// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
    site: 'https://www.onelifejapan.com',
    outDir: './dist',
    integrations: [react(), sitemap()],
    style: {
        sass: {
            // Tell Sass to look in the node_modules directory for imports
            includePaths: ['./node_modules'],
        },
    },
});
