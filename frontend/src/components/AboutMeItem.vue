<template>
    <div :id="block_id" class="main-item">
      <h2>
        {{ $t("common.about.title") }}
        <a class="headerlink" :href="'#' + block_id">#</a>
      </h2>
      <div class="about" :class="getClass()">
        <img src="@/assets/photo.png" />
        {{ info.about }}
      </div>
    </div>
  </template>
  
  <style scoped>
  img {
    width: 200px;
    filter: brightness(var(--brightness));
    border-radius: .25rem;
    max-width: 25vw;
    float: right;
    margin: 0 0 1rem 1rem;
  }
  h2 {
    padding-top: 1rem;
    border-bottom: 2px solid var(--color-background-2);
  }
  .about {
    padding: 1rem 0;
    font-size: 1.1rem;
  }
  </style>
  
  <script lang="ts">
  interface InfoAboutMe {
    about: string
  };

  import { mapGetters } from 'vuex';
  export default {
    props: {
      block_id: String,
    },
    data() {
      let info: InfoAboutMe = {"about": ""}
      return {
        api_url: import.meta.env.VITE_API_ROOT + 'me/about',
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
        this.getInfoAboutMe();
      }
    },
  
    mounted() {
      this.getInfoAboutMe();
    },
  
    methods: {
      getInfoAboutMe() {
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