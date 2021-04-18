<template>
  <article>
      <h1>
        {{ page.title }}
      </h1>
      <p class="subtitle">{{ page.description }}</p>
      <hr>
      <section>
        <nuxt-content :document="page"/>
      </section>
  </article>
</template>

<script>
  export default {
    async asyncData({ $content }) {
      const page = await $content("about").fetch()

      return {
        page
      };
    }
  };
</script>