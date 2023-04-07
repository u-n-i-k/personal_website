<script setup lang="ts">
import IconGitHub from './icons/IconGitHub.vue';
</script>

<template>
  <footer>
    <div class="wrapper">
      <div><span class="big-screen">{{ $t("footer.proposal") }}</span> <a href="https://github.com/u-n-i-k/personal_website" class="source-code"><span class="big-screen">{{ $t("footer.source_code_link") }}</span> <span lang="en"><IconGitHub/>GitHub</span></a></div>
      <div>(c) {{ $t("common.my_name") }}, 2023</div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  height: 60px;
  background-color: var(--color-background-3);
}

a.source-code {
  --color-github-icon-fill: var(--color-text);
  color: var(--color-text);
  font-weight: bold;
}

a.source-code:hover {
  --color-github-icon-fill: var(--color-text-3);
  color: var(--color-text-3);
}

footer .wrapper {
  display: flex;
  place-items: flex-start;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
}

@media screen and (max-width: 719px) {
  .big-screen {
    display: none;
  }
}
</style>
