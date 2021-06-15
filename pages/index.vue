<template>
  <article>
      <h1>
        Hi there 👋, I'm Micah Walter
      </h1>
      <p class="subtitle">Welcome to my website.</p>
      <hr>
      <section>
        <h2>More soon!</h2>

        <p>You can usually find me <a href="https://twitter.com/micahwalter">here</a>.</p>
        <p>Here's a little <a href="/about">about</a> me.</p> 
        <p>And be sure to check out "<a href="/wwms">What Would Micah Say?</a>"</p>

      </section>

      <h2 v-if="recents.length > 0">Recently Updated</h2>
      <li v-for="recent of recents" :key="recent.id">
        <NuxtLink :to="`/${recent.slug}`">{{ recent.title }}</NuxtLink> - {{ recent.description }}
      </li>
  </article>
</template>

<script>

export default {
  async asyncData({ $content, error }) {

    const recents = await $content("/")
      .only(['title', 'updatedAt', 'date', 'description', 'slug'])
      .sortBy('updatedAt', 'desc')
      .limit(5)
      .fetch()
      .catch(err => {
        error({ statusCode: 404, message: "Page not found" });
      });  

    return {
      recents
    };
  },
};
</script>