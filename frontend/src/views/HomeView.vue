<script setup lang="ts">
import AboutMeItem from '../components/AboutMeItem.vue'
import ContactsItem from '../components/ContactsItem.vue'
import PageNavigationItem from '../components/PageNavigationItem.vue'
import WorkExperienceItem from '../components/WorkExperienceItem.vue'
</script>

<template>
  <PageNavigationItem :items="nav_items" />
  <div class="scrollable-content">
    <AboutMeItem :block_id="nav_items[0].anchor"/>
    <WorkExperienceItem :block_id="nav_items[1].anchor"/>
    <ContactsItem :block_id="nav_items[2].anchor"/>
  </div>
</template>


<script lang="ts">
export default {
  data() {
    return {
      nav_items: [
        { anchor: 'about',      key: "pages.about.navigation.about"    },
        { anchor: 'experience', key: "pages.about.navigation.work"     },
        { anchor: 'contacts',   key: "pages.about.navigation.contacts" },
      ]
    };
  }
};
</script>