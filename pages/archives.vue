<template>
  <article>
      <h1>
        Archives
      </h1>
      <p class="subtitle">All the articles.</p>

      <li v-for="article of articles" :key="article.id">
        <NuxtLink :to="`/${article.slug}`">{{ article.title }}</NuxtLink> - {{ article.description }}
      </li>
      
      <hr>
      <nuxt-link to="/">Home</nuxt-link> | <nuxt-link to="/about">About</nuxt-link> | <nuxt-link to="/archives">Archives</nuxt-link>
      <hr>
  </article>
</template>
<script>
export default {
  async asyncData({ $content, params, error }) {
    const articles = await $content("/")
      .only(['title', 'description', 'slug'])
      .sortBy('title', 'asc')
      .fetch()
      .catch(err => {
        error({ statusCode: 404, message: "Page not found" });
      });  


    return {
      articles
    };
  },
}
</script>
