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
      <hr>
      <nuxt-link to="/">Home</nuxt-link> | <nuxt-link to="/about">About</nuxt-link> 
      <hr>
      <h3 v-if="article.backlinks.length > 0">Backlinks</h3>
      <li v-for="backlink of article.backlinks" :key="backlink.id">
        <NuxtLink :to="`/${backlink.slug}`">{{ backlink.title }}</NuxtLink> - {{ backlink.description }}
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

    const searchString = '/' + slug
    
    const backlinks = await $content("/")
      .where({
        'text': {$contains: searchString},
        'slug': {$ne: 'index'},
      })
      .fetch()
      .catch(err => {
        error({ statusCode: 404, message: "Page not found" });
      });  

    if (typeof article !== 'undefined') {
      article['backlinks'] = backlinks
    }

    return {
      article
    };
  },
  computed: {
    meta() {
      const metaData = {
        type: 'article',
        title: this.article.title,
        description: this.article.description,
        url: `${global.siteUrl}/${this.$route.params.slug}`,
        mainImage: this.article.image,
      };
      return getSiteMeta(metaData);
    },
  },
  head() {
    return {
      title: global.author + ' | ' + this.article.title,
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
          href: `${global.siteUrl}/${this.$route.params.slug}`,
        },
      ],
    };
  },
};
</script>