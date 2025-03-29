// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
    style: {
        sass: {
            // Tell Sass to look in the node_modules directory for imports
            includePaths: ['./node_modules'],
        },
    },
});
