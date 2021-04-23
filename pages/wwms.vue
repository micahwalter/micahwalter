<template>
  <p v-if="$fetchState.pending">Fetching saying...</p>
  <p v-else-if="$fetchState.error">An error occurred :(</p>
  <div v-else>
    <h1>What Would Micah Say?</h1>

    <blockquote>{{ micah.micah.says }}</blockquote>

    <button @click="$fetch">Refresh</button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        micah: {}
      }
    },
    async fetch() {
      this.micah = await fetch(
        'https://api.micahwalter.com/wwms'
      ).then(res => res.json())
    }
  }
</script>