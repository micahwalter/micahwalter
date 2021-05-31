export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  generate: { 
    fallback: '404.html',
    routes: [
      '/', 
      '/about',
      '/wwms',
      '/studio',
      '/accession',
      '/meditations-in-a-new-home',
    ],
  },

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Micah Walter',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { 
        hid: 'description', 
        name: 'description', 
        content: 'Art, technology, design, work, photography, and writing.' 
      },
      { property: "og:site_name", content: "I Love Painting" },
      { hid: "og:type", property: "og:type", content: "website" },
      {
        hid: "og:url",
        property: "og:url",
        content: "https://www.micahwalter.com",
      },
      {
        hid: "og:title",
        property: "og:title",
        content: "Micah Walter",
      },
      {
        hid: "og:description",
        property: "og:description",
        content: "Art, technology, design, work, photography, and writing.",
      },
      {
        hid: "og:image",
        property: "og:image",
        content: "https://media.micahwalter.com/IMG_1933.JPG",
      },
      { property: "og:image:width", content: "1200" },
      { property: "og:image:height", content: "900" },
      { name: "twitter:site", content: "@micahwalter" },
      { name: "twitter:card", content: "summary_large_image" },
      {
        hid: "twitter:url",
        name: "twitter:url",
        content: "https://www.micahwalter.com",
      },
      {
        hid: "twitter:title",
        name: "twitter:title",
        content: "Micah Walter",
      },
      {
        hid: "twitter:description",
        name: "twitter:description",
        content: "Art, technology, design, work, photography, and writing.",
      },
      {
        hid: "twitter:image",
        name: "twitter:image",
        content: "https://media.micahwalter.com/IMG_1933.JPG",
      },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    link: [
      {
        hid: "canonical",
        rel: "canonical",
        href: "https://www.micahwalter.com",
      },
    ],
    script: [
      {
        hid: 'fathom',
        src: 'https://lark.micahwalter.com/script.js',
        site: 'BQSMBQKX',
        spa: 'auto',
        defer: 'defer',
        once: false,
        skip: process.env.NODE_ENV !== 'production'
      }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/css/tufte.css',
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/content
    '@nuxt/content',
  ],

  // Content module configuration: https://go.nuxtjs.dev/config-content
  content: {},

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
