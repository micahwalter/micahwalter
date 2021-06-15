<template>
  <article>
      <h1>
        {{ article.title }}
      </h1>
      <p class="subtitle">{{ article.description }}</p>
      <hr>
      <section>
        <nuxt-content :document="article"/>
      </section>
      <h2 v-if="article.recents.length > 0">Recently Updated</h2>
      <li v-for="recent of article.recents" :key="recent.id">
        <NuxtLink :to="`/${recent.slug}`">{{ recent.title }}</NuxtLink> - {{ recent.description }}
      </li>
  </article>
</template>

<script>
import global from '@/utils/global';
import getSiteMeta from '@/utils/getSiteMeta';

export default {
  async asyncData({ $content, params, error }) {
    const slug = params.slug || "index";
    const article = await $content(slug)
      .fetch()
      .catch(err => {
        error({ statusCode: 404, message: "Page not found" });
      });

    const recents = await $content("/")
      .only(['title', 'updatedAt', 'date', 'description', 'slug'])
      .sortBy('updatedAt', 'desc')
      .limit(5)
      .fetch()
      .catch(err => {
        error({ statusCode: 404, message: "Page not found" });
      });  

    if (typeof article !== 'undefined') {
      article['recents'] = recents
    }
    return {
      article
    };
  },
  computed: {
    meta() {
      const metaData = {
        type: 'article',
        title: global.siteTitle,
        description: global.siteDesc,
        url: global.siteUrl,
        mainImage: this.article.image,
      };
      return getSiteMeta(metaData);
    },
  },
  head() {
    return {
      title: global.author,
      meta: [
        ...this.meta,
        {
          property: 'article:published_time',
          content: this.article.createdAt,
        },
        {
          property: 'article:modified_time',
          content: this.article.updatedAt,
        },
        {
          property: 'article:tag',
          content: this.article.tags ? this.article.tags.toString() : '',
        },
        { name: 'twitter:label1', content: 'Written by' },
        { name: 'twitter:data1', content: global.author || '' },
        { name: 'twitter:label2', content: 'Filed under' },
        {
          name: 'twitter:data2',
          content: this.article.tags ? this.article.tags.toString() : '',
        },
      ],
      link: [
        {
          hid: 'canonical',
          rel: 'canonical',
          href: `${global.siteUrl}`,
        },
      ],
    };
  },
};
</script>