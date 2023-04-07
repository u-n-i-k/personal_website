<template>
  <div :class="getClass()" :id="block_id">
    <h2>
      {{ $t("common.experience.title") }}
      <a class="headerlink" :href="'#' + block_id">#</a>
    </h2>
    <div v-for="item in info.history" class="experience_item">
      <div class="working_period">{{ item.start_dt }} - {{ item.finish_dt || $t("common.experience.now") }}</div>
      <div>
        <h3 class="position">{{ item.position }} {{ $t("common.experience.at") }} <a target="_blank" rel="noopener noreferrer" :href="item.company.website">{{ item.company.name }}</a></h3>
        <div class="technologies"><p v-for="technology in item.technologies" class="technology">{{ technology }}</p></div>
        <div class="description">{{ item.job_description }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h2 {
  padding-top: 1rem;
  border-bottom: 2px solid var(--color-background-2);
}
.experience_item {
  padding: 1rem 0;
}
.experience_item ~ .experience_item {
  border-top: 2px solid var(--color-background-3);
}

.technologies {
  display: flex;
  place-items: flex-start;
  flex-wrap: wrap;
  justify-content: start;
  align-items: center;

  --indentation: .25rem;

  margin: calc(-1 * var(--indentation));
}
.technology {
  background: var(--color-background-2);
  color: var(--color-text-3);
  border-radius: 1rem;
  padding: 0 calc(var(--indentation) * 2);
  margin: var(--indentation);
  white-space: nowrap;
}

.description {
  margin-top: 1rem;
}
</style>

<script lang="ts">
interface CompanyInfo {
  name: string
  website: string
};

interface WorkExperienceItem {
  job_description: string
  position: string
  company: CompanyInfo
  start_dt: string
  finish_dt: string | null
  technologies: string[]
};

interface WorkExperienceHistory {
  history: WorkExperienceItem[]
};

import { mapGetters } from 'vuex';
export default {
  props: {
    block_id: String,
  },
  data() {
    let info: WorkExperienceHistory = {"history": []}
    return {
      api_url: import.meta.env.VITE_API_ROOT + 'work/history',
      info: info,
      loading: true,
      errored: false
    };
  },
  computed: {
    ...mapGetters(["locale"])
  },

  watch: {
    locale(newValue) {
      this.getWorkExperience();
    }
  },

  mounted() {
    this.getWorkExperience();
  },

  methods: {
    getWorkExperience() {
      this.errored = false;
      this.loading = true;

      let req_config = {
        params: {
          lang: this.locale
        }
      };

      this.axios.get(this.api_url, req_config).then(
        (response) => {
          this.info = response.data;
        }
      ).catch(
        (error) => {
          console.log(error);
          this.errored = true;
        }
      ).finally(() => (this.loading = false));
    },
    getClass() {
      if (this.errored) {
        return 'errored';
      } else if (this.loading) {
        return 'loading';
      } else {
        return '';
      }
    }
  }
};
</script>