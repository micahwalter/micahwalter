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
    async asyncData({ $content, params, error }) {
      const slug = params.slug || "index";
      const page = await $content(slug)
        .fetch()
        .catch(err => {
          error({ statusCode: 404, message: "Page not found" });
        });

      return {
        page
      };
    }
  };
</script>