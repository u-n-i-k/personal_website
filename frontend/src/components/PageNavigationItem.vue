<template>
  <div class="page-navigation">
    <h2>{{ $t("common.navigation") }}</h2>
    <div class="page-nav-items">
        <a v-for="item in items" :href="'#' + item.anchor">{{ $t(item.key) }}</a>
    </div>
  </div>
</template>

<style scoped>
@media screen and (max-width: 719px) {
  .page-navigation h2 {
    border-bottom: 2px solid var(--color-background-2);
  }
}

@media screen and (min-width: 720px) {
  .page-navigation {
    min-width: 250px;
    border-right: 2px solid var(--color-background-2);
    margin-right: 50px;
  }
}

h2 {
  padding-top: 1rem;
}
div.page-nav-items {
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

a {
  color: var(--color-text);
  padding: .25rem 0 .25rem .5rem;
  margin: 0;
}
</style>

<script lang="ts">
export default {
  props: {
    items: Object,
  },
  data() {
    return {
    };
  }
};
</script>