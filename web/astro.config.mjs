// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // Public URL where the site is served. Used for sitemap/canonical/OG tags.
  // For a User/Org GitHub Pages site (https://<org>.github.io) base stays "/".
  site: 'https://soda-labo.github.io',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
